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


def search_raeperscans(query:str):
    """
    Search for comics on the Reaperscans website and filter by a given query.

    Args:
    query (str): The query to filter comics by.

    Returns:
    dict: A dictionary of comic names and their corresponding URLs.
    """
    
    # Read JSON file data
    with open("saves/reaper/reaper.json", 'r') as json_file:
        data_asura = json.load(json_file)
    
    # Get header from config.json
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    # Extract the headers from the configuration
    headers = config.get("headers", {})
    
    url = data_asura["url"]
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
                
    
    temp_dict = dict_comics.copy()
    
    # Filter comics by query
    for k,i in temp_dict.items():
        if k.lower().find(query.lower()) < 0:
            dict_comics.pop(k)
    
    return dict_comics
    
    