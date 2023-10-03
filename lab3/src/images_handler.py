import os
import requests
import csv
import re
import pandas as pd

import directory_handler as dir_h

from bs4 import BeautifulSoup
from datetime import datetime

IMAGES_FIELDS = ['date', 'file_name', 'url']

class ImagesHandler:
    def __init__(self, curr_dir):
        self.CURR_DIR = curr_dir

    @staticmethod
    def write_csv_file(path: str, data: list) -> None:
        mode = 'w' if not os.path.exists(path) else 'a'
        with open(path, mode, newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(data)

    @staticmethod
    def parser_url(url: str) -> str:
        pattern = r'img_url=([^&]+)&text='
        match = re.search(pattern, url)

        if match:
            img_url_encoded = match.group(1)
            img_url_decoded = img_url_encoded.replace('%2F', '/').replace('%3A', ':')
            return img_url_decoded
        else:
            print('Ошибка: Ссылка после img_url не найдена в URL')
    
    @staticmethod
    def calc_pages(num_images: int) -> int:
        return num_images // 30 + (num_images % 30 > 0) if num_images > 30 else 1

    @staticmethod
    def get_html_tags(mini_images: bool) -> tuple[str, str, str]:
        if mini_images:
            return 'img', 'serp-item__thumb', 'src'
        else:
            return 'a', 'serp-item__link', 'href'

    @staticmethod
    def download_image(url: str, save_path: str) -> bool:
        try:
            response = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, stream=True)
            if(response.status_code == 200):
                with open(save_path, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                return True
            else:
                print(f'Ошибка: Не удалось загрузить изображение: {url}')
                return False
        except Exception as e:
            print(f'Ошибка {e}: при загрузке изображения: {url}')
            return False
        
    def download_images(self, query: str, num_images: int, mini_images: bool = False) -> None:
        pages = ImagesHandler.calc_pages(num_images)
        class_folder = dir_h.check_repository(self.CURR_DIR, f'datasets/images/{query}')

        downloaded_count = 0

        base_url = 'https:'

        csv_file_path = f'{self.CURR_DIR}/datasets/images/{query}_dataset.csv'
        ImagesHandler.write_csv_file(csv_file_path, IMAGES_FIELDS)
        tag, tag_class, tag_source = ImagesHandler.get_html_tags(mini_images)
        #а вот это чтобы без движков было, грузим странички
        for page in range(0, pages):
            search_url = f'https://yandex.ru/images/search?text={query}&p={page}'

            #сделал с with для автоматического закрытия соединения
            with requests.get(search_url, headers={'User-Agent':'Mozilla/5.0'}) as response:
                soup = BeautifulSoup(response.text, 'html.parser')

                for a in soup.find_all(tag, class_=tag_class):
                    img_url = a[tag_source]
                    # получаем полный URL изображения
                    if mini_images and not img_url.startswith('http'):
                        img_url = base_url + img_url
                    elif img_url.startswith('/images'):
                        img_url = ImagesHandler.parser_url(img_url)

                    #csv_image_filename = image_filename
                    image_filename = f'{downloaded_count:04d}.jpg'
                    image_path = os.path.join(class_folder, image_filename)
                    if(ImagesHandler.download_image(img_url, image_path)):
                        downloaded_count += 1
                        print(f'Загружено изображений для {query}: {downloaded_count}/{num_images}')

                        ImagesHandler.write_csv_file(csv_file_path, [datetime.now().strftime('%Y-%m-%d'), image_filename, img_url])

                    if(downloaded_count >= num_images):
                        break