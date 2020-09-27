from bs4 import  BeautifulSoup
import urllib.request
import requests
import os
import datetime

def xtract_feed_book(link):
 for page in range(2,63):
     url=link+str(page)
     soup = BeautifulSoup(requests.get(url).text,'html.parser')
     files = soup.find_all('a', href=True)
     for file in files:
        urlink=file['href']
        if urlink[-5:]=='.epub':
            filename = urlink.split('/')[-1]
            if 'epub' in filename and os.path.isfile(filename) is False:
                  try:
                      print(datetime.datetime.now().time(),urlink.split('/')[-1],"downloading....")
                      urllib.request.urlretrieve(urlink,filename)
                      print(datetime.datetime.now().time(),urlink.split('/')[-1],"downloaded")
                  except:
                      print("Can't Download file")

print("Type your link whithout page number...")
link=input()
print("Extraction is processing...")
xtract_feed_book(link)



