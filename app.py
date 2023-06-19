import csv
import os
import zipfile

import cv2

import data


class CreateCSVAndImages:
    def __init__(self, filename):
        self.filename = filename
        self.file = open(self.filename, "w")
        self.writer = csv.writer(self.file)
        self.writer.writerow(["Image Name", "Link", "Subject", "Width"])

    def write(self, name, link, subject, width):
        self.writer.writerow([name, link, subject, width])

    def close(self):
        self.file.close()


def main():
    # change according to your needs
    format_image = "png"
<<<<<<< HEAD
    name_request = "cewwa"
    lines = getattr(data, name_request)
=======
    lines = data.e137a
>>>>>>> 7d3c8af (add data;)

    # Read image
    image = cv2.imread(f"image.{format_image}")
    output_folder = name_request
    output_folder_images = os.path.join(output_folder, "images")
    # create the folder to save the output
    os.makedirs(output_folder_images, exist_ok=True)

    csv_file = CreateCSVAndImages(os.path.join(output_folder, "eblast.csv"))

    for index, value in enumerate(lines):
        initial_height = 0 if index == 0 else int(
            lines[index - 1]["end_pixel"])

        for index_x, val_x in enumerate(value["lines_x"]):
            value_x = val_x
            url = ""
            # check type of value_x is a dictionary
            if isinstance(val_x, dict):
                value_x = val_x["size"]
                url = val_x["url"]

            initial_width = 0 if index_x == 0 else int(value["lines_x"][index_x - 1]["size"]) if isinstance(
                value["lines_x"][index_x - 1], dict) else int(value["lines_x"][index_x - 1])

            new_image = image[initial_height:int(
                value["end_pixel"]), initial_width:int(value_x)]

            file_name_number = f"0{index+1}" if index < 9 else f"{index+1}"
            if len(value["lines_x"]) > 1:
                file_name_number += f"-{index_x+1}"

            file_name = f"image {file_name_number}.{format_image}"

            csv_file.write(file_name, url, "", new_image.shape[1])

            cv2.imwrite(os.path.join(
                output_folder_images, file_name), new_image)

    csv_file.close()

    # Create zip file
    zip_file_name = os.path.join(output_folder, f"{name_request} response.zip")
    with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as zip_file:
        # Add the eblast.csv file
        zip_file.write(os.path.join(output_folder, "eblast.csv"), "eblast.csv")

        # Add the images folder and its contents
        for root, dirs, files in os.walk(output_folder_images):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.join("images", file))


if __name__ == "__main__":
    main()
