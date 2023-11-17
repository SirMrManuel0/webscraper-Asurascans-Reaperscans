import requests
from bs4 import BeautifulSoup
import googlesearch
import json
import re
import html
import sys
try:
    from scripts import download
except:
    ...

with open('config.json', 'r', encoding="utf-8") as config_file:
    config = json.load(config_file)

# Extract the headers from the configuration
HEADERS = config.get("headers", {})

def google_search(query:str, amount = 1):
    """
    Perform a Google Custom Search and retrieve search results.

    Args:
        query (str): The search query.
        amount (int, optional): The number of search results to retrieve (default is 1).

    Returns:
        list: A list of search results.
    """
    
    # Send a GET request to Google
    url = f"https://www.google.com/search?q={query}"
    response = googlesearch.search(query, tld="co.in", num=amount, stop=amount, pause=2)
    results = []
    
    for link in response:
        results.append(link)
    return results


def search_asurascans(query:str):
    """
    Perform a search for a certain manga / manhua / manhwa on AsuraScans.
    
    Args:
        query (str): The name.
        
    Returns:
        dict: A dictonary of results (name: url).
    """
    # Read JSON file data
    with open("scripts/search_asura_cache.json", 'r', encoding="utf-8") as json_file:
        data_asura = json.load(json_file)
    
    
    
    temp_dict = data_asura.copy()
    
    # Filter comics by query
    for k,i in temp_dict.items():
        if k.lower().find(query.lower()) < 0:
            data_asura.pop(k)
    
    return data_asura


def search_reaperscans(query:str):
    """
    Search for comics on the ReaperScans website and filter by a given query.

    Args:
    query (str): The query to filter comics by.

    Returns:
    dict: A dictionary of comic names and their corresponding URLs.
    """
    # Read JSON file data
    with open("scripts/search_reaper_cache.json", 'r', encoding="utf-8") as json_file:
        data_reaper = json.load(json_file)
    
    
    
    temp_dict = data_reaper.copy()
    
    # Filter comics by query
    for k,i in temp_dict.items():
        if k.lower().find(query.lower()) < 0:
            data_reaper.pop(k)
    
    return data_reaper
    
def update_reaper_cache():
    """
    Update the cache of comic data for the Reaperscans website.

    This function fetches and stores a list of comics and their URLs from the Reaperscans website.
    The data is saved in a JSON file for caching.

    The function relies on the 'reaper.json' and 'config.json' files for configuration data.

    Returns:
    None
    """
    # Read JSON file data
    with open("saves/reaper/reaper.json", 'r', encoding="utf-8") as json_file:
        data_reaper = json.load(json_file)
    
    url = data_reaper["url"]
    url_search = url + "comics/"
    url += "latest/comics"
    
    dict_comics = {}
    auto_complete = {}
    auto_complete["list"] = []
    
    size_dict_old = 0
    size_dict_new = 0
    
    # Loop through pages of comics
    for i in range(1, sys.maxsize):
        response = ""
        if i > 1:
            response = requests.get(url+"?page="+str(i),headers=HEADERS)
        else:
            response = requests.get(url,headers=HEADERS)
        
        response_list = response.text.split("\n")
        
        # Extract comic names and URLs
        for index, i in enumerate(response_list):
            if i.find(f'<a href="{url_search}') > -1 and response_list[index+1].find("<img") < 0 and response_list[index+1].find("Chapter") < 0:
                temp_url = i
                temp_name = response_list[index+1]
                temp_name = html.unescape(temp_name)
                match = re.search(r'href="([^"]+)"', temp_url)
                if match:
                    temp_url = match.group(1)

                dict_comics[temp_name] = {}
                dict_comics[temp_name]["url"] = temp_url
                dict_comics[temp_name]["newest_chap"] = response_list[index+6].split()[1]
                auto_complete["list"].append(temp_name)
                
                size_dict_new = len(dict_comics)

        # Check if the number of comics has stopped increasing
        if size_dict_old == size_dict_new:
            break
        if size_dict_new > size_dict_old:
            size_dict_old = size_dict_new
    
    # Save the cache data to a JSON file
    with open("scripts/search_reaper_cache.json", "w", encoding="utf-8") as cache_file:
        json.dump(dict_comics, cache_file, ensure_ascii=False, indent=4)
    with open("auto_complete_reaper.json", "w", encoding="utf-8") as complete_file:
        json.dump(auto_complete, complete_file, ensure_ascii=False, indent=4)

