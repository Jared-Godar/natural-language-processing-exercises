import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import strftime


################ PARSE NEWS #################

def parse_news(article):
    '''
    Generate a dictionary of values for title, author, date, and body of news articles
    '''
    #card_title = article.select_one('.news-card-title')
    output = {}
    output['title'] = article.find('span', itemprop = 'headline').text
    output['author'] = article.find('span', class_ = 'author').text
    output['body'] = article.find('div', itemprop = 'articleBody').text
    output['date'] = article.find('span', clas ='date').text.split(',',2)[0]
    return output

################### PARSE PAGE #####################

def parse_page(url):
    '''
    Given a url, creates a dataframe where each row is a news article, getting category from end of url
    '''
    category = url.split('/')[-1]
    response = requests.get(url, headers={'user-agent': 'Codeup DS'})
    soup = BeautifulSoup(response.text)
    cards = soup.select('.news-card')
    df = pd.DataFrame([parse_news(card) for card in cards])
    df['category'] = category
    return df

#################### GET ARTICLES################

def get_articles():
    '''
    Creates a dataframe of articles.
    '''
    url = 'https://inshorts.com/en/read/'
    categories = ['business', 'sports', 'technology', 'entertainment']
    df = pd.DataFrame()
    for cat in categories:
        df = pd.concat([df, pd.DataFrame(parse_page(url + cat))])
    df = df.reset_index(drop=True)
    # Cache results
    today = strftime('%Y-%m-%d')
    df.to_csv(f'codeup_blog_{today}.csv')
    print('Results saved to CSV file')
    
    return df

##################################