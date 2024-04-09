import requests
from bs4 import BeautifulSoup
import os

def scrape_recipe_page(soup):
    '''
    Args:
        soup (BeautifulSoup): contains html code of the recipe page to be scraped
    Returns:
        (list): all details about the recipe
    '''
    title = get_title(soup)
    if soup.find('header', class_='tasty-recipes-entry-header') is None or title is None or 'freezer' in title.lower() or 'instant' in title.lower():
        raise ValueError('This is not a recipe page, I cannot scrape it')
    category = get_category(soup)
    cuisine = get_cuisine(soup)
    total_time = get_total_time(soup)
    nbr_of_ser = get_nbr_of_servings(soup)
    steps = get_steps(soup)
    rating = get_rating(soup)
    ingredients = get_ingredients(soup)
    image_link = get_image_link(soup)
    list_all_type = [title, category, cuisine, total_time, nbr_of_ser, steps, rating, ingredients, image_link]
    return list_all_type


def get_title(soup):
    title_element = soup.find('h2', class_='tasty-recipes-title') 
    if title_element is None:
        title_element = soup.find('h1', class_='tasty-recipes-title')
    if title_element is None:
        return None
    title = title_element.text.strip()
    return title


def get_category(soup):
    category_element = soup.find('span', class_='tasty-recipes-category')
    category=category_element.text.strip()
    return category


def get_cuisine(soup):
    cuisine_element = soup.find('span', class_='tasty-recipes-cuisine')
    cuisine=cuisine_element.text.strip()
    return cuisine


def get_total_time(soup):
    li_time=soup.find('span', class_='tasty-recipes-total-time')
    total_time=li_time.text.strip()
    return total_time


def get_nbr_of_servings(soup):
    number_of_servings = soup.find('span', {'data-amount': True})
    if number_of_servings is None:
        return None
    number_of_servings = number_of_servings.text.strip()
    return number_of_servings


def get_steps(soup):
    allstep_element_div = soup.find('div',class_="tasty-recipes-instructions")
    allstep_element = allstep_element_div.find('ol')
    steps_text = allstep_element.find_all('li')
    list_steps = []
    for step in steps_text:
        list_steps.append(step.get_text(strip=True))
    return list_steps


def get_rating(soup):
    try:
        rating = soup.find("span", class_="average")
        rating = rating.text.strip()
        return rating
    except:
        return None


def get_ingredients(soup):
    ingredient_items = soup.find_all('li', {'data-tr-ingredient-checkbox': True})
    ingredients_list = []

    for index, item in enumerate(ingredient_items, start=1):
        ingredient_list = ' '.join(item.stripped_strings)
        ingredients_list.append(ingredient_list)
    return ingredients_list


def get_image_link(soup):
    try:
        main_image = soup.find_all('img')[1]
        main_image_link = main_image['src']
        return main_image_link
    except:
        DEFAULT_BACKGROUND_IMAGE = 'https://img.freepik.com/free-photo/wooden-planks-with-blurred-restaurant-background_1253-56.jpg'
        return DEFAULT_BACKGROUND_IMAGE
