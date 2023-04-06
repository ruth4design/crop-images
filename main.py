import csv
import os

import cv2

import data

colors = {
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "purple": "\033[95m",
    "cyan": "\033[96m",
    "white": "\033[97m",
    "black": "\033[98m",
    "end": "\033[0m",
}

the_axis = {
    "x": "column",
    "y": "row",
}


def get_lines(num_line_x=1, max_pixel_size=1000, axis="x"):
    # get the lines from the prompt
    lines = []
    is_last_line = False
    num_line_y = 1
    min_width = 0
    while not is_last_line:
        print(f"""
          {colors['yellow']}max allowed:{colors['purple']} {max_pixel_size}
        """)
        line = input(f"{colors['green']}[ENTER to finish columns]{colors['end']} {colors['blue']}Field {num_line_x}, cut on {the_axis[axis]} => {num_line_y}: {colors['yellow']} (min allowed:{colors['purple']} {min_width+1}){colors['end']}")
        try:
            if line == "":
                is_last_line = True
                lines.append(max_pixel_size)
                continue
            if int(line) == max_pixel_size:
                is_last_line = True
                lines.append(max_pixel_size)
                continue
            if int(line) > max_pixel_size:
                print(
                    "\033[93mThe number is bigger than the max width of Image\033[0m")
                continue
            if int(line) <= min_width:
                print(
                    "\033[93mThe number is smaller than the min width allowed\033[0m")
                continue
            else:
                num_line_y += 1
                min_width = int(line)
            lines.append(line)
        except ValueError:
            print("\033[91mThe value is not a number\033[0m")
    return lines


# this is deprecated, but I'm keeping it for now (it uses the old data format, by terminal)
def cut_image(image):
    height = image.shape[0]
    width = image.shape[1]

    lines = []
    last_field_pixel = 0
    field = 1
    is_last_line = False

    while not is_last_line:
        end_pixel = input(f"""
      {colors['blue']}Enter the HEIGHT to cut
      max height {colors['purple']}{height} {colors['blue']}
[FIELD:{field}]{colors['green']}[ENTER to finish]{colors['end']} (min value {colors['purple']} {last_field_pixel}{colors['end']}) """)

        lines_x = []

        if end_pixel == "":
            lines_x = get_lines(num_line_x=field, max_pixel_size=width)
            is_last_line = True
            last_field_pixel = height
            lines.append({
                "end_pixel": height,
                "lines_x": lines_x
            })
            continue
        if int(end_pixel) > height:
            print(
                "\033[93mThe number is bigger than the max height of Image\033[0m")
            continue
        if int(end_pixel) <= last_field_pixel:
            print(
                "\033[93mThe number is smaller than the min height allowed\033[0m")
            continue
        else:
            lines_x = get_lines(num_line_x=field, max_pixel_size=width)
            last_field_pixel = int(end_pixel)

        lines.append({
            "end_pixel": end_pixel,
            "lines_x": lines_x
        })
        print(lines)
        field += 1

    print(lines)

    # for with index and value in lines:
    for index, value in enumerate(lines):
        initial_height = 0
        if index == 0:
            initial_height = 0
        else:
            initial_height = int(lines[index - 1]["end_pixel"])

        for index_x, value_x in enumerate(value["lines_x"]):
            initial_width = 0
            if index_x == 0:
                initial_width = 0
            else:
                initial_width = int(value["lines_x"][index_x - 1])

            new_image = image[initial_height:int(
                value["end_pixel"]), initial_width:int(value_x)]
            cv2.imwrite(f"main_cut_{index}_{index_x}.jpg", new_image)
            print(index, value)


class CreateCSV:
    def __init__(self, filename):
        self.filename = filename
        self.file = open(f"{filename}", "w")
        self.writer = csv.writer(self.file)
        self.writer.writerow(["Image Name", "Link", "Subject", "Width"])

    def write(self, name, link, subject, width):
        self.writer.writerow([name, link, subject, width])

    def close(self):
        self.file.close()


def __main__():
    # Read image
    image = cv2.imread("image.jpg")

    output_folder = "output"
    output_folder_images = output_folder + "/images/"
    format_image = "jpg"
    # create the folder to save the output
    if not os.path.exists(output_folder_images):
        print("creating folder")
        os.makedirs(output_folder_images)

    csv_file = CreateCSV(output_folder + "/eblast.csv")

    #change according to your needs
    lines = data.e84

    for index, value in enumerate(lines):
        initial_height = 0
        if index == 0:
            initial_height = 0
        else:
            initial_height = int(lines[index - 1]["end_pixel"])

        for index_x, val_x in enumerate(value["lines_x"]):
            value_x = val_x
            url = ""
            # check type of value_x is a dictionary
            if type(val_x) is dict:
                print("is a dict", val_x)
                value_x = val_x["size"]
                url = val_x["url"]

            initial_width = 0
            if index_x == 0:
                initial_width = 0
            else:

                if type(value["lines_x"][index_x - 1]) is dict:
                    initial_width = int(value["lines_x"][index_x - 1]["size"])
                else:
                    initial_width = int(value["lines_x"][index_x - 1])

            new_image = image[initial_height:int(
                value["end_pixel"]), initial_width:int(value_x)]
            
            file_name_number = ""
            if index < 9:
                file_name_number = f"0{index+1}"
            else:
                file_name_number += f"{index+1}"
            print(value["lines_x"])
            if len(value["lines_x"]) > 1:
                file_name_number += f"-{index_x+1}"
            
            file_name = f"image {file_name_number}.{format_image}"

            csv_file.write( file_name, url, '', new_image.shape[1])

            cv2.imwrite(output_folder_images+file_name, new_image)
            print(value)
    return 0


if __name__ == "__main__":
    __main__()
