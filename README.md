## A command line utility to search and download songs from Youtube

Basically a wrapper around youtube-dl to enable easy searching and downloading songs from youtube in mp3 format.

Requires beautifulSoup4, youtube-dl with python3 and ffmpeg

### Usage
`y2mp3.py [-h] [-s KEYWORD [KEYWORD ...]] [-l KEYWORD [KEYWORD ...]][url]`

#### Positional arguments:
  **url**: url of song to be downloaded (optional)              
  
  use for simply downloading a url
#### Optional arguments:
  `-s KEYWORD [KEYWORD ...], --search KEYWORD [KEYWORD ...]`
  
   search and display results, and give option to download
   
  `-l KEYWORD [KEYWORD ...], --lucky KEYWORD [KEYWORD ...]`
  
   search and download the first search result
#### Examples:
**Downloading a url:**

`y2mp3.py <url>`

**Download the first search hit:**

`y2mp3.py KEYWORD1 KEYWORD2 ...`