#! /usr/bin/env python3
'''
A script to search and download songs and playlists from youtube as mp3.
'''
import argparse
import json
import os
import re

import requests

# Some constants:
SEARCH_BASE_URL = "https://www.youtube.com/results?search_query="
VIDEO_BASE_URL = "https://www.youtube.com/watch?v="
LIST_BASE_URL = "https://www.youtube.com/playlist?list="

YDL_OPTIONS = ["-xwc",
               "--no-post-overwrites",
               "--audio-format mp3",
               "--audio-quality 0",
               "--add-metadata",
               "--embed-thumbnail",
               "--download-archive {path}/downloaded.txt",
               "-o '{path}/%(title)s.%(ext)s'"
              ]

# Functions
def conv_list_url(url):
    '''
    Converts watchable playlist link to a normal playlist link.
    '''
    if 'watch' in url:
        url = url.replace(url[url.find('watch'):url.find('list')], 'playlist?')
    return url

def get_search_data(args):
    '''
    Makes request, extracts JSON data, and traverses JSON tree to relevant part
    '''
    search_key = '+'.join(args)
    response = requests.get(SEARCH_BASE_URL + search_key).text

    re_search = re.findall(r"window\[\"ytInitialData\"\]\s*=\s*({.*});\s*window", response)
    if len(re_search) == 0:
        re_search = re.findall(r"var\s*ytInitialData\s*=\s*({.*});", response)
    jsontxt = re_search[0]

    data = json.loads(jsontxt)
    data = data.get("contents").get("twoColumnSearchResultsRenderer").\
                get("primaryContents").get("sectionListRenderer").\
                get("contents")[0].get("itemSectionRenderer").get("contents")
    return data

def get_vid_links(args):
    '''
    Makes a search and returns results as a list of dicts containing video titles and urls.
    '''
    search_data = get_search_data(args)

    vid_links = []
    for item in search_data:
        vrenderer = item.get("videoRenderer")
        if vrenderer is not None:
            vid_links.append({"title": vrenderer.get("title").get("runs")[0].get("text"),
                              "url": VIDEO_BASE_URL + vrenderer.get("videoId")})
    return vid_links

def get_list_links(args):
    '''
    Makes a search and returns results as a list of dicts containing playlist titles and urls.
    '''
    search_data = get_search_data(args)

    list_links = []
    for item in search_data:
        prenderer = item.get("playlistRenderer")
        if prenderer is not None:
            list_links.append({"title": prenderer.get("title").get("simpleText"),
                               "url": LIST_BASE_URL + prenderer.get("playlistId")})
    return list_links

def make_dl_command(url, path):
    '''
    Constructs system command for downloading a link.
    '''
    return ("youtube-dl "+" ".join(YDL_OPTIONS)+" "+url).format(path=path)

def dl_link(link, path=''):
    '''
    Runs system command to download a link.
    '''
    os.makedirs(path, exist_ok=True)

    command = make_dl_command(link, path)
    os.system(command)


if __name__ == "__main__":
    # Parse arguments:
    parser = argparse.ArgumentParser(description='Script to search and download songs as mp3 from Youtube')
    exclusive_group = parser.add_mutually_exclusive_group()
    exclusive_group.add_argument('-s', '--search', nargs='+',
                                 metavar='KEYWORD',
                                 help='search and display results, and give option to download'
                                )
    exclusive_group.add_argument('-l', '--lucky', nargs='+',
                                 metavar='KEYWORD',
                                 help='search and download the first search result'
                                )
    exclusive_group.add_argument('url', nargs='?', help='url of song to be downloaded (optional)')
    parser.add_argument('-p', '--playlist', action='store_true', help='enable downloading playlist')
    parser.add_argument('-d', '--dir', default='.', metavar='DIRECTORY', help='output directory for downloads')
    args = parser.parse_args()

    # Process command:
    if args.search:
        # search and display result, then ask user which ones to download
        print('Search Results:')
        if args.playlist:
            list_links = get_list_links(args.search)
            for i, link in enumerate(list_links):
                print('\t'+str(i+1)+'.', link["title"])
            print('Enter list numbers to download (0 to do nothing): ')
            to_download = [int(x) for x in input().split()]
            if to_download[0] == 0:
                exit()
            for link_number in to_download:
                print('Now downloading playlist: ', list_links[link_number-1]["title"])
                dl_link(list_links[link_number-1]["url"], args.dir)
        else:
            vid_links = get_vid_links(args.search)
            for i, link in enumerate(vid_links):
                print('\t'+str(i+1)+'.', link["title"])
            print('Enter song numbers to download (0 to do nothing): ')
            to_download = [int(x) for x in input().split()]
            if to_download[0] == 0:
                exit()
            for link_number in to_download:
                print('Now downloading: ', vid_links[link_number-1]["title"])
                dl_link(vid_links[link_number-1]["url"], args.dir)

    elif args.lucky:
        # search and download the first search result
        print('Feeling lucky huh?')
        if args.playlist:
            list_links = get_list_links(args.lucky)
            print('Now downloading: ', list_links[0]["title"])
            dl_link(list_links[0]["url"], args.dir)
        else:
            vid_links = get_vid_links(args.lucky)
            print('Now downloading: ', vid_links[0]["title"])
            dl_link(vid_links[0]["url"], args.dir)

    else:
        # default behavior: download the url supplied
        if args.url is None:
            parser.print_help()
            exit()
        if args.playlist:
            args.url = conv_list_url(args.url)
        print('Now downloading: ', args.url)
        dl_link(args.url, args.dir)
