import os
import requests

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

def download_reviews(num_reviews, star_rating):
    pages = 2
    search_url = f'https://www.livelib.ru/reviews/~{pages}#reviews'
    response = requests.get(search_url, headers={'User-Agent':'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')
    for review in soup.find_all('article', class_='review-card lenta__item'):
        rating_span = review.find('span', class_='lenta-card__mymark')
        if rating_span:
            rating = rating_span.text
            print("rating", rating)
        else: #нехорошие люди не ставят рейтинг книги
            print("rating not found")

         

def main():
    check_dataset()
    download_reviews(2, 1)

if __name__ == '__main__':
    main()