def update_asura_cache():
    """
    Update the cache of manga data for the Asuratoon website.

    This function fetches and stores a list of manga titles and their URLs from the Asuratoon website.
    The data is saved in a JSON file for caching.

    The function relies on the 'asura.json' and 'config.json' files for configuration data.

    Returns:
    None
    """
    # Read JSON file data
    with open("saves/asura/asura.json", 'r', encoding="utf-8") as json_file:
        data_asura = json.load(json_file)
    
    # Build the URL for the manga list on Asuratoon
    super_url = data_asura["url"]
    super_url += "manga/?page="
    
    dict_manga = {}
    auto_complete = {}
    auto_complete["list"] = []
    
    last = False
    for i in range(1, sys.maxsize):
        # Fetch the web page content
        response = requests.get(super_url+str(i),headers=HEADERS)

        response = response.text.split("\n")
        
        # Extract links from the response
        links = [i for i in response if i.find(f'<a href="{data_asura["url"]}manga/') > -1]
        chaps = [response[index+8] for index,i in enumerate(response) if i.find(f'<a href="{data_asura["url"]}manga/') > -1]
        next_list = [i for i in response if i.find(f'class="r">Next') > -1]
        

        if len(next_list) == 0:
            last = True
            break
        
        for index, i in enumerate(links):
            # Use regular expressions to extract the title and URL
            match_links = re.search(r'href="(.*?)" title="(.*?)">', i)
            match_chaps = re.search(r'>(.*?)<', chaps[index])
            
            
            
            if match_links and match_chaps:
                url = match_links.group(1)
                title = match_links.group(2)
                newest_chap = match_chaps.group(1)
                newest_chap = newest_chap.split()[1]

                # Unescape HTML entities in the title
                title = html.unescape(title)
            
                # Create a dictionary with the title and URL
                dict_manga[title] = {}
                dict_manga[title]["url"] = url
                dict_manga[title]["newest_chap"] = newest_chap
                auto_complete["list"].append(title)
        
        if last:
            break
    
    # Save the cache data to a JSON file
    with open("scripts/search_asura_cache.json", "w", encoding="utf-8") as cache_file:
        json.dump(dict_manga, cache_file, ensure_ascii=False, indent=4)
    with open("auto_complete_asura.json", "w", encoding="utf-8") as complete_file:
        json.dump(auto_complete, complete_file, ensure_ascii=False, indent=4)


