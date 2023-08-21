"""
This is the research project to DVM for Hoover, William
The purpose and goal of this project is to scrape the data from
arXiv api for all research papers related to the field of AI: Artificial Intelligence
over the course of a 10-year period, to track the growth of the field and to see
if research has been speeding up or slowing down
"""

#imports
import pandas as pd
from src.arXiv_Api_Access import scrape_arxiv
import matplotlib.pyplot as plt
import seaborn as sns



# #update ai_research_data.xlsx with updated data
# uncomment if needed to use
# scrape_arxiv()
#
# # dataframe to be used through the program
df = pd.read_csv('data/ai_research_data.csv')

#Line plot for number of papers published per year for each AI field
plt.figure(figsize=[15,10])

# Loop through each unique search query and plot a line for it
for query in df['Query'].unique():
    subset = df[df['Query'] == query]
    subset['Year'].value_counts().sort_index().plot(label=query)

plt.title('Number of Papers Published per Year for Different AI Fields')
plt.xlabel('Year')
plt.ylabel('Number of Papers')
plt.legend()
plt.savefig('output/Comparison_of_AI_Fields.png')
plt.show()

#



