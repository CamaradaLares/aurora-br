import os
from bs4 import BeautifulSoup

def extract_links_from_directory(directory_path, output_file):
    # Initialize a list to store all unique links across multiple files
    all_links = []
    
    # Step 1: List all HTML files in the directory
    html_files = [f for f in os.listdir(directory_path) if f.endswith('.html')]
    
    for html_file in html_files:
        file_path = os.path.join(directory_path, html_file)
        
        # Step 2: Read the HTML File
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        # Step 3: Parse the HTML and Extract Links
        soup = BeautifulSoup(html_content, 'html.parser')
        meta_tags = soup.find_all('meta', {'itemprop': 'url'})
        
        # Extracting the links from 'content' attribute of these meta tags
        extracted_links = [tag['content'] for tag in meta_tags if 'content' in tag.attrs]
        
        # Step 4: Apply filters and deduplicate
        # Filter by domain and exclude links with file extensions like .jpg
        filtered_links = [link for link in extracted_links if link.startswith('https://www.brasildefato.com.br/') and not link.endswith('.jpg')]
        
        all_links.extend(filtered_links)
    
    # Deduplicate links
    unique_links = list(set(all_links))
    print("Unique links " + str(len(unique_links)))
    # Step 5: Save Links to File
    with open(output_file, 'w', encoding='utf-8') as f:
        for link in unique_links:
            f.write(link + '\n')
            
input_path = "html-files"  # Replace with the path to your HTML file or directory
output_file = "unique_extracted_links-brasildefato.txt"  # Output file name
extract_links_from_directory(input_path, output_file)

