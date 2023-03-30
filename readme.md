this python script is to crop images according to the coordinates of the bounding box

# Usage of the script

1. create the environment

```bash
python3 -m venv venv
```

2. activate the environment

```bash
source venv/bin/activate
```

3. install the dependencies

```bash
pip install -r requirements.txt
```

4. move the image file to the same directory as the script named `image.png` or change the name of the image file in the script to the name of the image file you want to crop

5. run the script

```bash
python3 main.py
```

6. the cropped images will be saved in the `output` folder


# generate html file

1. run the script with the file name and the output directory

```bash
python3 generate_html.py <file_name> <output_dir>
```

2. the html file will be saved in the `output` folder

# get the size of the image

1. run the script with the file name and the output directory

```bash
python3 get_image_size.py
```
# Dependencies

check the requirements.txt file

# Note

The script is written in python 3.11.2
