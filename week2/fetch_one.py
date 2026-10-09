import requests
from bs4 import BeautifulSoup
 
headers = {'User-Agent': 'data-eng-class-crawler/1.0 (learning purpose)'}
res = requests.get('https://quotes.toscrape.com/', headers=headers, timeout=10)
print('status:', res.status_code)
 
soup = BeautifulSoup(res.text, 'html.parser')
for q in soup.select('div.quote'):
    text = q.select_one('span.text').get_text(strip=True)
    author = q.select_one('small.author').get_text(strip=True)
    tags = [t.get_text(strip=True) for t in q.select('a.tag')]
    print(author, '|', text[:30], '|', tags)