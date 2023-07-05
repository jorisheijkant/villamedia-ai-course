# This script analyzes the sentiment of the various texts in the /data folder
from transformers import pipeline
import os

# Set up the pipeline
classifier = pipeline("sentiment-analysis", model='DTAI-KULeuven/robbert-v2-dutch-sentiment')

# Analyze the sentiment of a text
def analyze(text):
    return classifier(text)

chunk_size = 256
articles = []

# Test the pipeline
if __name__ == '__main__':
    # Loop over the texts in the /data subfolders
    for file in os.listdir('data'):
            print(f"Analyzing article {file}")

            file_path = f'data/{file}'
            with open(file_path, 'r') as txt_file:
                text = txt_file.read()
                # Make text into one line string
                text = text.replace('\n', ' ')

                # Break the text into chunks of 512 characters
                chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
                print(f"Analyzing {file_path}...")
                print(f"Has {len(chunks)} chunks of {chunk_size} characters each")

                if file not in [article["name"] for article in articles]:
                    articles.append({
                        'name': file,
                        'positive_passages': 0,
                        'negative_passages': 0,
                        'total_passages': 0
                    })

                # Analyze each chunk
                for chunk in chunks:
                    for article in articles:
                        if article['name'] == file:
                            article["total_passages"] += 1
                            analysis = analyze(chunk)
                            print(analysis)
                            if analysis[0]['label'] == 'Positive':
                                article["positive_passages"] += 1
                            elif analysis[0]['label'] == 'Negative':
                                article["negative_passages"] += 1


    # Print the results
    print(articles)

    # Write the results to a csv file
    with open('articles.csv', 'w') as csv_file:
        csv_file.write('article,positive_passages,negative_passages,total_passages\n')
        for article in articles:
            csv_file.write(f"{article['name']},{article['positive_passages']},{article['negative_passages']},{article['total_passages']}\n")

    

