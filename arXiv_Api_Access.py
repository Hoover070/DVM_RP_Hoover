import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

"""
This is the arXiv API access code for the research project to DVM for Hoover, William

Args: None
returns: Data Frame with freshly scraped data from arXiv API
"""


def scrape_arxiv():

    # Variables
    saved_papers = []
    start_index = 0
    max_results = 100

    # define the query parameters of the search. AI: Artificial Intelligence JAN012010-DEC312020
    while True:
        query_params = {
            'search_query': 'all:artificial intelligence AND submittedDate:[20000101 TO 20231231]',
            'start':  start_index,
            'max_results': max_results  # max is 100
        }

        # send the access request to the arXiv API
        response = requests.get('http://export.arxiv.org/api/query', params=query_params)
        soup = BeautifulSoup(response.content, 'xml')

        # extract and save the data
        entries = soup.find_all('entry')
        for entry in entries:
            title = entry.title.text
            year = entry.published.text[:4]
            affiliations_tag = entry.find('affiliation')
            affiliations = affiliations_tag.text if affiliations_tag else 'Independent'
            saved_papers.append([title, year, affiliations])
        if len(entries) < max_results:
            break

        start_index += max_results
        time.sleep(3)  # Pause to be considerate, they advise 2 seconds so i added 1 more

    # Create a DataFrame
    df = pd.DataFrame(saved_papers, columns=['Title', 'Year', 'Affiliations'])

    # convert to int
    df['Year'] = df['Year'].astype(int)

    # save dataframe df as CSV file
    df.to_csv('ai_research_data.csv', index=False)

    return df



