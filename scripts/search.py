import requests
from bs4 import BeautifulSoup
import googlesearch
import json
import re
import html


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


def search_asurascans(query:str, amount:int = 1):
    """
    Perform a search for a certain manga / manhua / manhwa on asurascans.
    
    Args:
        query (str): The name.
        amount (int, optional): The number of search results to retrieve (default is 1).
        
    Returns:
        dict: A dictonary of results (name: url).
    """
    
    # Replace spaces with plus signs to format the query for the URL
    query = query.replace(" ", "+")
    
    # Read JSON file data
    with open("saves/asura/asura.json", 'r') as json_file:
        data_asura = json.load(json_file)
    
    # Construct the URL for the search
    url = data_asura["url"]
    if url.endswith("/"):
        url += "?s=" + query
    else:    
        url += "/?s=" + query
    
    # Send a GET request to the AsuraScans search page
    response = requests.get(url)
    
    # Split the HTML content into lines
    lines = response.text.split("\n")
    
    url = data_asura["url"]
    
    # Ensure the URL ends with a "/"
    if not url.endswith("/"):
        url += "/"
    
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
    
    returner = {}
    
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
                
        name = html.unescape(name)
        returner[name] = url
    
    return returner
