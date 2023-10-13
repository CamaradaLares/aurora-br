import os
import re
import requests  # Uncomment this line when running locally
from bs4 import BeautifulSoup

# Function to read URLs from a text file
def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file.readlines()]
    return urls

# Function to download article (commented out as it needs internet access)
def download_article(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to download article from {url}")
        return None

# Function to extract article based on <p> tags
def extract_article(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    paragraphs = soup.find_all('p')
    article_text = ' '.join([p.get_text() for p in paragraphs])
    return article_text

# Function to clean text
def clean_text(text):
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'Copyright.*', '', text)
    return text

# Main function to process URLs
def process_urls(urls, output_folder):
    for i, url in enumerate(urls):
        # Uncomment the following line when running locally
        html_content = download_article(url)
        
        # Comment the following line when running locally
        #html_content = "<p>This is a sample paragraph.</p>"  # Replace with downloaded HTML content
        
        article_text = extract_article(html_content)
        cleaned_text = clean_text(article_text)
        
        output_file_path = os.path.join(output_folder, f'article_{i+1}.txt')
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(cleaned_text)

        print("Article " + str(url) + " saved")

if __name__ == "__main__":
    url_file_path = "unique_extracted_links-novademocracia.txt"  # Replace with the path to your text file containing URLs
    urls = read_urls_from_file(url_file_path)
    output_folder = "cleaned_extracted_articles_novademocracia"  # Output folder name
    os.makedirs(output_folder, exist_ok=True)
    process_urls(urls, output_folder)

