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

def parse_rating(str):
    str = re.search(r'\d+', str)
    if str:
        number = str.group()
        return number
    else:
        return 0

def download_reviews(num_reviews, star_rating, full_mode = False):
    pages = 2
    search_url = f'https://www.livelib.ru/reviews/~{pages}#reviews'
    response = requests.get(search_url, headers={'User-Agent':'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')
    for review in soup.find_all('div', class_='lenta-card'):
        rating_tag = review.find('span', class_='lenta-card__mymark')
        title_tag = review.find('h3', class_='lenta-card__title')
        link = title_tag.find('a')['href']
        title = title_tag.find('a').text
        rating = rating_tag.text
        rating = parse_rating(rating)
        
        text_escaped_tag = review.find('div', id='lenta-card__text-review-escaped')
        text = text_escaped_tag.text

        print('rating', rating)
        print('title', title)
        print('link', link)
        print('text', text)

        break

def main():
    check_dataset()
    download_reviews(2, 1)

if __name__ == '__main__':
    main()