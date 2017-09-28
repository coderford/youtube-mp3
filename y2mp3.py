#! /usr/bin/env python3
import requests
import argparse
from os import system
from bs4 import BeautifulSoup

def make_search_soup(args): # args is a list of search keywords
    base_url = "https://youtube.com/results?search_query="
    search_key = '+'.join(args)
    url = base_url + search_key
    search_request = requests.get(url)
    #print(search_request.status_code) # should be 200
    search_soup = BeautifulSoup(search_request.text, 'html.parser')
    return search_soup

def get_vidlinks(soup):
    # extracting video links from soup and storing them into an array:
    vid_links = []
    links = soup.findAll('a', {'class': 'yt-uix-tile-link'})
    for link in links:
        href = link.get('href')
        if 'watch' in href and 'list' not in href: # don't want playlists right now...
            vid_links.append([link.text, 'https://www.youtube.com/'+href])
    return vid_links

def dl_link(link):
    # lame system command:
    command = "youtube-dl --extract-audio --audio-format mp3 --audio-quality 0 '{url}'".format(url=link)
    system(command)


# parsing arguments:
parser = argparse.ArgumentParser(description='Script to search and download songs as mp3 from Youtube')
parser.add_argument('-s', '--search', nargs='+',    # nargs = '+' means 1 or more arguments is required
                    metavar = 'KEYWORD',
                    help='search and display results, and give option to download'
                   )
parser.add_argument('-l', '--lucky', nargs='+',
                    metavar = 'KEYWORD',
                    help='search and download the first search result'
                   )
parser.add_argument('url', nargs='?', help='url of song to be downloaded (optional)')  # nargs = '?' is used to make positional arg optional
args = parser.parse_args()

# processing command:

if args.search :    # search and display result, then ask user which ones to download
    search_soup = make_search_soup(args.search)
    vid_links = get_vidlinks(search_soup)
    print('Search Results:')
    for i,link in enumerate(vid_links):
        print('\t'+str(i+1)+'.', link[0])
    print('Enter song numbers to download (0 to do nothing): ')
    to_download = [int(x) for x in input().split()]
    if to_download[0]==0:
        exit()
    for song_number in to_download:
        print('Now downloading: ', vid_links[song_number-1][0])
        dl_link(vid_links[song_number-1][1])

elif args.lucky:    # search and download the first search result
    search_soup = make_search_soup(args.lucky)
    vid_links = get_vidlinks(search_soup)
    print('Feeling lucky huh?')
    print('Now downloading: ', vid_links[0][0])
    dl_link(vid_links[0][1])

else:    # default behavior: download the url supplied
    if args.url == None:
        parser.print_help()
        exit()
    print('Now downloading: ', args.url)
    dl_link(args.url)
