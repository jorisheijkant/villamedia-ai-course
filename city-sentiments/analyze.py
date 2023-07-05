# This script analyzes the sentiment of the various texts in the /data folder
from transformers import pipeline
import os

# Set up the pipeline
classifier = pipeline("sentiment-analysis", model='DTAI-KULeuven/robbert-v2-dutch-sentiment')

# Analyze the sentiment of a text
def analyze(text):
    return classifier(text)

chunk_size = 256
cities = []

# Test the pipeline
if __name__ == '__main__':
    # Loop over the texts in the /data subfolders
    for folder in os.listdir('data'):
        for file in os.listdir(f'data/{folder}'):
            print(f"Analyzing folder for {folder}")

            file_path = f'data/{folder}/{file}'
            with open(file_path, 'r') as txt_file:
                text = txt_file.read()
                # Make text into one line string
                text = text.replace('\n', ' ')

                # Break the text into chunks of 512 characters
                chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
                print(f"Analyzing {file_path}...")
                print(f"Has {len(chunks)} chunks of {chunk_size} characters each")

                if folder not in [city["name"] for city in cities]:
                    cities.append({
                        'name': folder,
                        'positive_passages': 0,
                        'negative_passages': 0,
                        'total_passages': 0
                    })

                # Analyze each chunk
                for chunk in chunks:
                    for city in cities:
                        if city['name'] == folder:
                            city["total_passages"] += 1
                            analysis = analyze(chunk)
                            print(analysis)
                            if analysis[0]['label'] == 'Positive':
                                city["positive_passages"] += 1
                            elif analysis[0]['label'] == 'Negative':
                                city["negative_passages"] += 1


    # Print the results
    print(cities)

    # Write the results to a csv file
    with open('results.csv', 'w') as csv_file:
        csv_file.write('city,positive_passages,negative_passages,total_passages\n')
        for city in cities:
            csv_file.write(f"{city['name']},{city['positive_passages']},{city['negative_passages']},{city['total_passages']}\n")

    

