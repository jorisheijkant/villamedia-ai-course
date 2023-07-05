# Convert the csv file to .txt files, using the first column as the .txt content
# Generate a file name based on the first column

import csv
import os

file_name = "funds"
column_to_read = 0

# Create a folder inside the /texts folder if it doesn't exist
if not os.path.exists(f"texts/{file_name}"):
    os.makedirs(f"texts/{file_name}")

# Read the csv file
with open(f"csv/{file_name}.csv", 'r') as csv_file:
    print(f"Reading {file_name}.csv")
    csv_reader = csv.reader(csv_file)
    next(csv_reader) # Skip the first line
    for line in csv_reader:
        # Create a hash based on the first column
        text_content = line[column_to_read]
        print(f"Text: {text_content}")
        text_hash = hash(text_content)
        print(f"Hash: {text_hash}")
        # Convert to a string and remove possible negative sign
        text_hash = str(text_hash).replace("-", "")
        file_path = f"texts/{file_name}/{text_hash}.txt"
        # Create a txt file 
        with open(file_path, 'w') as txt_file:
            txt_file.write(text_content)
