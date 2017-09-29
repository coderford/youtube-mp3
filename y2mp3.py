#! /usr/bin/env python3
import requests
import argparse
import os
from bs4 import BeautifulSoup

# some options:
quiet = False
get_list = False

def conv_list_url(list_url):
    return list_url.replace(list_url[list_url.find('watch'):list_url.find('list')],'playlist?')

def make_search_soup(args): # args is a list of search keywords
    base_url_vid = "https://youtube.com/results?sp=EgIQAVAU&q=" # these might have to updated repeatedly
    base_url_list = "https://youtube.com/results?sp=EgIQA1AU&q="
    search_key = '+'.join(args)
    if get_list:
        url = base_url_list + search_key
    else: url = base_url_vid + search_key
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
        if 'watch' in href and 'list' not in href: # don't want playlists right now..
            vid_links.append((link.text, 'https://www.youtube.com'+href))
    return vid_links

def get_listlinks(soup):
    # extracting playlist links from soup and storing them into an array:
    list_links = []
    links = soup.findAll('a', {'class': 'yt-uix-tile-link'})
    for link in links:
        href = link.get('href')
        if 'watch' in href and 'list' in href:
            list_url = 'https://www.youtube.com'+href # ydl doesn't automatically download playlists with watchable links
            list_url = conv_list_url(list_url)
            list_links.append((link.text, list_url))
    return list_links

def dl_link(link, path=''):
    # lame system command:
    command = "youtube-dl -xwc --audio-format mp3 --audio-quality 0 --add-metadata --embed-thumbnail '{url}' ".format(url=link)
    if path!='':
        os.makedirs(path, exist_ok=True)
        command = command + "-o '{path}/%(title)s.%(ext)s'".format(path=path)
    os.system(command)


# parsing arguments:
parser = argparse.ArgumentParser(description='Script to search and download songs as mp3 from Youtube')
exclusive_group = parser.add_mutually_exclusive_group()
exclusive_group.add_argument('-s', '--search', nargs='+',    # nargs = '+' means 1 or more arguments is required
                    metavar = 'KEYWORD',
                    help='search and display results, and give option to download'
                   )
exclusive_group.add_argument('-l', '--lucky', nargs='+',
                    metavar = 'KEYWORD',
                    help='search and download the first search result'
                   )
exclusive_group.add_argument('url', nargs='?', help='url of song to be downloaded (optional)')  # nargs = '?' for optional argument
parser.add_argument('-p', '--playlist', action='store_true',
                    help='enable downloading playlist'
                   )
parser.add_argument('-d', '--dir', default='',metavar='DIRECTORY', help='output directory for downloads')
args = parser.parse_args()

# processing command:
if args.playlist:
    get_list = True;

if args.search :    # search and display result, then ask user which ones to download
    search_soup = make_search_soup(args.search)
    print('Search Results:')
    if get_list:
        list_links = get_listlinks(search_soup)
        for i,link in enumerate(list_links):
            print('\t'+str(i+1)+'.', link[0])
        print('Enter list numbers to download (0 to do nothing): ')
        to_download = [int(x) for x in input().split()]
        if to_download[0]==0:
            exit()
        for link_number in to_download:
            print('Now downloading: ', list_links[link_number-1][1])
            dl_link(list_links[link_number-1][1], args.dir)
    else:
        vid_links = get_vidlinks(search_soup)
        for i,link in enumerate(vid_links):
            print('\t'+str(i+1)+'.', link[0])
        print('Enter song numbers to download (0 to do nothing): ')
        to_download = [int(x) for x in input().split()]
        if to_download[0]==0:
            exit()
        for link_number in to_download:
            print('Now downloading playlist: ', vid_links[link_number-1][1])
            dl_link(vid_links[link_number-1][1], args.dir)

elif args.lucky:    # search and download the first search result
    print('Feeling lucky huh?')
    search_soup = make_search_soup(args.lucky)
    if get_list:
        list_links = get_listlinks(search_soup)
        print('Now downloading: ', list_links[0][0])
        dl_link(list_links[0][1], args.dir)
    else:
        vid_links = get_vidlinks(search_soup)
        print('Now downloading: ', vid_links[0][0])
        dl_link(vid_links[0][1], args.dir)

else:    # default behavior: download the url supplied
    if args.url == None:
        parser.print_help()
        exit()
    the_url = args.url
    if get_list:
        the_url  = conv_list_url(the_url)
    print('Now downloading: ', the_url)
    dl_link(the_url, args.dir)