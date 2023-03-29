import requests
from bs4 import BeautifulSoup
import pandas as pd

# Disable SSL certificate verification
requests.packages.urllib3.disable_warnings()

# URL to scrape
url = 'https://nationalsharedhousing.org/program-directory/'

# Get HTML content
response = requests.get(url, verify=False)
html_content = response.content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all the state listings on the page
listings = soup.find_all('div', class_='vc_tta-panel')
listings

# Create an empty list to store the program information
programs = []

# Loop through each program listing and extract the title and link if available
for program in listings:
    program_name = program.find('h4').text
    program_links = program.find_all('a')
    program_link = ''
    for link in program_links:
        href = link.get('href')
        if href and 'http' in href:
            program_link = href
            break
    programs.append({'Program Name': program_name, 'Program Link': program_link})


# Convert the list of programs into a dataframe
df = pd.DataFrame(programs)

# Export the dataframe as a CSV file
df.to_csv('programs.csv', index=False)