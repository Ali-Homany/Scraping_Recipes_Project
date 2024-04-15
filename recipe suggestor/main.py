import pandas
import warnings
import os
import time
from suggestor import suggest_recipes
from displayer import display_recipe


def get_int_from_user(msg, mini=None, maxi=None):
    '''
    This function asks the user for an integer, and makes sure it is bounded as needed
    
    Args:
        - msg (str): question to be asked for the user
        - mini (int): the minimum accepted value (included), default None
        - maxi (int): the maximum accepted value (included), default None
    '''
    answer = input(msg)
    if isnumeric(answer) and (not mini or mini <= int(answer)) and (not maxi or maxi >= int(answer)):
        return int(answer)
    msg = f"Please enter an integer{['',f', minimum {mini}'][mini is not None]}{['', f', maximum {maxi}'][maxi is not None]}: "
    return get_int_from_user(msg, mini, maxi)


def isnumeric(s):
    '''
    Args: s (str) string to be checked
    Returns: (bool) whether the given string is all numerical
    '''
    return all(character.isdigit() for character in s)


def get_string_from_user(msg):
    '''
    This function asks the user for a string
    Args
        - msg (str): question to be asked to user
    Returns:
        (str) user input
    '''
    response = input(msg)
    if response == '':
        return get_string_from_user('')
    return response


def get_user_choice(title, all_choices, allow_any=True):
    '''
    Args:
        - title (str): what the choice is about
        - all_choices (list[str]): list of available choices, if size 1, automatically returned
        - allow_any (bool): whether to add "any" choice or not
    Returns:
        (str): choice chosen by the user, None if the answer is any
    Raises:
        RuntimeError when all_choices is empty
    '''
    all_choices = list(set(all_choices))
    n = len(all_choices)
    if n == 0:
        raise RuntimeError('No choices are given! Empty list given')
    if n == 1:
        return all_choices[0]
    msg = f'Choose one from the list below for {title.capitalize()} (insert the number you want)\n'
    if allow_any: msg += '0) any\n'
    msg += ''.join([f'{i+1}) {c}\n' for i, c in enumerate(all_choices)])
    chosen_index = get_int_from_user(msg=msg, mini=int(not allow_any), maxi=n)
    os.system('cls')
    if chosen_index == 0:
        return None
    return all_choices[chosen_index - 1]


def get_available_ingredients_from_user():
    '''
    Returns:
        (list[str]): list of unique ingredients names that the user have
    '''
    n = get_int_from_user(msg='How many ingredients do you have? ', mini=1)
    available_ingredients = [get_string_from_user(f'{i + 1} ingredient: ') for i in range(n)]
    return available_ingredients


if __name__ == '__main__':
    try:
        warnings.filterwarnings('ignore')
        df = pandas.read_json('./cleaned_data.json')

        available_categories = df['category'].unique()
        chosen_category = get_user_choice('category', available_categories)
        if chosen_category is not None:
            df = df[df['category'] == chosen_category]

        available_cuisines = df['cuisine'].unique()
        chosen_cuisine = get_user_choice('cuisine', available_cuisines)
        suggestions = suggest_recipes(
                    df=df,
                    cuisine=chosen_cuisine,
                    category=chosen_category,
                    available_ingredients=get_available_ingredients_from_user()
                    )
        chosen_recipe = get_user_choice('best recipe', suggestions, allow_any=False)
        df = df[df['title'] == chosen_recipe]
        display_recipe(df.iloc[0])
    except Exception as e:
        print(f'An error occured while running: {e}')
    time.sleep(10)
