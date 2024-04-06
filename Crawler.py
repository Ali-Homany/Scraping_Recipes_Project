import os
import time
import requests
import pandas
from bs4 import BeautifulSoup
from Scraper import scrape_recipe_page

LINKS_FILE_PATH = "recipes_links.txt"
MAIN_PAGE_LINK = 'https://pinchofyum.com/recipes/all'
LAST_PAGE_INDEX = 105


def write_to_file(filepath: str, lines: list[str]) -> None:
    '''
    This function writes a given list to a the given filepath

    Args:
        - filepath (str): full path of the file to be written to, including file extension
        - lines (list[str]): list of strings to be written to the file, line by line
    '''
    with open(filepath, "w") as file:
        file.write('\n'.join(lines))

# to be used once
def save_recipes_links():
    '''
    This function scrapes all needed recipes links from the main page, saves them to a file
    '''
    recipes_links = []
    for index in range(1, LAST_PAGE_INDEX + 1):
        print(f'Index {index}')
        curr_page_url = MAIN_PAGE_LINK + f'/page/{index}' * int(index > 1)
        soup = create_soup(curr_page_url)
        curr_recipes_links = [a['href'] for a in soup.select('section > div > article > a')]
        recipes_links.extend(curr_recipes_links)

    write_to_file("recipes_links.txt", recipes_links)


def create_soup(url):
    '''
    Args:
        - url (str): link of webpage
    Return:
        - soup (BeautifulSoup) from a given url
    Raises:
        - ValueError if invalid url passed
        - RuntimeError if connection failed or not successful request
    '''
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        raise ValueError(f'The URL {url} is not valid or could not be reached.')
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        raise RuntimeError('Check your internet connection')
    except Exception as error:
        raise RuntimeError(f'Error occured while requesting page: {error}')

    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def read_n_links(n=None):
    '''
    This function open 'recipes_links.txt' file, and returns links for recipes

    Args:
        - n (int): positive integer for the number of links wanted, if None, get all links there
    Return:
        - links (list[str]): list of first n links
    '''

    with open(LINKS_FILE_PATH, "r") as file:
        links = file.readlines()
    if n is None or n > len(links):
        n = len(links)
    if n < len(links):
        with open(LINKS_FILE_PATH, "w") as file:
            file.writelines(links[n:])
    else:
        os.remove(LINKS_FILE_PATH)
    links = [link.strip() for link in links[:n]]
    return links


def scrape_n_pages(n=None):
    '''
    This function uses read_n_links to get links for recipes, then uses scrape_recipe_page to scrape each one and create a list, then return it

    Args:
        - n (int): positive integer for the number of recipes wanted
    Return:
        - (list): list representing data of scraped recipes
    Raises:
        - ValueError when non-integer or negative integer passed
        - RuntimeError if an error happens while scraping the page
    '''
    if n is not None and not isinstance(n, int) and n < 0:
        raise ValueError('Error: Invalid value for parameter n: n should be a positive integer')

    links = read_n_links(n)
    result = []
    for index, link in enumerate(links):
        print(f'Page {index}: ', end='')
        try:
            soup = create_soup(link)
            curr_page_result = scrape_recipe_page(soup=soup)
            print('Done')
        except Exception as error:
            print(f'An error occured while scraping this page: {link}\n{error}')
            continue
        result.append(curr_page_result)
    return result


if __name__ == "__main__":
    if not os.path.exists(LINKS_FILE_PATH):
        save_recipes_links()
    # result = scrape_n_pages(10)
    # df = pandas.DataFrame(result)
    # df.to_csv('data.csv', mode='a', header=False, index=False)
