from flask import Flask, render_template, request, send_from_directory
from lancedb.embeddings import EmbeddingFunctionRegistry
from PIL import Image
import lancedb
from lancedb.pydantic import LanceModel, Vector
from pathlib import Path
from random import sample
import pandas as pd
from itertools import chain
import re, os
import argparse
import urllib.parse

parser = argparse.ArgumentParser(description='Image search application')
parser.add_argument('--image-folder', type=str, default='images', help='Path to the folder containing the images')
args = parser.parse_args()


app = Flask(__name__)

# Configure LanceDB and load the image search table
registry = EmbeddingFunctionRegistry.get_instance()
clip = registry.get("open-clip").create(max_retries=0)

class Media(LanceModel):
    vector: Vector(clip.ndims()) = clip.VectorField()
    image_uri: str = clip.SourceField()

    @property
    def image(self):
        return Image.open(self.image_uri)


db = lancedb.connect(f"database")

def is_valid_file(file_path):
    """
    Check if a file is valid based on its extension and name.

    Args:
        file_path (str or pathlib.Path): The path to the file.

    Returns:
        bool: True if the file is valid, False otherwise.

    Criteria for a valid file:
    - The file must exist and be a file (not a directory).
    - The file extension must be one of the supported image formats: '.jpg', '.jpeg', or '.png'.
    - The file name must not contain any special characters: '#', '?', 'NUL', '\\', '/', ':', '*', '?', '"', '<', '>', '|'.

    Example usage:
        file_path = 'path/to/image.jpg'
        if is_valid_file(file_path):
            # Process the valid file
        else:
            # Skip the invalid file
    """
    if not os.path.isfile(file_path):
        return False

    _, ext = os.path.splitext(file_path)
    if ext.lower() not in ['.jpg', '.jpeg', '.png']:
        return False

    file_name = os.path.basename(file_path)
    special_chars_pattern = re.compile(r'[#?\\/:*?"<>|]')
    if special_chars_pattern.search(file_name):
        print("skipped", file_name)
        return False

    return True


def get_valid_table_name(folder_path):
    # Remove any special characters and replace them with underscores
    table_name = re.sub(r'[^a-zA-Z0-9]', '_', folder_path)
    # Remove leading and trailing underscores
    table_name = table_name.strip('_')
    return table_name

image_folder_path = args.image_folder
table_name = get_valid_table_name(image_folder_path)

if table_name in db:
    print("--------")
    print(f'Table {table_name} exists already. If you want to create a new table with same name, please rename your folder or delete existing table from database/folder_name.lance')
    print("--------")
    table = db[table_name]
else:
    try:
        print("Creating new table...")
        table = db.create_table(table_name, schema=Media, mode="overwrite")
        
        p = Path(image_folder_path).expanduser()
        uris = [str(f.absolute()) for f in p.iterdir() if is_valid_file(f)]
        
        table.add(pd.DataFrame({"image_uri": uris}))
    except Exception as e:
        print('here')
        if image_folder_path in db:
            db.drop_table(table_name)
        raise e

@app.route('/', methods=['POST', 'GET'])
def image_search():
    results = []
    if request.method == 'POST':
        search_query = request.form.get('search')
        query_image = request.files.get('image')
        image_url = request.form.get('image_url')
        
        if search_query:
            # Perform text-based image search
            rs = table.search(search_query).limit(40).to_pydantic(Media)
            results = [{'image_uri': item.image_uri} for item in rs]
        elif query_image:
            # Perform image-based search
            query_image = Image.open(query_image)
            rs = table.search(query_image).limit(40).to_pydantic(Media)
            results = [{'image_uri': item.image_uri} for item in rs]
        elif image_url:
            # Perform image-based search using the URL
            image_path = image_url.replace(request.host_url + 'images/', '')
            decoded_image_path = urllib.parse.unquote(image_path)
            query_image = Image.open(os.path.join(image_folder_path, decoded_image_path))
            rs = table.search(query_image).limit(40).to_pydantic(Media)
            results = [{'image_uri': item.image_uri} for item in rs]

    return render_template('image_search.html', results=results)

@app.route('/images/<path:filename>')
def serve_image(filename):
    # mention the folder name here
    return send_from_directory(image_folder_path, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
