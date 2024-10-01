import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
import mimetypes
import re
import argparse
from tqdm import tqdm
import hashlib

def download_file(url, base_folder):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to download: {url}. Error: {e}")
        return None

    parsed_url = urlparse(url)
    filename = os.path.basename(unquote(parsed_url.path))
    if not filename:
        filename = 'index.html'
    
    content_type = response.headers.get('Content-Type', '').split(';')[0]
    extension = mimetypes.guess_extension(content_type) or os.path.splitext(filename)[1]
    if extension:
        file_type = extension[1:]
    else:
        file_type = 'other'
    
    subfolder = os.path.join(base_folder, file_type)
    os.makedirs(subfolder, exist_ok=True)
    
    # Use content hash to avoid duplicates
    content_hash = hashlib.md5(response.content).hexdigest()
    name, ext = os.path.splitext(filename)
    filepath = os.path.join(subfolder, f"{name}_{content_hash[:8]}{ext}")

    with open(filepath, 'wb') as f:
        f.write(response.content)
    return os.path.relpath(filepath, base_folder)

def update_html_links(soup, base_url, base_folder):
    tags_to_update = ['link', 'script', 'img', 'audio', 'video', 'source', 'track', 'embed', 'object', 'iframe', 'meta', 'a']
    attrs_to_update = ['href', 'src', 'data', 'poster', 'content']

    for tag in tqdm(soup.find_all(tags_to_update), desc="Updating HTML links"):
        for attr in attrs_to_update:
            if tag.has_attr(attr):
                # Special handling for meta tags
                if tag.name == 'meta' and attr == 'content':
                    if tag.get('property') in ['og:image', 'og:audio', 'og:video', 'twitter:image']:
                        url = urljoin(base_url, tag[attr])
                        new_path = download_file(url, base_folder)
                        if new_path:
                            tag[attr] = new_path
                # Special handling for anchor tags
                elif tag.name == 'a' and attr == 'href':
                    url = urljoin(base_url, tag[attr])
                    parsed_url = urlparse(url)
                    if parsed_url.netloc == urlparse(base_url).netloc:
                        new_path = download_file(url, base_folder)
                        if new_path:
                            tag[attr] = new_path
                else:
                    url = urljoin(base_url, tag[attr])
                    new_path = download_file(url, base_folder)
                    if new_path:
                        tag[attr] = new_path

    for tag in tqdm(soup.find_all(style=True), desc="Updating inline styles"):
        style = tag['style']
        urls = re.findall(r'url\(["\']?([^)"\']+)["\']?\)', style)
        for url in urls:
            full_url = urljoin(base_url, url)
            new_path = download_file(full_url, base_folder)
            if new_path:
                style = style.replace(url, new_path)
        tag['style'] = style

    for style in tqdm(soup.find_all('style'), desc="Updating style tags"):
        css_content = style.string
        if css_content:
            urls = re.findall(r'url\(["\']?([^)"\']+)["\']?\)', css_content)
            for url in urls:
                full_url = urljoin(base_url, url)
                new_path = download_file(full_url, base_folder)
                if new_path:
                    css_content = css_content.replace(url, new_path)
            style.string = css_content

def scrape_website(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to access the website: {url}. Error: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    domain = urlparse(url).netloc
    base_folder = f"{domain}_files"
    os.makedirs(base_folder, exist_ok=True)
    
    update_html_links(soup, url, base_folder)
    
    index_path = os.path.join(base_folder, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"Scraping completed! Files saved in: {os.path.abspath(base_folder)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape a website and download its resources.")
    parser.add_argument("url", help="The URL of the website to scrape")
    args = parser.parse_args()

    scrape_website(args.url)