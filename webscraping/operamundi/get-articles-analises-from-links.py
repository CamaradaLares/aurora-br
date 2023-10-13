import os
import requests
from bs4 import BeautifulSoup
import threading
import re  # Import the regular expressions module

semaphore = threading.Semaphore(10)


# Add the clean_text function
def clean_text(text):
    print("Start cleaning.")
    # Replace multiple spaces with a single space
    text = re.sub(r' +', ' ', text)
    # Replace multiple newlines with a single newline
    text = re.sub(r'\n+', '\n', text)
    # remove repeting words
    text = re.sub(r'\(\*\).*', '', text, flags=re.DOTALL)
    text = re.sub(r'Você que chegou até aqui e que acredita em uma mídia autônoma.*', '', text, flags=re.DOTALL)
    
    # Replace multiple occurrences of any punctuation mark with a single instance
    text = re.sub(r'([!@#$%^&*()_+={}\[\]:;"\'<>,.?/~`|\\-])\1+', r'\1', text)
    print("Finished cleaning.")
    return text

# Existing function to extract articles
def extract_article_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    article_content = ''
    for div in soup.find_all('div'):
        for p in div.find_all('p'):
            article_content += p.get_text() + '\n'
    content_div = soup.find('div', {'class': 'content conteiner-fluid'})
    if content_div:
        for p in content_div.find_all('p'):
            article_content += p.get_text() + '\n'  # Fixed this line to actually add the text

    # Call the clean_text function to clean the extracted article
    cleaned_article = clean_text(article_content)
    return cleaned_article


def process_link(link, articles_folder):
    # Acquire the semaphore
    semaphore.acquire()
    
    try:
        link = link.strip()
        response = requests.get(link)
        html_content = response.text
        filename = link.split('/')[-1].replace(' ', '_').replace('%', '_') + '.txt'
        filepath = os.path.join(articles_folder, filename)
        article_content = extract_article_from_html(html_content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(article_content)
        
        # Explicitly close the response
        response.close()
    finally:
        # Release the semaphore
        semaphore.release()

def save_articles_from_links(links_file, articles_folder):
    if not os.path.exists(articles_folder):
        os.makedirs(articles_folder)
    
    with open(links_file, 'r', encoding='utf-8') as f:
        links = f.readlines()

    threads = []

    for link in links:
        thread = threading.Thread(target=process_link, args=(link, articles_folder))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# File containing the list of links (replace with your actual file)
links_file = 'unique_extracted_hrefs-analises.txt'
# Folder to save the articles (replace with your desired folder)
articles_folder = 'cleaned_extracted_articles_analises'

# Run the function
save_articles_from_links(links_file, articles_folder)

