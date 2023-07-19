import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_images(url, folder_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for invalid HTTP responses
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to the website: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    img_tags = soup.find_all('img')

    for img in img_tags:
        img_url = img.get('src')
        if img_url:
            img_url = urljoin(url, img_url)
            try:
                img_name = os.path.join(folder_path, os.path.basename(img_url))
                img_response = requests.get(img_url)
                img_response.raise_for_status()  # Raise an exception for invalid HTTP responses
                with open(img_name, 'wb') as img_file:
                    img_file.write(img_response.content)
                print(f"Downloaded: {img_name}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to download {img_url}: {e}")
            except OSError as e:
                print(f"Failed to save {img_url}: {e}")

if __name__ == "__main__":
    website_url = "YOUR_WEBSITE_URL_HERE"
    save_folder = "YOUR_SAVE_FOLDER_PATH_HERE"

    download_images(website_url, save_folder)
