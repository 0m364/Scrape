import os
import requests
from bs4 import BeautifulSoup

# Function to scrape data from a website
def scrape_website(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, requests.exceptions.Timeout) as err:
        print(f"Error occurred: {err}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    # Remove scripts and styles for clean text
    for script in soup(["script", "style"]):
        script.decompose()

    text = soup.get_text(separator="\n")

    # Break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())

    # Remove blank lines
    text = '\n'.join(line for line in lines if line)
    
    return text

# Prompt user for the website URL
website_url = input("Please enter the URL of the website you want to scrape data from: ")

# Scrape the website for data
website_text = scrape_website(website_url)

if website_text is None:
    print("Scraping failed. Please check your URL or internet connection.")
else:
    # Prompt user to create or update the "scraped" file
    if os.path.exists("scraped"):
        append_or_overwrite = input("The 'scraped' file already exists. Would you like to 'append' or 'overwrite' its content? ")

        if append_or_overwrite.lower() == "append":
            with open("scraped", "a") as file:
                file.write("\n" + website_text)
            print("Data appended to 'scraped' file.")
        else:
            with open("scraped", "w") as file:
                file.write(website_text)
            print("Data overwritten in 'scraped' file.")
    else:
        with open("scraped", "w") as file:
            file.write(website_text)
        print("'scraped' file created with scraped data.")
