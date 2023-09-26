import os
import requests
import re

from bs4 import BeautifulSoup

#путь .py
CURR_DIR = os.path.dirname(os.path.abspath(__file__))

def check_dataset():
    dataset_directory = os.path.join(CURR_DIR, 'dataset')
    if not os.path.exists(dataset_directory):
        os.makedirs(dataset_directory)

def check_repo_dataset(class_name):
    class_folder = os.path.join(CURR_DIR + '\dataset', class_name)
    if not os.path.exists(class_folder):
        os.makedirs(class_folder)
        return class_folder
    else:
        return class_folder

def parser_url(url):
    pattern = r'img_url=([^&]+)&text='
    match = re.search(pattern, url)

    if match:
        img_url_encoded = match.group(1)
        img_url_decoded = img_url_encoded.replace('%2F', '/').replace('%3A', ':')
        return img_url_decoded
    else:
        print('Ссылка после img_url не найдена в URL')

def calc_pages(num_images):
    return num_images // 30 + (num_images % 30 > 0) if num_images > 30 else 1

def get_html_tags(mini_images):
    if mini_images:
        return 'img', 'serp-item__thumb', 'src'
    else:
        return 'a', 'serp-item__link', 'href'

def download_image(url, save_path):
    try:
        response = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, stream=True)
        if(response.status_code == 200):
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
    pages = calc_pages(num_images)
    class_folder = check_repo_dataset(query)

    downloaded_count = 0

    base_url = 'https:'

    #а вот это чтобы без движков было, грузим странички
    for page in range(0, pages):
        search_url = f'https://yandex.ru/images/search?text={query}&p={page}'
        
        #сделал с with для автоматического закрытия соединения
        with requests.get(search_url, headers={'User-Agent':'Mozilla/5.0'}) as response:
            soup = BeautifulSoup(response.text, 'html.parser')

            tag, tag_class, tag_source = get_html_tags(mini_images)

            for a in soup.find_all(tag, class_=tag_class):
                img_url = a[tag_source]
                # получаем полный URL изображения
                if mini_images and not img_url.startswith('http'):
                    img_url = base_url + img_url
                elif img_url.startswith('/images'):
                    img_url = parser_url(img_url)

                image_filename = f'{downloaded_count:04d}.jpg'
                image_path = os.path.join(class_folder, image_filename)
                if(download_image(img_url, image_path)):
                    downloaded_count += 1
                    print(f"Загружено изображений для {query}: {downloaded_count}/{num_images}")

                if(downloaded_count >= num_images):
                    break

def main():
    check_dataset()
    #download_images('polar bear', num_images = 5, mini_images = True)
    #download_images('Артас Король-лич', num_images = 5, mini_images = True)
    #download_images('brown bear', num_images = 5, mini_images = True)
    download_images('Серый медведь', 5, False)
    download_images('Белый медведь', 5, True)

if __name__ == '__main__':
    main()