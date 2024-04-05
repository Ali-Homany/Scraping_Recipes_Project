import requests
from bs4 import BeautifulSoup
import os

def scrape_recipe_page(soup: BeautifulSoup) -> list[list[str]]:
    title = get_title(soup)
    category = get_category(soup)
    cuisine = get_cuisine(soup)
    total_time = get_total_time(soup)
    nbr_of_ser = get_nbr_of_servings(soup)
    steps = get_steps(soup)
    rating = get_rating(soup)
    ingredients = get_ingredients(soup)
    list_all_type = [title,category,cuisine,total_time,nbr_of_ser,steps,rating,ingredients]
    return list_all_type


def get_title(soup):
    title_element = soup.find('h2', class_='tasty-recipes-title') 
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
    number_of_servings1 = soup.find('span', {'data-amount': True})
    number_of_servings_text = number_of_servings1.text.strip()
    number_of_servings = float(number_of_servings_text)
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
    rating = soup.find("span", class_="average")
    rating_text = rating.text.strip()
    rating = float(rating_text)
    return rating


def get_ingredients(soup):
    ingredient_items = soup.find_all('li', {'data-tr-ingredient-checkbox': True})
    ingredients_list = []

    for index, item in enumerate(ingredient_items, start=1):
        try:
            ingredient_type = item.find('strong').get_text(strip=True)
        except:
            ingredient_type = item.select('span')[-1].get_text(strip=True)
        quantity_span = item.find('span', attrs={'data-amount': True})
        quantity = quantity_span['data-amount'].strip() if quantity_span else None
        unit = quantity_span.get('data-unit', '').strip() if quantity_span else None
        ingredient_list = [ingredient_type, quantity, unit]
        ingredients_list.append(ingredient_list)
    return ingredients_list
