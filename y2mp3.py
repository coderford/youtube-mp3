#! /usr/bin/env python3
import requests
import sys, getopt
from os import system
from bs4 import BeautifulSoup

def get_vidlinks(soup):
    # extracting video links from soup and storing them into an array:
    vid_links = []
    links = soup.findAll('a', {'class': 'yt-uix-tile-link'})
    for link in links:
        href = link.get('href')
        if 'watch' in href and 'list' not in href:
            vid_links.append([link.text, 'https://www.youtube.com/'+href])
    return vid_links

def dl_link(link):
    command = "youtube-dl --extract-audio --audio-format mp3 --audio-quality 0 '{url}'".format(url=link)
    system(command)


base_url = "https://youtube.com/results?search_query="
search_key = '+'.join(input("Enter search term: ").split(' '))
url = base_url + search_key
search_request = requests.get(url)
#print(search_request.status_code) # should be 200
search_soup = BeautifulSoup(search_request.text, 'html.parser')
vid_links = get_vidlinks(search_soup)


print('\n\nDownloading:', vid_links[0][0], '\n')
dl_link(vid_links[0][1])
