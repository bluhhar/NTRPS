import os
import requests
from bs4 import BeautifulSoup
import re

def checkdataset():
    if not os.path.exists('dataset'):
        os.makedirs('dataset')

def parserurl(url):
    pattern = r'img_url=([^&]+)&text='
    match = re.search(pattern, url)

    if match:
        img_url_encoded = match.group(1)
        img_url_decoded = img_url_encoded.replace("%2F", "/").replace("%3A", ":")
        return img_url_decoded
    else:
        print("Ссылка после img_url не найдена в URL")

def download_image(url, save_path):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return True
        else:
            print(f"Не удалось загрузить изображение: {url}")
            return False
    except Exception as e:
        print(f"Ошибка при загрузке изображения: {url}")
        return False

def download_images(query, class_name, num_images=1000):
    class_folder = os.path.join('dataset', class_name)
    if not os.path.exists(class_folder):
        os.makedirs(class_folder)

    search_url = f"https://yandex.ru/images/search?text={query}"

    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    downloaded_count = 0

    for a in soup.find_all('a', class_='serp-item__link'):
        img_url = a['href']
        # Получаем полный URL изображения
        img_url = parserurl(img_url)
        image_filename = f"{downloaded_count:04d}.jpg"
        image_path = os.path.join(class_folder, image_filename)
        if download_image(img_url, image_path):
            downloaded_count += 1
            print(f"Загружено изображений для {class_name}: {downloaded_count}/{num_images}")

        if downloaded_count >= num_images:
            break

def main():
    checkdataset()
    #download_images("polar bear", "polar_bear", num_images=5)
    download_images("brown bear", "brown bear", num_images=5)


if __name__ == "__main__":
    main()