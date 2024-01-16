import requests
from bs4 import BeautifulSoup
from warnings import warn
from time import sleep
from random import randint
import numpy as np, pandas as pd
import seaborn as sns

## Define the URL you want to be scrapped

topics_url = 'https://www.imdb.com/list/ls051105303/'

## Get the response from it

response = requests.get(topics_url)

## Define the text from the response and convert the information
## Extract the title instances in the code

page_content = response.text
doc = BeautifulSoup(response.text, 'html.parser')  ## Parse (convert the information into something easier to work with) the HTML using beautiful soup
doc.find('title')

## Define a function which finds all the movie titles
## and adds them to a list

def get_movie_title():

    selection_class = "lister-item-header"
    movie_title_tags = doc.find_all('h3',{'class':selection_class})
    movie_titles = []

    for tag in movie_title_tags:
        title = tag.find('a').text
        movie_titles.append(title)

    return movie_titles

## Define a function which finds all the movie years
## and adds them to a list

def get_movie_year():

    year_selector = "lister-item-year text-muted unbold"           
    movie_year = doc.find_all('span',{'class':year_selector})
    movie_years = []

    for tag in movie_year:
        movie_years.append(tag.get_text().strip()[1:5])

    return movie_years

## Define a function which goes through all the pages of films
## and calls the other two functions to make the lists
## Sort the items in the dictionary and return a pandas dataframe

def all_pages():

    movies_dict = {
        'Title':[],
        'Year':[],
    }

    for i in range(1,2000,100):
        
        try:
            url = 'https://www.imdb.com/list/ls051105303/?start='+str(i)+'&ref_=adv_next'
            response = requests.get(url)
        except:
            break
            
        if response.status_code != 200:
            break

    titles = get_movie_title()
    years = get_movie_year()

    for i in range(len(titles)):
        movies_dict['Title'].append(titles[i])
        movies_dict['Year'].append(years[i])
    
    sorted_movies_dict = {key: value for key, value in sorted(movies_dict.items())}

    return pd.DataFrame(sorted_movies_dict)

## Call the function

movies = all_pages()

## Write the dictionary to a CSV file

movies.to_csv(r'C:\Users\pc\Desktop\Ai Core\SQL Essentials\Samuel_2.csv', index = None, encoding = 'utf-8')

