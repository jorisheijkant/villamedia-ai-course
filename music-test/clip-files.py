# This script is used to clip the songs in the og-files folder to 15 second clips
# And save them in the clips folder

import os
import pydub
from pydub import AudioSegment

# Loop over the folders in the og-files folder and the files within them
for folder in os.listdir('og-files'):
    print(f"Now clipping songs in {folder} folder")
    # Ignore the .DS_Store file
    if folder == '.DS_Store':
        continue
    for file in os.listdir(f'og-files/{folder}'):
        # Ignore the .DS_Store file
        if file == '.DS_Store':
            continue
        # Load the song
        song = AudioSegment.from_file(f'og-files/{folder}/{file}')
        # Clip the song to 15 seconds, starting at 2:00
        clip = song[120000:135000]
        # Save the clip in the clips folder
        clip.export(f'clips/{folder}/{file}', format='mp3')
        print(f"Clipped {file} to 15 seconds")

print("Done clipping songs")