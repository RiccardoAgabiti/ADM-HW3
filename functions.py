import asyncio
import requests
from bs4 import BeautifulSoup
import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool
import pathlib
from pathlib import Path

"""
============================================================================================================

    html pages download functions

============================================================================================================

"""

def save_html_animePage(url, directoryNum, index):
    # Get current page
    req = requests.get(url)
    
    # MyAnimeList might stop the connection due to the numbers of request
    if(req.status_code != 200) : 
        raise Exception(f"Web site have closed the connection.\nRestart the process from page: {(index//50)}")
    
    # get the path where to place the file
    save_path = f"{pathlib.Path().resolve()}/animeList_pages/{directoryNum}th_page"
    Path(save_path).mkdir(parents=True, exist_ok=True)
    
    # Write the file in the directory.
    with open(f"{save_path}/article_{index}.html", 'w') as file:
        file.write(req.text)
    

def save_html_AnimePage_In_ListAnimePage(urls, folderNumber, CPUs = multiprocessing.cpu_count()):
    pool = ThreadPool(CPUs)
    pool.map(lambda url : save_html_animePage(url, folderNumber, (50*(folderNumber-1)) + urls.index(url) +1), urls)


def get_listAnimePage(index, listPages):
    listPages[index] = requests.get(f"https://myanimelist.net/topanime.php{'?limit={}'.format(50*index)}")



def get_urls_In_ListAnimePage(page, pages):
    
    soup = BeautifulSoup(page.content, "html.parser")
    
    # Find all links of the animes
    Urls = soup.find_all("a", class_="hoverinfo_trigger fl-l ml12 mr8", id=lambda string: string and string.startswith('#area'), href=True)
    
    #get just the href
    animeLinks = []
    for link in Urls:
        link_anime = str(link.get("href"))
        animeLinks.append(link_anime)
    
    pages[pages.index(page)] = animeLinks
    
    
def initGet(pageToGet = 400 ,CPUs = multiprocessing.cpu_count()):

    pages = [None] * pageToGet
    numberOfPage = range(0, pageToGet)

    pool = ThreadPool(CPUs)
    pool.map(lambda num : get_listAnimePage(num, pages), numberOfPage)   
    pool.map(lambda page : get_urls_In_ListAnimePage(page, pages), pages)
    
    return pages


def getAnime(pages, start=0):
    pages_from_start_to_end = pages[start:]
    for i in range(0, len(pages_from_start_to_end)) : 
        save_html_AnimePage_In_ListAnimePage(pages_from_start_to_end[i], start+i+1)