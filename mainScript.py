from bs4 import BeautifulSoup
import re
import urllib.request
import requests
import os



contentType = ""
block = False



def getImageURL(url):
    global contentType
    global block

    try:
        urllib.request.urlopen(url)
    except urllib.error.URLError:
        block = True
        return False
    
    data = urllib.request.urlopen(url).read()

    soup = BeautifulSoup(data, "html.parser")
    img = soup.find(id="main_image")
    
    contentType = getImageRating(data,soup)
    
    return img.get('src')



def checkForDisgustingTags(data,stringToCheck):
    matches = re.findall(stringToCheck, str(data));
    if len(matches) == 0: 
       return False
    else:
       return True


def getImageRating(data,soup):
    global block
    
    de = soup.find_all('tr')

    for item in de:
        if not (item.th==None):
            if(item.th.string=='Rating'):
                contentType = item.td.string.replace("	", "").replace("\n", "")

                if not(contentType=='Explicit'):
                    block=False
                
                return contentType
            
            elif(item.th.string=='Tags'):
                if not (item.td==None):
                    stringsToIgnore=['loli','underage']
                    boolean = False
                    for x in stringsToIgnore:
                        if(checkForDisgustingTags(str(item.td),x)==True):
                            boolean = True

                    if boolean==True:
                        block = True



print("Please input the index to start the download at")
startID = input("Start index: ")

print("Please input the index to end the download at")
endID = input("End index: ")




url = "https://neko-booru.com/post/view/"
baseURL = 'https://neko-booru.com'



getImageURL(url+"1")

for x in range(int(startID),int(endID)+1):
    block = False
    urlToLoad = getImageURL(url+str(x))

    if(block==True):
        print("Index "+str(x)+" being ignored ")
    else:
        f = open(os.getcwd()+"/content/"+contentType+"_"+str(x)+".jpeg",'wb')
        
        str2 = (url+str(x)+".jpg")
        
        f.write(requests.get(baseURL+urlToLoad).content)
        f.close()
        
        print("Index "+str(x)+" complete! ")








    
