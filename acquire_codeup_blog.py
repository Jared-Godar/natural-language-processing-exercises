import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import strftime


########## GET LINKS ###############

def get_links():
    '''
    Create a list containing the URLs for Codeup blog posts.'''
    response = requests.get("https://codeup.com/blog/",
                            headers={"user-agent": "Codeup DS"})
    soup = BeautifulSoup(response.text)
    links = [link.attrs["href"] for link in soup.select(".more-link")]
    return links

################ PARSE BLOG #######################


def parse_blog(url):
    '''
    Take a url and return title, date, and content of individual blog posts to a dictionary.
    '''
    response = requests.get(url, headers={'user-agent': 'Codeup DS'})
    soup = BeautifulSoup(response.text)
    return {
        'title': soup.select_one('.entry-title').text,
        'date': soup.select_one('.published').text,
        'post': soup.select_one('.entry-content').text.replace('\n', ' ').strip(),
    }

################## GET BLOG POSTS #####################


def get_blog():
    '''
    Wrapper function to pull URL links from main blog page, then extract information from those links returning a dataframe
    '''
    links = get_links()
    df = pd.DataFrame([parse_blog(link) for link in links])
    # Cache results
    today = strftime('%Y-%m-%d')
    df.to_csv(f'codeup_blog_{today}.csv')
    print('Results saved to CSV file')
    return df
