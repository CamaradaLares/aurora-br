import os
from bs4 import BeautifulSoup

# Function to read and parse HTML file
def read_and_parse_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    h1_elements = soup.find_all('h1', {'class': 'elementor-heading-title elementor-size-default'})
    links = [h1.find('a', href=True)['href'] for h1 in h1_elements if h1.find('a', href=True)]
    return links

# Function to handle multiple files or a directory
def process_files_or_directory(input_path, output_file):
    all_links = []
    if os.path.isdir(input_path):
        for filename in os.listdir(input_path):
            #if filename.endswith('.html'):
            file_path = os.path.join(input_path, filename)
            all_links.extend(read_and_parse_html(file_path))
    else:
        all_links.extend(read_and_parse_html(input_path))
    
    # Deduplicate links
    unique_links = list(set(all_links))
    
    # Save unique links to a file
    with open(output_file, 'w') as file:
        for link in unique_links:
            file.write(f"{link}\n")

if __name__ == "__main__":
    input_path = "html-files"  # Replace with the path to your HTML file or directory
    output_file = "unique_extracted_links-novademocracia.txt"  # Output file name
    process_files_or_directory(input_path, output_file)

