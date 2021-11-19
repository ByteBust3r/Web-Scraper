import string
import requests
import os

from bs4 import BeautifulSoup

# Get all necessary user input
num_pages = int(input())
art_type = input()

for i in range(1, num_pages + 1):
    os.mkdir(f'Page_{i}')
    url = f'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={i}'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    articles = soup.findAll('article')
    for article in articles:
        if article.find('span', attrs={'class': 'c-meta__type'}).text == art_type:
            a = article.find('a')
            suburl = a['href']
            r_new = requests.get(f'https://nature.com{suburl}')
            soup_new = BeautifulSoup(r_new.content, 'html.parser')
            # Get article title
            title = soup_new.find('title').text
            title = title.translate(str.maketrans('', '', string.punctuation))
            title = title.replace(' ', '_')
            print(title)
            # Get article body
            c_article_body = soup_new.find('div', {'class': 'c-article-body'})
            body = c_article_body.text.strip()
            body = body.replace("\n", "")
            # Create text file
            save_path = f'{os.getcwd()}/Page_{i}'
            file_name = f"{title}.txt"
            completeName = os.path.join(save_path, file_name)
            print(completeName)
            file = open(completeName, 'w', encoding='UTF-8')
            file.write(body)
            os.path.join(f'Page_{i}', f'{title}.txt')
            file.close()


