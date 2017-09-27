import requests
from os import system
from bs4 import BeautifulSoup
from youtube_dl import YoutubeDL

base_url = "https://youtube.com/results?search_query="

search_key = '+'.join(input("Enter search term: ").split(' '))
url = base_url + search_key

search_request = requests.get(url)

print(search_request.status_code) #200
#print(search_request.text)

search_soup = BeautifulSoup(search_request.text, 'html.parser')

vid_links = []
links = search_soup.findAll('a', {'class': 'yt-uix-tile-link'})
for link in links:
    href = link.get('href')
    #print(href)
    if 'watch' in href and 'list' not in href:
        vid_links.append([link.text, 'https://www.youtube.com/'+href])

for link in vid_links:
    print(link[0])
    print('\t',link[1])

print('\n\nDownloading:', vid_links[0][1])
command = "youtube-dl --extract-audio --audio-format mp3 --audio-quality 0 '{url}'".format(url=vid_links[0][1])
system(command)

