import requests
from bs4 import BeautifulSoup
import googlesearch
import json
import re
import html
import sys


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
    Perform a search for a certain manga / manhua / manhwa on asurascans.
    
    Args:
        query (str): The name.
        
    Returns:
        dict: A dictonary of results (name: url).
    """
    
    # Get header from config.json
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    # Extract the headers from the configuration
    headers = config.get("headers", {})
    
    # Replace spaces with plus signs to format the query for the URL
    query = query.replace(" ", "+")
    
    # Read JSON file data
    with open("saves/asura/asura.json", 'r') as json_file:
        data_asura = json.load(json_file)
    
    # Construct the URL for the search
    url = data_asura["url"]
    url += "?s=" + query
    
    
    # Send a GET request to the AsuraScans search page
    response = requests.get(url,headers=headers)
    
    # Extract the page numbers from the HTML content
    page_number = response.text.split("\n")
    page_number = [i for i in page_number if i.find('<a class="page-numbers"') > -1]
    
    try:
        # Get the last page number if it exists
        page_number = page_number[len(page_number)-1]
    except IndexError:
        try:
            # Get the first page number if the last page number doesn't exist
            page_number = page_number[0]
        except IndexError:
            # Use a default page number if no page numbers are found
            page_number = "<a>1</a>"
            
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(page_number, 'html.parser')
    
    # Find the text inside the <a> tag to determine the total number of pages
    page_number = soup.get_text()
    page_number = int(page_number) + 1 # Add 1 to loop through all pages with range()
    
    returner = {}
    
    # Iterate through pages
    for i in range(1, page_number):
        
        
        if i == 1:
            url = data_asura["url"]
            url += "?s=" + query
        else:
            url = data_asura["url"]
            url += "page/" + str(i) + "/?s=" + query
        
        # Send a GET request to the AsuraScans search page
        response = requests.get(url,headers=headers)
        
        # Split the HTML content into lines
        lines = response.text.split("\n")
        
        
        url = data_asura["url"]
        
        
        # Extract links to manga titles from the HTML content
        links = [i for i in lines if i.find(f'<a href="{url}manga/') > -1]
        
        results = []

        # Extract URL and title from each link using regular expressions
        for link in links:
            match = re.search(r'href="([^"]+)" title="([^"]+)"', link)
            
            if match:
                url = match.group(1)
                title = match.group(2)
                results.append(f"{url} {title}")
        
        # Create a dictionary of results (name: url)
        for i in results:
            splitted = i.split(" ")
            url = splitted[0]
            length = len(splitted)
            name = ""
            for i in range(1, length):
                if not i == length - 1:
                    name += splitted[i] + " "
                elif i == length - 1:
                    name += splitted[i]
                    
            name = html.unescape(name)  # Replace HTML entities
            returner[name] = url
    
    return returner


def search_reaperscans(query:str):
    """
    Search for comics on the Reaperscans website and filter by a given query.

    Args:
    query (str): The query to filter comics by.

    Returns:
    dict: A dictionary of comic names and their corresponding URLs.
    """
    # Read JSON file data
    with open("scripts/search_reaper_cache.json", 'r') as json_file:
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
    with open("saves/reaper/reaper.json", 'r') as json_file:
        data_reaper = json.load(json_file)
    
    # Get header from config.json
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    # Extract the headers from the configuration
    headers = config.get("headers", {})
    
    url = data_reaper["url"]
    url += "comics"
    
    dict_comics = {}
    
    size_dict_old = 0
    size_dict_new = 0
    
    # Loop through pages of comics
    for i in range(1, sys.maxsize):
        response = ""
        if i > 1:
            response = requests.get(url+"?page="+str(i),headers=headers)
        else:
            response = requests.get(url,headers=headers)
        
        response_list = response.text.split("\n")
        
        # Extract comic names and URLs
        for index, i in enumerate(response_list):
            if i.find(f'<a href="{url}/') > -1 and response_list[index+1].find("<img") < 0:
                temp_url = i
                temp_name = response_list[index+1]
                temp_name = html.unescape(temp_name)
                match = re.search(r'href="([^"]+)"', temp_url)
                if match:
                    temp_url = match.group(1)

                dict_comics[temp_name] = temp_url
                
                size_dict_new = len(dict_comics)

        # Check if the number of comics has stopped increasing
        if size_dict_old == size_dict_new:
            break
        if size_dict_new > size_dict_old:
            size_dict_old = size_dict_new
    
    # Save the cache data to a JSON file
    with open("scripts/search_reaper_cache.json", "w") as cache_file:
        json.dump(dict_comics, cache_file, indent=4)

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
    with open("saves/asura/asura.json", 'r') as json_file:
        data_asura = json.load(json_file)
    
    # Get header from config.json
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    # Extract the headers from the configuration
    headers = config.get("headers", {})
    
    # Build the URL for the manga list on Asuratoon
    url = data_asura["url"]
    url += "manga/list-mode/"
    
    dict_manga = {}
    
    # Fetch the web page content
    response = requests.get(url)
    
    response = response.text.split("\n")
    
    # Extract links from the response
    links = [i for i in response if i.find("<li>") > -1 and i.find("<a") > -1 and i.find("href") > -1]
    
    for i in links:
        # Use regular expressions to extract the title and URL
        match = re.search(r'href="(.*?)"[^>]*>(.*?)<', i)

        if match:
            url = match.group(1)
            title = match.group(2)

            # Unescape HTML entities in the title
            title = html.unescape(title)
        
            # Create a dictionary with the title and URL
            dict_manga[title] = url
    
    # Save the cache data to a JSON file
    with open("scripts/search_asura_cache.json", "w") as cache_file:
        json.dump(dict_manga, cache_file, indent=4)