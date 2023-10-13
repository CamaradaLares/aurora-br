from bs4 import BeautifulSoup

def extract_unique_hrefs(file_path, output_file_path, target_domain):
    # Initialize an empty list to store the extracted HREFs
    extracted_hrefs = []

    # Read the HTML file
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract all the links by finding all 'a' tags and getting their 'href' attribute
    for link in soup.find_all('a'):
        href = link.get('href', '')
        if target_domain in href:
            extracted_hrefs.append(href)

    # Remove duplicates by converting the list to a set and then back to a list
    unique_hrefs = list(set(extracted_hrefs))

    # Save the final list to a text file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        for href in unique_hrefs:
            f.write(f"{href}\n")

    print(f"Extracted {len(unique_hrefs)} unique HREFs and saved them to {output_file_path}")

# Define file paths and target domain
file_path = 'final_page_opiniao.html'
output_file_path = 'unique_extracted_hrefs-opiniao.txt'
target_domain = 'https://operamundi.uol.com.br/opiniao/'

# Run the function
extract_unique_hrefs(file_path, output_file_path, target_domain)

