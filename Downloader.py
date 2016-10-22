import os
import pafy
import urllib
import urllib2
import json
from bs4 import BeautifulSoup



def mycb(total, recvd, ratio, rate, eta):
        print(recvd, ratio, eta)

def downloadSong(url, title):
        usock = urllib2.urlopen(url)
        print ('info: ', usock.info())
        f = open(title, "wb")
        try :
                file_size = int(usock.info().getheaders("Content-Length")[0])
                print ('Downloading : %s Bytes: %s' % (title, file_size))
        except IndexError:
                print ('Unknown file size: index error')

        downloaded = 0
        block_size = 8192
        while True:
                buff = usock.read(block_size)
                if not buff:
                        break

                downloaded = downloaded + len(buff)
                f.write(buff)
        f.close()

while True: 
        video_ids = []
        video_titles = []
        print "Enter song name"
        song = str(raw_input())
        
        print "Searching for your song"

        query = urllib.quote(song)
        url = "https://www.youtube.com/results?search_query=" + query
        response = urllib2.urlopen(url)
        html_data = response.read()
        soup = BeautifulSoup(html_data)
        
        videos = soup.find_all("a",class_="yt-uix-tile-link")
        k=1
        if len(videos) == 0:
                print "Error, Continue Again"
                continue
 
        for vid in videos:
                print k,vid.text.encode("utf-8")
                k=k+1
                print "-----"
                video_titles.append(vid.string)
                video_ids.append("https://youtube.com" + str(vid['href']))

        print "Select your song to download"
        number = int(raw_input())

        print "1. Download Audio \n2. Download Video \n"
        selection = int(input())

        if selection == 1:
                os.chdir("/storage/emulated/0/Musicd") #Set path to save your audios
                BASE_URL = 'http://www.youtubeinmp3.com/fetch/?format=JSON&video='
                JSON_URL = BASE_URL + video_ids[number-1]
                print ('JSON URL : ' + JSON_URL)
                response = urllib.urlopen(JSON_URL)
                try:
                          data = json.loads(response.read()) #Json object
                          print (data)        
                          #Getting length, download url and title of song from json object
                          if 'length' not in data:
                                                raise ValueError("No length in given data")
                                                print ('No length in given data')
                                                break
                          if 'link' not in data:
                                                raise ValueError("No link in given data")
                                                print ('No link in given data')
                                                break
                          if 'title' not in data:
                                                raise ValueError("No title in given data")
                                                print ('No title in given data')
                                                break
                                
                          length = data['length'] 
                          print ('Length : ' + str(length))
                          DOWNLOAD_URL = data['link']
                          print ('DOWNLOAD_URL : ' + DOWNLOAD_URL)
                          video_titles[number-1] = video_titles[number-1].replace("|"," ") + ".mp3"
                          print video_titles[number-1]
                          downloadSong(DOWNLOAD_URL, video_titles[number-1])
                except ValueError:
                         print ('No song found')
        if selection == 2:
        	os.chdir("/storage/emulated/0/Videosd") #set path to save videos
         	p = pafy.new(video_ids[number-1])
        	j = 1
        	for i in p.streams:
        		print j,i
        		j = j + 1
        	print "select stream to download"
        	select = int(raw_input())
        	video = p.streams[select-1]
        	video.download(quiet=True,callback=mycb)