def check_asura():
    """
    Check for updates in the Asura bookmarks and return update information.

    Returns:
        Tuple:
        - Index 0: A dictionary containing information about the newest and next-to-read chapter for each bookmarked webcomic.
            - Key: Webcomic name
            - Value: Dictionary with information about the newest and next-to-read chapters, including chapter name, number, and URL.
        - Index 1: A dictionary containing all available links, chapter numbers, and names for each bookmarked webcomic.
            - Key: Webcomic name
            - Value: Dictionary with chapter numbers as keys and tuples containing chapter names and URLs.
    """
    up_to_date_asura()
    with open("scripts/search_asura_cache.json", "r", encoding='utf-8') as cache_file:
        cache = json.load(cache_file)
    with open("saves/asura/asura.json", "r", encoding='utf-8') as json_file:
        bookmarks = json.load(json_file)["bookmarks"]
    
    cache = {key: value for key, value in cache.items() if key in bookmarks}
    
    have_update = [key for key, value in cache.items() if float(value["newest_chap"]) > float(bookmarks[key]["current_chap"])]
    
    update_links = {}
    all_links_after = {}
    
    for name in have_update:
        
        response = requests.get(bookmarks[name]["url"], headers=HEADERS)
        response = response.text.split("\n")
        
        nums = [i for i in response if i.find('<li data-num="') > -1]
        
        # nums = [float(i.split('data-num="')[1].split(' ')[0]) for i in nums]
        
        nums_temp = nums.copy()
        entire_names = [i.split('data-num="')[1][:-2] for i in nums]
        entire_names = ["Chapter " + i for i in entire_names]
            
        nums = []
            
        for i in nums_temp:
            i = i.split('data-num="')[1]
            i = i.split(" ")[0]
            while True:
                try:
                    if len(i) == 0:
                        if 0 in nums:
                            i = -1
                        else:
                            i = 0
                    i = float(i)
                    nums.append(i)
                    break
                except ValueError:
                    i = i[:-1]
        
        for index, i in enumerate(entire_names):
            if len(i.split(" ")) > 2:
                if nums[index] == int(nums[index]):
                    temp = i.split(" ")[0] + " " + str(nums[index])[:-2] + " | "
                else:
                    temp = i.split(" ")[0] + " " + str(nums[index]) + " | "
                rest = [html.unescape(ii) for ii_index, ii in enumerate(i.split(" ")) if ii_index > 1 ]
                
                temp += " ".join(rest)
                
                entire_names[index] = temp
            elif nums[index] == int(nums[index]):
                    entire_names[index] = i
            
            
        
        links = [response[index+3] for index, i in enumerate(response) if i.find('<li data-num="') > -1]
        
        links = [i.split('href="')[1][:-2] for i in links]
        
        
        
        for index, num in enumerate(nums):
            if num <= float(bookmarks[name]["current_chap"]):
                break
            if index == 0:
                all_links_after[name] = {}
                all_links_after[name][num] = (entire_names[index], links[index])
                
                
                
                update_links[name] = {}
                update_links[name]["newest"] = {}
                update_links[name]["next_to_read"] = {}
                update_links[name]["newest"]["name"] = entire_names[index]
                update_links[name]["newest"]["chap"] = num
                update_links[name]["newest"]["url"] = links[index]
            
            update_links[name]["next_to_read"]["name"] = entire_names[index]
            update_links[name]["next_to_read"]["chap"] = num
            update_links[name]["next_to_read"]["url"] = links[index]
            
            all_links_after[name][num] = (entire_names[index], links[index])
            
    return (update_links, all_links_after)

