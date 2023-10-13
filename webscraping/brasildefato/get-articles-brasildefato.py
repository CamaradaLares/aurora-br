import os
import re
from bs4 import BeautifulSoup
from bs4 import NavigableString

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
    paragraphs = []
    
    for p in soup.find_all('p'):
        # If <p> contains only text, append it
        if p.string:
            paragraphs.append(p.string)
        else:
            # If <p> contains nested tags like <span>, extract text from them
            for content in p.contents:
                if content.string:
                    paragraphs.append(content.string)
                    
    article_text = ' '.join(paragraphs)
    return article_text

# Function to clean text
def clean_text(text):
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    
    text = re.sub(r'Ouça a entrevista na íntegra no tocador de áudio abaixo do título desta matéria\..*', '', text)
    text = re.sub(r'Edição\:.*', '', text, flags=re.DOTALL)
    text = re.sub(r'Clique aqui.*', '', text, flags=re.DOTALL)
    text = re.sub(r'Confira abaixo a entrevista.*', '', text, flags=re.DOTALL)
    text = re.sub(r'Fonte\:.*', '', text, flags=re.DOTALL)
    text = re.sub(r'Assista\:.*', '', text, flags=re.DOTALL)
    
    
        
    return text

# Main function to process URLs
def process_urls(urls, output_folder, max_retries=3):
    for i, url in enumerate(urls[37200:],37200):
        retries = 0  # Initialize retry counter for each URL
        
        while retries < max_retries:
            try:
                # Attempt to download and process the article
                html_content = download_article(url)
                
                if html_content is None:
                    print(f"Skipping URL due to download failure: {url}")
                    break  # Exit while loop
                
                article_text = extract_article(html_content)
                cleaned_text = clean_text(article_text)
                
                output_file_path = os.path.join(output_folder, f'article_{i+1}.txt')
                with open(output_file_path, 'w', encoding='utf-8') as file:
                    file.write(cleaned_text)

                print(f"Article {url} saved")
                break  # Successfully processed, exit while loop

            except TypeError as e:
                if "object of type 'NoneType' has no len()" in str(e):
                    print(f"Caught specific TypeError for URL {url}. Retrying...")
                    retries += 1  # Increment retry counter
                
                else:
                    # Different TypeError, don't retry
                    print(f"Caught different TypeError for URL {url}: {e}")
                    break

            except Exception as e:
                # Catch all other exceptions and break the loop
                print(f"Error occurred for URL {url}: {e}")
                break


if __name__ == "__main__":
    url_file_path = "unique_extracted_links-brasildefato.txt"  # Replace with the path to your text file containing URLs
    urls = read_urls_from_file(url_file_path)
    output_folder = "cleaned_extracted_articles_brasildefato"  # Output folder name
    os.makedirs(output_folder, exist_ok=True)
    process_urls(urls, output_folder)

