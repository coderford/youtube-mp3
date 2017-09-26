import requests
from bs4 import BeautifulSoup

base_url = "https://youtube.com/results?search_query="
current_page = 0


search_key = '+'.join(input("Enter song name: ").split(' '))
url = base_url + search_key

search_request = requests.get(url)

print(search_request.status_code) #200
#print(search_request.text)

search_soup = BeautifulSoup(search_request.text, 'html.parser')

links = search_soup.findAll('a', {'class': 'spf-link'})
for link in links:
    if 'watch' in link.get('href'):
        print('https://www.youtube.com/'+link.get('href'))
