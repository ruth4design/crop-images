import argparse
import csv
import os

parser = argparse.ArgumentParser(description='Generate an HTML file with images from a CSV file')
parser.add_argument('file_name', help='CSV file with image data')
parser.add_argument('output_dir', help='Directory to output HTML file')
args = parser.parse_args()

with open(args.file_name, newline='') as csv_file:
    reader = csv.DictReader(csv_file)
    data = [row for row in reader]

data.sort(key=lambda x: x['Image Name'])

rows = []
current_row = []
for row in data:
    if current_row and row['Image Name'].split("-")[0] == current_row[0]['Image Name'].split("-")[0]:
        current_row.append(row)
    else:
        rows.append(current_row)
        current_row = [row]
rows.append(current_row)

html_file_path = os.path.join(args.output_dir, 'index.html')
with open(html_file_path, 'w') as html_file:
    html_file.write('<!DOCTYPE html>\n')
    html_file.write('<html lang="en">\n')
    html_file.write('<head>\n')
    html_file.write('<meta charset="UTF-8">\n')
    html_file.write('<style>\n')
    html_file.write('body {\n')
    html_file.write('  max-width: 650px;\n')
    html_file.write('  margin: 0 auto;\n')
    html_file.write('}\n')
    html_file.write('.row {\n')
    html_file.write('  display: flex;\n')
    html_file.write('}\n')
    html_file.write('</style>\n')
    html_file.write('</head>\n')
    html_file.write('<body>\n')
    for row in rows:
        html_file.write('<div class="row">\n')
        for image in row:
            if image["Link"]:
                html_file.write(f'<a href="{image["Link"]}">')
            html_file.write(f'<img src="images/{image["Image Name"]}" alt="{image["Subject"]}" width="{image["Width"]}">')
            if image["Link"]:
                html_file.write('</a>')
            html_file.write('\n')
        html_file.write('</div>\n')
    html_file.write('</body>\n')
    html_file.write('</html>\n')

print(f'HTML file generated at {html_file_path}')
