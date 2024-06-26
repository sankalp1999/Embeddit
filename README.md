# Embeddit: Image Search Using CLIP and LanceDB

Embeddit is a Python/flask app that allows you to search for images using text queries or by uploading an image (image to image search). It uses the OpenAI [CLIP](https://github.com/mlfoundations/open_clip) for embedding images and stores in the vectors in [LanceDB](https://github.com/lancedb/lancedb).



## Table of Contents

1. [Features](#features)

2. [Prerequisites](#prerequisites)

3. [Setup](#setup)

   - [Setting up a Python Virtual Environment](#setting-up-a-python-virtual-environment)

   - [Activating the Virtual Environment](#activating-the-virtual-environment)

   - [Installing Dependencies](#installing-dependencies)

4. [Usage](#usage)

5. [License](#license)

## Features

- Text-based image search: Users can enter a text query to search for relevant images.

- Image-based search: Users can upload an image to find visually similar images.

- Efficient similarity search using LanceDB.

- User-friendly web interface for seamless interaction.

- Customizable image folder for indexing and searching.

## Prerequisites

Before setting up Embeddit, ensure that you have the following prerequisites installed:

- Python 3.8 or higher

- pip (Python package installer)

## Setup


1. navigate to the project folder

   ```
   cd Embeddit
   ```

   create the virtual environment.

   ```

   python3 -m venv embeddit_env

   ```

   This will create a new virtual environment named embeddit_env.



2. To activate the virtual environment, run the appropriate command based on your operating system:

- For Windows:

  ```

  embeddit_env\Scripts\activate

  ```

- For macOS and Linux:

  ```

  source embeddit_env/bin/activate

  ```

3. Install necessary dependencies. I try to keep them at minimum.

    ```

    pip install -r requirements.txt

    ```

    

## Usage

To run the Embeddit application, follow these steps:

1. Ensure that you have activated the virtual environment.

2. Place the images you want to index and search in the designated image folder (default: `images/` folder).

3. Run the following command to start the application:


   ```

   python app_image_search.py --image-folder path/to/your/image/folder

   ```

   Replace path/to/your/image/folder with the actual path to the folder containing your images. By default, uses `images/` folder in the project directory.

4. Open a web browser and visit http://localhost:5000 to access the Embeddit web interface.

5. Use the search bar to enter **text queries** or **upload an image** to find visually similar images.

## License

Embeddit is released under the [MIT License](LICENSE).