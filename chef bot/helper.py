import os
import pandas
from Image_Processor import save_image, scrape_image


def get_ith_recipe_message(index):
    recipe = get_ith_recipe(index=index)
    msg = f"""
It is Daily Recipe Time !!
————————————————\n
✨ {recipe['title']}: ✨\n
is a {recipe['category']} from {recipe['cuisine']} cuisine, of rating {recipe['rating']}
Time needed: {recipe['total_time']} mins\n
Here is how you can do it yourself:\n\n
———————————————————————————\n
First, you will need:\n
- {'\n-  '.join(recipe['ingredients'])}\n
———————————————————————————\n\n
Step by step: 👨🏻‍🍳👩🏻‍🍳
{''.join([f'\nStep {number_to_emoji(i + 1)}: {step}\n' for i, step in enumerate(recipe['steps'])])}\n
———————————————————————————\n\n
Hope you like the taste! 😋
"""
    
    photo_name = './application_2/recipe.jpg'
    try:
        image_data = scrape_image(image_url=recipe['image_link'])
        save_image(image_data=image_data, filename=photo_name)
    except Exception as e:
        print(f'Error encountered while saving this image:{recipe['image_link']}\n{e}')
        photo_name = f'"{recipe['title']}"\n Recipe Image: {recipe['image_link']}'
    return msg, photo_name


def get_ith_recipe(index):
    df = pandas.read_json(PATHS.DATASET_FILE_PATH)
    if index >= len(df):
        index = 0
        with open(PATHS.CURR_INDEX_FILE_PATH, 'w') as file:
            file.write(str(index))
    df.rename(columns={0:'name', 1:'category', 2:'cuisine', 3:'time_needed', 5:'steps', 6:'rating', 7:'ingredients', 8:'image_link'}, inplace=True)
    return df.iloc[index, :]


def number_to_emoji(number):
    digits = ['0️⃣','1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣']
    if number >= 10:
        return number_to_emoji(number // 10) + digits[number % 10]
    return digits[number % 10]


class PATHS:
    SUBSCRIBERS_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'subscribers_ids.txt')
    CURR_INDEX_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'curr_index.txt')
    DATASET_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../cleaning&analysis/cleaned_data.json')


class MSGS:
    INTRO_MESSAGE = f"""
Welcome to our delicious world! 😃😋\n
Happy to meet you, I am Chef Bot 👨‍🍳🤖\n
I am an expert 😎 I know a lot of recipes, from different cuisines around the world 🌎\n
If you like, you could subscribe to our daily recipe, which I send everyday, you could try to make it 🍴\n
If you're not a chef yet, this is your chance! 😉
"""
    SUBSCRIBE_MESSAGE = 'Welcome!! It will be my honor to serve you from now on!'
    ALREADY_SUBSCRIBED_MESSAGE = 'You are already subscribed my friend'
    UNSUBSCRIBE_MESSAGE = 'Sorry to see you leave! Hope to c u again, good luck!'
    NOT_SUBSCRIBED_MESSAGE = 'You are already not subscribed my friend'
    ERROR_MESSAGE = 'Sorry an error encountered! Try again later'
