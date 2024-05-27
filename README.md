# Scraping_Recipes_Project
This project aims to crawl a [recipes website](https://pinchofyum.com/), scrapes out hundreds of recipes details, saving all collected data into a json file.

Then it:
- Cleans and analyzes collected data 
- Utilizes data for: 
   - Recipe Suggestor (suggests & displays a recipe for user based on his preferences)
   - Chef Bot (telegram bot that sends a daily recipe to subscribers) 

## Components
### 1. Scraping
- Scraper: This module offers all needed methods to scrape all needed information from a given recipe page soup
- Crawler: This module's goal is to utilize Scraper module functions to scrape each page in the recipes website. It consists of 2 main parts, functions to get links of all pages, and functions to scrape them iteratively
- Runner: Runs the Crawler until all recipes are scraped. For each run, it displays the current progress & saves any output/error to a log file

### 2. Data Preparation
- Cleaning:
   - Renaming columns
   - Fixing datatypes
   - Removing duplicates, nulls, & redundant categories/cuisines
- Analysis: we tried to answer some important questions:
   - Is there a favorite cuisine?
   - Does number of steps affect the rating?
   - Is there a 'harder' cuisine?

### 3. Chef Bot
- ChefBot: This module represents the telegram bot built using telebot library, so this is the major part of ChefBot application. It runs a parallel thread to continously check if it's time to send recipes for subscribers, while also being ready to accept new ones.
- Image Processor: Image_Processor module aims to enable the bot to send images, by providing 2 functions to scrape and save a given image url.
- Helper: The helper module offers all what chef_bot module needs in order to work, but isn't his duty to create it himself. It also defines constant variables for messages & paths. Also, it connects chef_bot to Image_Processor module

### 4. Recipe Suggestor
- Main: This module is the one who:
   - Interacts with the user
   - Recieves his answers
   - Utilizes Displayer & Image_Processor modules to send responses back to him
- Displayer: Responsible for presenting the recipe visually, as an html page
- Suggestor: Represents the 'mind' of this project. It is the one responsible for making the decision and choosing top recipes given user preferences

## Usage:
For the telegram bot part, you can simply chat with it [here](https://t.me/Everday_Recipe_Bot)

To use the recipe suggestor, it needs a little more patience:

- Download [Python](https://www.python.org/downloads/)
- Download [the project](https://github.com/homanydata/Scraping_Recipes_Project/archive/refs/heads/main.zip)
- Open the command line in the project folder then install required libraries:
   ```sh
   pip install -r requirements.txt
   ```
- Run recipe suggestor [main.py](./recipe%20suggestor/main.py)
- Choose your preferences

Hope you like the taste :)

## Documentation
For further details, the project is well documented [here](https://homanydata.github.io/Scraping_Recipes_Project/), which is created using pydoc + some additional styling. HTML/CSS code of the documentation is inside [docs branch](https://github.com/homanydata/Scraping_Recipes_Project/tree/docs)
