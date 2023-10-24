import os
import requests

# Check if the 'scripts' directory exists; if not, raise an error
if not os.path.exists("scripts"):
    raise FileNotFoundError("The 'scripts' directory is missing. It seems the cloning/copying/installing of this project failed.")

# Import necessary modules
import search
import request
import save

# Define a dictionary of scan URLs
scans = {
    "asurascans": "https://asuratoon.com",
    "asura": "https://asuratoon.com",
    "reaperscans": "https://reaperscans.com/",
    "reaper": "https://reaperscans.com/"
}

# Iterate through the scan URLs in the dictionary
for k, i in scans.items():
    try:
        # Check if the URL is accessible
        requests.get(i)
    except Exception as e:
        print(f"Please search the current/right URL for {k}.")
        while True:
            # Prompt the user to enter a new URL for the scan
            test = input(f"Enter the URL here for {k} (e.g., https://asuratoon.com): ")
            try:
                # Check if the entered URL is valid
                requests.get(test)
                scans[k] = test  # Update the URL in the dictionary
                # Update the corresponding key in the dictionary if needed
                if k in ["asurascans", "asura"]:
                    scans["asurascans" if k == "asura" else "asura"] = test
                if k in ["reaperscans", "reaper"]:
                    scans["reaperscans" if k == "reaper" else "reaper"] = test
                break
            except Exception:
                print("Invalid URL!")

# Create necessary directories for saving data
os.makedirs("saves", exist_ok=True)
os.makedirs("saves/asura", exist_ok=True)
os.makedirs("saves/reaper", exist_ok=True)
