import nltk
import os
from pathlib import Path

# Specify the directory to save NLTK data
nltk_data_dir = Path("nltk_data")

# Check if NLTK data directory exists, if not, create it
if not nltk_data_dir.exists():
    nltk_data_dir.mkdir()

# Set NLTK data directory
nltk.data.path.append(nltk_data_dir)

# Download and save NLTK resources if not already present
def download_nltk_resources():
    resources = ['punkt', 'stopwords']
    languages = ['fr']
    
    for resource in resources:
        if not nltk_data_dir.joinpath('tokenizers', resource).exists():
            nltk.download(resource, download_dir=nltk_data_dir)

    for lang in languages:
        if not nltk_data_dir.joinpath('corpora', 'stopwords', lang).exists():
            nltk.download(resource, download_dir=nltk_data_dir)

# Call the function to download resources
download_nltk_resources()

# Now you can use NLTK with the locally saved resources
