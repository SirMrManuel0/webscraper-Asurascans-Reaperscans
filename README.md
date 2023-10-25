# webscraper-Asurascans-Reaperscans

This project is a Python-based tool for managing and aggregating manga, manhua, and manhwa of specific scan websites. It provides functionality for creating JSON configuration files, searching for manga titles on specific scan websites, and updating cache files for quick access to the latest titles.

## Project Components

### 1. main.py

`main.py` is the core of the project, serving as the user interface and orchestration script. It handles the management of scan website URLs, cache updates, and user interactions. The script allows users to search for manga titles, update cache files, and more.

### 2. createJSONS.py

`createJSONS.py` is responsible for creating and updating JSON configuration files for specific scan websites. It checks for the existence of essential JSON files and, if missing, creates default configuration files for 'AsuraScans' and 'ReaperScans' websites. Users can customize URLs, bookmarks, and other settings through this script.

### 3. search.py

`search.py` contains functions for performing searches on scan websites and updating cache files. It includes functions for Google searches, searching for manga titles on 'AsuraScans' and 'ReaperScans' websites, and updating cache files with the latest titles and URLs. The script is critical for providing up-to-date search results and scan information.

### 4. requirements.txt

`requirements.txt` is a text file listing the Python packages required for running this project. You can use the provided package list to install the necessary libraries using the `pip` package manager.

## Installation

To set up the project and install the required Python packages, use the following command:

```bash
pip install -r requirements.txt
```