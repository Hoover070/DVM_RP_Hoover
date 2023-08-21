import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from openpyxl import Workbook  # Needed to handle Excel files
import os

"""
This is the arXiv API access code for the research project to DVM for Hoover, William

Args: None
returns: Data Frame with freshly scraped data from arXiv API

search queries are going to be anything related to the field of AI: Artificial Intelligence
"""

SEARCH_QUERIES = [
    "Artificial Intelligence",
    "Machine Learning",
    "Deep Learning",
    "Neural Networks",
    "Natural Language Processing",
    "Computer Vision",
    "Robotics",
    "Data Mining",
    "Data Science",
    "Big Data",
    "Data Analytics",
    "Data Visualization",
    "Data Engineering",
    "Data Warehousing",
    "Data Modeling",
    "Data Architecture",
    "Data Governance",
    "Data Quality",
    "Data Security",
    "Data Storage",
    "Data Integration",
    "Data Migration",
    "Data Lake",
    "Data Lakehouse",
    "Data Catalog",
    "Data Dictionary",
    "Data Lineage",
    "Data Profiling",
    "Data Wrangling",
    "Data Cleansing",
    "Data Preparation",
    "Data Exploration",
]


def scrape_arxiv():
    # Variables
    saved_papers = []

    for search_query in SEARCH_QUERIES:
        start_index = 0
        max_results = 100

        while True:
            print(f'looking for {search_query} papers')
            query_params = {
                'search_query': f'all:{search_query} AND submittedDate:[20000101 TO 20231231]',
                'start': start_index,
                'max_results': max_results  # max is 100
            }

            # Send the access request to the arXiv API
            response = requests.get('http://export.arxiv.org/api/query', params=query_params)
            print(f'{max_results} results for {search_query}')
            print(response.content)
            soup = BeautifulSoup(response.content, 'xml')

            # Extract and save the data
            entries = soup.find_all('entry')
            for entry in entries:
                title = entry.title.text
                year = entry.published.text[:4]
                affiliations_tag = entry.find('affiliation')
                affiliations = affiliations_tag.text if affiliations_tag else 'Independent'
                saved_papers.append([title, year, affiliations, search_query])  # Added search_query
            if len(entries) < max_results:
                break

            start_index += max_results
            time.sleep(3)  # Pause to be considerate

    # Create a DataFrame
    df = pd.DataFrame(saved_papers, columns=['Title', 'Year', 'Affiliations', 'Query'])

    # Convert to int
    df['Year'] = df['Year'].astype(int)

    # Save DataFrame df as Excel file in the output directory
    csv_path = 'data/ai_research_data.csv'
    df.to_csv(csv_path, index=False)

    return df