def up_to_date_asura():
    """
    Update Asura bookmarks to the latest URLs.
    """
    with open("scripts/search_asura_cache.json", "r", encoding='utf-8') as cache_file:
        cache = json.load(cache_file)
    with open("saves/asura/asura.json", "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
    
    bookmarks = data["bookmarks"]
    
    cache = {key: value for key, value in cache.items() if key in bookmarks}
    
    for key, value in cache.items():
        bookmarks[key]["url"] =  value["url"]
        
    data["bookmarks"] = bookmarks
    
    with open("saves/asura/asura.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def up_to_date_reaper():
    """
    Update Reaper bookmarks to the latest URLs.
    """
    with open("scripts/search_reaper_cache.json", "r", encoding='utf-8') as cache_file:
        cache = json.load(cache_file)
    with open("saves/reaper/reaper.json", "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
    
    bookmarks = data["bookmarks"]
    
    cache = {key: value for key, value in cache.items() if key in bookmarks}
    
    for key, value in cache.items():
        bookmarks[key]["url"] = value["url"]
        
    data["bookmarks"] = bookmarks
    
    with open("saves/reaper/reaper.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def check_reaper():
    """
    Check for updates in the Reaper bookmarks and return update information.

    Returns:
        Tuple:
        - Index 0: A dictionary containing information about the newest and next-to-read chapter for each bookmarked webcomic.
            - Key: Webcomic name
            - Value: Dictionary with information about the newest and next-to-read chapters, including chapter name, number, and URL.
        - Index 1: A dictionary containing all available links, chapter numbers, and names for each bookmarked webcomic.
            - Key: Webcomic name
            - Value: Dictionary with chapter numbers as keys and tuples containing chapter names and URLs.

    """
    up_to_date_reaper()
    with open("scripts/search_reaper_cache.json", "r", encoding='utf-8') as cache_file:
        cache = json.load(cache_file)
    with open("saves/reaper/reaper.json", "r", encoding='utf-8') as json_file:
        bookmarks = json.load(json_file)["bookmarks"]
    
    cache = {key: value for key, value in cache.items() if key in bookmarks}

    have_update = [key for key, value in cache.items() if float(value["newest_chap"]) > float(bookmarks[key]["current_chap"])]
    
    update_links = {}
    all_links_after = {}
    
    for name in have_update:
        end = False
        for page in range(1, sys.maxsize):
            
            response = requests.get(bookmarks[name]["url"]+"?page="+str(page), headers=HEADERS)
            response = response.text.split("\n")
            
            nums = [i for i in response if i.find('<li wire:key="') > -1]
            
            temp_nums = nums.copy()
            
            nums = []
            
            for i in temp_nums:
                i = i.split("-")
                i = i[len(i)-1]
                
                while True:
                    try:
                        i = float(i)
                        nums.append(i)
                        break
                    except ValueError:
                        i = i[:-1]
            
            entire_names = nums.copy()
            entire_names = ["Chapter " + str(i) for i in entire_names]
            
            for index, i in enumerate(entire_names):
                if len(i.split(" ")) > 2:
                    if nums[index] == int(nums[index]):
                        temp = "Chapter " + str(nums[index])[:-2] + " | "
                    else:
                        temp = "Chapter " + str(nums[index]) + " | "
                    rest = [html.unescape(ii) for ii_index, ii in enumerate(i.split(" ")) if ii_index > 1 ]
                    
                    temp += " ".join(rest)
                    
                    entire_names[index] = temp
                elif nums[index] == int(nums[index]):
                    entire_names[index] = i
        
            links = [response[index+1] for index, i in enumerate(response) if i.find('<li wire:key="') > -1]
            
            links = [i.split('href="')[1].split(" ")[0][:-1] for i in links]
            
            for index, num in enumerate(nums):
                if num <= float(bookmarks[name]["current_chap"]):
                    end = True
                    break
                if index == 0 and page == 1:
                    all_links_after[name] = {}
                    all_links_after[name][num] = (entire_names[index], links[index])
                    
                    update_links[name] = {}
                    update_links[name]["newest"] = {}
                    update_links[name]["next_to_read"] = {}
                    update_links[name]["newest"]["name"] = entire_names[index]
                    update_links[name]["newest"]["chap"] = num
                    update_links[name]["newest"]["url"] = links[index]
                
                update_links[name]["next_to_read"]["name"] = entire_names[index]
                update_links[name]["next_to_read"]["chap"] = num
                update_links[name]["next_to_read"]["url"] = links[index]

                all_links_after[name][num] = (entire_names[index], links[index])
            if end:
                break
    
    return (update_links, all_links_after)
    
    

def url_update(scan:int):
    """
    Update URLs for the specified scan (0 for Asura, 1 for Reaper).

    Args:
        scan (int): The scan to update URLs for (0 for Asura, 1 for Reaper).
    """
    path = "saves/asura/asura.json" if scan == 0 else "saves/reaper/reaper.json"
    
    with open(path, "r", encoding='utf-8') as file:
        data = json.load(file)
    
    if not len(data["bookmarks"]) == 0:
        url = data["url"]
        for key, value in data["bookmarks"].items():
            link = value["url"]
            link = link[link.find("/")+1:]
            link = link[link.find("/")+1:]
            link = url + link[link.find("/")+1:]
            value["url"] = link
        
    if not len(data["archived_bookmarks"]) == 0:
        url = data["url"]
        for key, value in data["archived_bookmarks"].items():
            link = value["url"]
            link = link[link.find("/")+1:]
            link = link[link.find("/")+1:]
            link = url + link[link.find("/")+1:]
            value["url"] = link