import requests
from bs4 import BeautifulSoup
import os



# file = open("test.txt", mode='r', encoding='utf-8')
# file.close()
# video: view-source:https://bibliogram.snopyta.org/p/Bb46l8XFW4W/
# image: view-source:https://bibliogram.pussthecat.org/p/BzYObQyhCh1

# bib_url = "https://bibliogram.pussthecat.org"
bib_url = "https://bibliogram.org/"
feed = ""
address = os.getcwd()


def get_pic_links(site_url):
    # create response object
    r = requests.get(site_url)
    
    # create beautiful-soup object
    soup = BeautifulSoup(r.content,'html.parser')
    
    # find all links on web-page
    links = soup.findAll('img')
    
    # filter the link sending with .jpg
    pic_links = []
    for link in links:
        if (("user" not in link['src']) and ("jpg" in link['src'])):
            a_link = bib_url + link['src']
            pic_links.append(a_link)
    
    return pic_links


def get_video_links(site_url):
    # create response object
    r = requests.get(site_url)
    
    # create beautiful-soup object
    soup = BeautifulSoup(r.content,'html.parser')
    
    # find all links on web-page
    links = soup.findAll('video')
    
    # filter the link sending with .mp4
    video_links = []
    for link in links:
        if ("mp4" in link['src']):
            a_link = bib_url + link['src']
            video_links.append(a_link)
    
    return video_links


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
    return


def download_pic_series(total_pics, pic_links):
    count = 1
    str_ct = str(count)
    
    '''
    The syntax of python os.mkdir() function is:
    
    os.mkdir(path, mode=0o777, *, dir_fd=None)
    
    where path is the directory location to be created and mode is the
    file permissions to be assigned while creating the directory.
    '''
    feed = "pictures"
    
    # will return 'feed/address'
    # dir_path = os.path.join(feed, address)
    
    # create directory [current_path]
    # os.makedirs(dir_path)
    # output = open(os.path.join(dir_path, file_name), 'wb')
    
    # https://pythonexamples.org/python-create-directory-mkdir/#5
    # https://stackoverflow.com/questions/7935972/writing-to-a-new-directory-in-python-without-changing-directory
    # https://www.programiz.com/python-programming/directory
    
    
    # https://pythonprogramminglanguage.com/python-self/
    
    
    for link in pic_links:
        '''iterate through all links in pic_links
        and download them one by one'''
        
        file_name = "picture" + str(total_pics + count) + ".jpg"
        print("Downloading file: %s"%file_name)
        
        # create response object
        r = requests.get(link, stream = True)
        
        # open(file_name, 'wb')
        
        # download started
        # open(os.path.join(dir_path, file_name), 'wb')
        
        with open(file_name, 'wb') as file:
            for chunk in r.iter_content(chunk_size = 1024*1024):
                if chunk:
                    file.write(chunk)
        
        print("%s downloaded!"%file_name)
        count += 1
    
    print ("\nAll pictures downloaded!\n\n")
    return


def num_times_visited(total, func_name):
    if (total == 1):
        print(name_func + " visited 1 time")
    else:
        print(name_func + " visited " + str(total) + " times")
    
    return


if __name__ == "__main__":
    filename = input("Enter a filename: ")
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
    
    
    