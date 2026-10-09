import requests
 
headers = {'User-Agent': 'data-eng-class-crawler/1.0 (learning purpose)'}
res = requests.get('https://quotes.toscrape.com/', headers=headers, timeout=10)
 
print('status:', res.status_code)
print('encoding:', res.encoding)
print('length:', len(res.text))
print(res.text[:400])
