import requests
from bs4 import BeautifulSoup
import os



# video example: view-source:https://bibliogram.org/p/BzLwtk4hjQm/
# image example: view-source:https://bibliogram.org/p/BzYObQyhCh1

# bib_url = "https://bibliogram.pussthecat.org"
bib_url = "https://bibliogram.org"
feed = ""
address = os.getcwd()


'''
Returns a list of links to .jpg
images in the given webpage

@param site_url A given website URL
@return .jpg images in webpage
'''
def get_pic_links(site_url):
    # create response object
    r = requests.get(site_url)
    
    # create beautiful-soup object
    soup = BeautifulSoup(r.content,'html.parser')
    
    # find all images on web-page
    links = soup.findAll('img')
    
    # filter the link sending with .jpg
    pic_links = []
    for link in links:
        if (("user" not in link['src']) and ("jpg" in link['src'])):
            a_link = bib_url + link['src']
            pic_links.append(a_link)
    
    return pic_links


'''
Returns a list of links to .mp4
videos in the given webpage

@param site_url A given website URL
@return .mp4 videos in webpage
'''
def get_video_links(site_url):
    # create response object
    r = requests.get(site_url)
    
    # create beautiful-soup object
    soup = BeautifulSoup(r.content,'html.parser')
    
    # find all videos on web-page
    links = soup.findAll('video')
    
    # filter the link sending with .mp4
    video_links = []
    for link in links:
        if ("mp4" in link['src']):
            a_link = bib_url + link['src']
            video_links.append(a_link)
    
    return video_links


'''
Given a list of URLs to videos,
download them to the current
directory. Uses a simple numbering
convention to name the videos
based on the order in which the
videos were downloaded

@precondition The videos are .mp4 files
@param total_vids Total number of videos
@param video_links Links to .mp4 videos
'''
def download_video_series(total_vids, video_links):
    count = 1
    str_ct = str(count)
    
    for link in video_links:
        '''iterate through all links in video_links
        and download them one by one'''
        
        file_name = "video" + str(total_vids + count) + ".mp4"
        print("Downloading file: %s"%file_name)
        
        # create response object
        r = requests.get(link, stream = True)
        
        # download started
        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size = 1024*1024):
                if chunk:
                    f.write(chunk)
        
        print("%s downloaded!"%file_name)
        count += 1
    
    print ("\nAll videos downloaded!\n\n")


'''
Given a list of URLs to images,
download them to the current
directory. Uses a simple numbering
convention to name the images
based on the order in which the
images were downloaded

@precondition The images are .jpg files
@param total_pics Total number of images
@param pic_links Links to .jpg images
'''
def download_pic_series(total_pics, pic_links):
    count = 1
    str_ct = str(count)
    for link in pic_links:
        '''
        iterate through all links in pic_links
        and download them one by one
        '''
        file_name = "picture" + str(total_pics + count) + ".jpg"
        print("Downloading file: %s"%file_name)
        
        # create response object
        r = requests.get(link, stream = True)
        
        with open(file_name, 'wb') as file:
            for chunk in r.iter_content(chunk_size = 1024*1024):
                if chunk:
                    file.write(chunk)
        
        print("%s downloaded!"%file_name)
        count += 1
    
    print ("\nAll pictures downloaded!\n\n")


'''
Indicates the number of times
a function was visited

@param total The total number of visits
@param func_name The function invoked
'''
def num_times_visited(total, func_name):
    if (total == 1):
        print(func_name + " visited 1 time")
    else:
        print(func_name + " visited " + str(total) + " times")


'''
Executes the instagram scraper
'''
if __name__ == "__main__":
    filename = input("Enter a filename or link: ")
    # filename = "instagram.txt"
    # filename = "instagram2.txt"
    list_vids = []
    list_pics = []
    total_vids = 0
    visits_vids = 0
    
    total_pics = 0
    visits_pics = 0
    
    
    if (filename == "exit"):
        exit()
    
    '''
    For downloading content from a single post
    '''
    if ("https" in filename):
        items = filename.split('/')
        link = bib_url + "/p/" + items[4]
        #list_vids = get_video_links(link)
        #num_vids = len(list_vids)
        #if (num_vids > 0):
        #    download_video_series(total_vids, list_vids)
        #    total_vids += num_vids
        #    visits_vids += 1
        #    num_times_visited(visits_vids, name_func)
        
        name_func = "download_pic_series()"
        list_pics = get_pic_links(link)
        num_pics = len(list_pics)
        if (num_pics > 0):
            download_pic_series(total_pics, list_pics)
            total_pics += num_pics
            visits_pics += 1
            num_times_visited(visits_pics, name_func)
        exit()
        
    
    file = open(filename, mode='r', encoding='utf-8')
    
    '''
    For downloading content from several posts
    '''
    for line in file:
        if "instagram.com" in line:
            items = line.split('/')
            link = bib_url + "/p/" + items[4]
            
            name_func = "download_video_series()"
            list_vids = get_video_links(link)
            num_vids = len(list_vids)
            if (num_vids > 0):
                download_video_series(total_vids, list_vids)
                total_vids += num_vids
                visits_vids += 1
                num_times_visited(visits_vids, name_func)
            
            name_func = "download_pic_series()"
            list_pics = get_pic_links(link)
            num_pics = len(list_pics)
            if (num_pics > 0):
                download_pic_series(total_pics, list_pics)
                total_pics += num_pics
                visits_pics += 1
                num_times_visited(visits_pics, name_func)
    
    
    file.close()
    
    
    