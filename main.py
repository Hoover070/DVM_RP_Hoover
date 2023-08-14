"""
This is the research project to DVM for Hoover, William
The purpose and goal of this project is to scrape the data from
arXiv api for all research papers related to the field of AI: Artificial Intelligence
over the course of a 10-year period, to track the growth of the field and to see
if research has been speeding up or slowing down
"""

#imports
from arXiv_Api_Access import scrape_arxiv
import matplotlib.pyplot as plt


#variables
data_frame = scrape_arxiv()


#number of total AI papers published
data_frame['Year'].value_counts().sort_index().plot(kind='bar')
plt.title('Number of AI Papers Published per Year')
plt.xlabel('Year')
plt.ylabel('Number of Papers')
plt.savefig('Number of AI Papers Published per Year.png')
plt.show()



