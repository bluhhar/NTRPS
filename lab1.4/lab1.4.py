import os
import requests
from bs4 import BeautifulSoup
import re

def checkdataset():
    if not os.path.exists('dataset'):
        os.makedirs('dataset')


def checkrepodataset(class_name):
    class_folder = os.path.join('dataset', class_name)
    if not os.path.exists(class_folder):
        os.makedirs(class_folder)
        return class_folder
    else:
        return class_folder

def parserurl(url):
    pattern = r'img_url=([^&]+)&text='
    match = re.search(pattern, url)

    if match:
        img_url_encoded = match.group(1)
        img_url_decoded = img_url_encoded.replace('%2F', '/').replace('%3A', ':')
        return img_url_decoded
    else:
        print('Ссылка после img_url не найдена в URL')

def download_image(url, save_path):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return True
        else:
            print(f'Не удалось загрузить изображение: {url}')
            return False
    except Exception as e:
        print(f'Ошибка при загрузке изображения: {url}')
        return False

def download_images(query, num_images, mini_images = False):
    class_folder = checkrepodataset(query)
    search_url = f'https://yandex.ru/images/search?text={query}'
    
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    downloaded_count = 0

    base_url = 'https:'

    if (mini_images == False):
        for a in soup.find_all('a', class_='serp-item__link'):
            img_url = a['href']
            # Получаем полный URL изображения
            img_url = parserurl(img_url)
            image_filename = f"{downloaded_count:04d}.jpg"
            image_path = os.path.join(class_folder, image_filename)
            if download_image(img_url, image_path):
                downloaded_count += 1
                print(f"Загружено изображений для {query}: {downloaded_count}/{num_images}")

            if downloaded_count >= num_images:
                break
    else:
        for a in soup.find_all('img', class_='serp-item__thumb'):
            img_url = a['src']
            # из за получение //avatar, надо бы добавить https:// чтобы ссылка стала полной
            if not img_url.startswith('http'):
                img_url = base_url + img_url
                image_filename = f'{downloaded_count:04d}.jpg'
                image_path = os.path.join(class_folder, image_filename)
                if download_image(img_url, image_path):
                    downloaded_count += 1
                    print(f'Загружено изображений для {query}: {downloaded_count}/{num_images}')

                if downloaded_count >= num_images:
                    break

def main():
    checkdataset()
    download_images('polar bear', num_images = 5, mini_images = True)
    download_images('brown bear', num_images = 5, mini_images = True)

if __name__ == '__main__':
    main()