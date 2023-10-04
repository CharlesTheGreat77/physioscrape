import requests, os, re
from argparse import ArgumentParser
from bs4 import BeautifulSoup
from bullet import Bullet

def get_contents_of_physio(search):
    url = f'https://physionet.org/content/?topic={search}'
    contents = requests.get(url).text
    soup = BeautifulSoup(contents, 'html.parser')

    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            text = link.get_text(strip=True)
            links.append((f'https://physionet.org{href}', text))

    urls = []
    descriptions = []
    for url, text in links:
        if 'content' in url:
            if 'topic' not in url:
                if 'Find' not in text:
                    urls.append(f'{url} ; Description: {text}')
                    descriptions.append(text)
    return urls, descriptions

def download_dataset(url):
    zip_file = re.search(r'/([^/]+\.zip)$', url)
    if zip_file:
        zip_file = zip_file.group(1)
    print(f'[*] Downloading zip file from {url}..')
    zip_request = requests.get(url)
    if zip_request.status_code == 200:
        print('[*] Download successful..')
        with open(f'{zip_file}', 'wb') as file:
            file.write(zip_request.content)
    else:
        print(f'[-] Error Downloading the file...\n')

def get_description_for_dataset(url):
    content = requests.get(url).text
    soup = BeautifulSoup(content, 'html.parser')
    headers = soup.find_all('h3')
    for header in headers:
        header_text = header.get_text().strip()
        next_element = header.find_next_sibling()
        if next_element:
            paragraph = next_element.get_text().strip()
            print(f'\033[92m{header_text}\033[0m\n\033[94m{paragraph}\033[0m')

    zip_file = soup.find_all('a', string="Download the ZIP file")
    file_size = soup.find('a', string='Download the ZIP file').next_sibling.strip()
    if zip_file:
        for link in zip_file:
            zip_url_download = link.get('href')
    
    print(f'https://physionet.net{zip_url_download} ; file size: {file_size}')
    return zip_url_download

def menu(question, options):
    cli = Bullet(
            prompt = question,
            choices = [option for option in options],
            indent = 0,
            align = 5,
            margin = 2,
            shift = 0,
            bullet = "",
            pad_right = 5,
            return_index = True
        )
    result = cli.launch()
    os.system('clear')
    return result[0]


if __name__=='__main__':
    parser = ArgumentParser(description='Query Physionet for datasets to analyze')
    parser.add_argument('-s', '--search', help='search by study name, general search, etc', type=str, required=True)
    args = parser.parse_args()
    search = args.search

    urls, descriptions = get_contents_of_physio(search)
    urls = set(urls)
    descriptions = set(descriptions)
    result = menu('\nChoose an Option:', urls)
    dataset = result.split(';')
    url = dataset[0]
    dataset_url = url.strip()
    print(dataset_url)
    zip_file_url = get_description_for_dataset(dataset_url)
    result = menu('\nDownload dataset [yes/no]?', ['yes', 'no'])
    if result != 'no':
        download_dataset(f'https://physionet.org{zip_file_url}')
        print("[*] Done..")
