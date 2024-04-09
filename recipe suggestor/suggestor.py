import pandas


def count_common(ingredients, available_ingredients):
    common = 0
    for a in available_ingredients:
        for i in ingredients:
            common += int(i.lower().count(a.lower()) > 0)
    return common


def suggest_recipes(df: pandas.DataFrame, cuisine, category, available_ingredients, n=5):
    '''
    This function suggests recipes based on some given filters

    Args:
        - df (pandas.DataFrame): dataframe containing all recipes
        - cuisine (str): preferred cuisine, may be None, if no favorite
        - category (str): preferred category, may be None, if no favorite
        - available_ingredients (list[str]): list of ingredients the user has
        - n (int): number of recipes to be suggested, default 5
    Returns:
        (pandas.DataFrame) dataframe containing n recipes suitable suggestions
    '''
    print(f'Preferences: {cuisine}, {category}, {available_ingredients}\n')
    temp = df
    if cuisine is not None:
        temp = temp[temp['cuisine'] == cuisine]
    temp.loc[:,'score'] = temp['ingredients'].apply(lambda row: count_common(row, available_ingredients))
    temp = temp.sort_values(by=['score','rating'], ascending=False)
    temp.to_csv('temp.csv')
    result = temp.iloc[:min(n, len(temp)), 0]
    return result
