import pandas as pd
import webbrowser
import random


def create_steps(recipe):
    result = '<ol>'
    for step in recipe['steps']:
        result += f'<li>{step}</li>'
    result += '</ol>'
    return result


def create_ingredients(recipe):
    result = '<ul>'
    for ingredient in recipe['ingredients']:
        result += f'<li>{ingredient}</li>'
    result += '</ul>'
    return result


def build_recipe_page(recipe):
    recipe_name = recipe['title']
    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta http-equiv="X-UA-Compatible" content="IE=edge">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <style>
            @import url('https://fonts.googleapis.com/css2?family=Finger+Paint&family=Dancing+Script:wght@700&family=Solway:wght@300;400;500;700;800&family=Leckerli+One&family=Tangerine:wght@400;700&family=Work+Sans:ital,wght@0,100;0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap');
            /* 
            font-family: 'Finger Paint', sans-serif; for some buttons, a bit cute & funny
            font-family: 'Solway', serif; for lists, nice & clean
            font-family: 'Dancing Script', cursive; handwriting-like font for the slogan
            font-family: 'Work Sans', sans-serif; for most stuff
            font-family: 'Leckerli One', cursive; for recipe name in recipe page
            */



            /* colors, fonts.. all common stuff btw the 3 pages */
            :root{
            --gold: #B68D13;
            --brown: #3B2200;
            --grey: #D6D6D6;
            --pink: #FF86DA;
            --orange: #FFC720;
            }


            /* we can use any of these colors in any other file, this is an example:
            .selected{
            color: var(--gold);
            }
            */


            /* some common styling */
            *{
            margin:0;
            padding:0;
            font-family: 'Work Sans', sans-serif;
            }
            a{
            color: inherit;
            font-size: inherit;
            }


            </style>
            <style>
            body {
                background-image: linear-gradient(to bottom, rgba(182, 141, 19), rgba(255, 255, 255, 0));
                text-align: center;
                margin: 0;
            }


        .recipe-name{
            position: sticky;
            top: 0;
            display: flex;
            width: 100%;
            justify-content:space-around;
            align-items: center;
            background-color: var(--gold);
            margin-top: 0;
            margin-bottom: 5px;
            height:50px;
            color: white;
            font-family: 'Leckerli One', cursive;
            font-weight: 400;
            text-transform: capitalize;
            box-shadow: 0 5px 8px rgba(0, 0, 0, 0.553);
        }
        .recipe-name h2{
            font-weight: inherit;
        }
        .recipe-name svg{
            height: 50px;
            aspect-ratio: 1/1;
            fill: white;
            translate: 0% 20%;
        }

        .step-container {
            display: flex;
            flex-direction: column; 
            margin:20px 20px;

        }

        /* step number */
        .step-box {
            background-color:var(--brown);
            padding: 10px;
            border-radius: 20px;
            margin-bottom: 10px;
            width:fit-content;
            color: white;
            font-family: 'Finger Paint', sans-serif;
        }

        /* details tb3 recipe */
        .details-box {
            background-color:rgba(255, 255, 255, 0.5); 
            border: solid var(--brown);
            color: var(--brown);
            font-family: 'Work Sans', sans-serif;
            padding: 15px;
            border-radius: 20px;
            height:100px;
        }

        /* previous home next container */
        .navigation-container {
            display: flex;
            justify-content: space-around;
            align-items: center;
            margin-bottom: 50px;
        }

        /* previous next */
        .navigation-box {
            padding: 10px;
            margin: 0 10px;
            border-radius:50%; 
            height:40px; 
            width:40px;
        }

        /* svg style for prev next */
        .navigation-box svg{
            width: 40px;
            height: 40px;
            fill:white;
            border: solid var(--brown);
            border-radius: 50%;
            filter: drop-shadow(2px 2px 10px rgba(255, 255, 255, 0,5));
        }

        /* division tb3 l home */
        #home{
            height:20px;
            width:20px;
            background-color:var(--brown);
        }

        #home svg{
            width: 20px;
            height: 20px;
            fill:white;
            border: none;
        }

        /* l container tb3 l edit w delete */
        .additional-buttons {
            display: flex;
            flex-direction: column;
            justify-content: center;
            margin-bottom: 10px ;
        }

        /* edit delete buttons */
        .additional-button {
            margin: 0 10px;
            padding: 5px;
            background-color: none;
        }
        /* style lal svg  */
        .additional-button svg{
            height: 20px;
            width:20px;
            fill: white;
        }


        .top{
            display: flex;
            flex-direction: row;
            justify-content:left;
            margin-bottom: 5px;
            margin-left: 20px;
            width: auto;
        }


        .ingredients-box {
            background-color: var(--brown); 
            padding: 8px;
            border-radius: 20px;
            width: 100px; 
            font-family: 'Finger Paint', sans-serif;
            text-transform: capitalize;
            color:white;
        }

        /* margin right is to center manuallly the box based on ingredients container */
        .big-container{
            display: flex;
            justify-content: left;
            margin-right: 50px;
            margin-left: 20px;
        }


        /* contains list of ingredients m3 l share w copy buttons */
        .ingredients-container{
            background-color:white;
            border: solid var(--brown);
            border-radius: 15px;
            width:500px;
        }

        .list-container {
            text-align: center;
            font-family: 'Solway', serif;
            font-weight: bold;
            color:var(--brown);
            margin: 30px ;
        }

        ul{
            width: fit-content;
        }

        .list-item {
            margin-bottom: 15px;
        }

        /* container lal copy w share buttons */
        .icons-container {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }

        /* style buttons */
        .icon {
            width:50px;
            margin: 10px 10px;
            fill:var(--brown);
            padding: 5px;
            border-radius: 5px;
        }

        /* la kl l buttons */
        button{
            border:none;
            outline:none;
            background-color: transparent;
        }

        #prevStep{
            visibility: hidden;
        }
      </style>
      <style>
        .details-box{
            height: fit-content;
            margin-left: 60px;
            margin-right: 60px;
        }
        ol, ul{
            margin-left: 30px;
            width: fit-content;
            text-align:left;
            color: rgba(41, 24, 0, 1);
            font-weight: 600;
        }
        .big-container{
            margin-right:0;
            margin-bottom: 30px;
        }
        #bg{
        """ + f"background-image: linear-gradient(to top, rgb(0, 0, 0) 5% , rgba(255, 255, 255, 0)), url({recipe['image_link']});" + """
            min-height: 100vh;
            height:fit-content;
            background-attachment: fixed;
            background-size:cover;
            background-position:center;
            text-align: left;
            padding-bottom: 20px;
            margin: 0;
        }
        .recipe-name svg{
            transform: translate(0, -4px);
        }
        html{
            min-height:100vh;
            height: fit-content;
            padding: 0;
            width:100%;
            background-color:white;
        }
        body{
            min-height:100vh;
            height: fit-content;
            width:100%;
        }
        li {
            margin-bottom: 10px;
        }
      </style>
      <title>Recipe</title>
    </head>
    <body>
      <div id="bg">
      <!-- header of the page -->
      <div class="recipe-name">
      <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
      viewBox="0 0 122.7 131.2" style="enable-background:new 0 0 122.7 131.2;" xml:space="preserve">
     <path d="M46.1,1.5c-5.3,2.1-9.6,6.3-10.8,10.6c-1,3.3-1.8,4.3-3.6,4.3c-1.2,0-4.5,1.4-7.2,3.1c-5.8,3.6-10.5,12.1-10.5,18.8
     c0,7.8,6,14.6,13.1,15c5,0.2,4.5-2.5-0.8-4.3c-5.6-1.9-8-5-8-10.3c0-7.8,5.8-16,12.7-18c3.2-0.9,3.5-0.8,4.9,2.6
     c2,4.8,6.9,8.6,8.9,6.9c1.3-1.1,1.1-1.6-1.2-3.4C34,18.6,38.8,6.7,52.7,4.1c4.9-0.9,11.9,1,15.7,4.2l3,2.6l-2.5,4.4
     c-2.7,4.7-2.8,9.2-0.2,9.2c0.9,0,1.8-1.5,2.3-3.5C73.5,8.1,93.8,6,102,17.7c1.7,2.3,2.6,5.4,2.9,9.7c0.4,5.5,0.1,6.9-2.4,10.6
     c-3.3,4.9-8.2,7.4-14.6,7.4h-4.4l2.1-2.8c2.7-3.3,4.8-9.7,4-11.7c-1.2-3.1-3.5-1.6-4.3,2.7c-0.9,5.8-6.2,11.8-10.5,11.8
     c-2.8,0-3.1-0.3-2.4-2.5c2.1-6.7-0.6-8.2-3.9-1.9c-1.8,3.6-2.7,4.4-5.4,4.4c-2.1,0-3.8-0.9-4.9-2.7c-1.7-2.6-2.3-10.2-1-12.3
     c0.3-0.6-0.1-1.4-1.1-1.8c-1.1-0.3-2.3,0-2.8,0.9c-1.3,2-1.2,9.9,0.1,13.2c0.9,2.4,0.8,2.8-1.1,2.8c-1.4,0-2.9-1.5-4.3-4.3
     c-1.2-2.4-2.7-4.3-3.2-4.3c-1.9,0-2.3,2.3-0.8,5.3c1.4,2.9,1.4,3.2-0.3,3.6c-2.5,0.6-9.4-6.3-10.6-10.6C32.9,33.4,31.8,32,31,32
     c-2.9,0-2.1,4.5,1.7,10.2l3.9,5.7l-2.3,2.4c-5.2,5.5-4.6,14.4,1.1,19.2c2.8,2.3,3.2,3.4,3.2,8c0,2.9,0.5,5.7,1.2,6.1
     c0.6,0.3,2.5-0.5,4.1-2.1l2.9-2.8l2.8,2.8c3.5,3.6,5.2,2.6,5.2-3.3v-4.8l18-0.2c15.1-0.3,17.9-0.5,17.9-1.9s-2.8-1.6-17.9-1.9
     l-18-0.2v-3.8v-3.8l18-0.2c15.1-0.3,17.9-0.5,17.9-1.9c0-1.4-3.5-1.6-25.8-1.6H39.1l-0.5,4.7c-0.4,3.8-0.8,4.4-1.7,3.2
     c-2.3-2.8-2.8-6.4-1.4-9.7c2.4-5.9,4.7-6.3,32.3-6.3c22,0,25.5-0.3,29.3-2C114,39.9,113.3,15.8,96,7.7c-5.3-2.5-13.5-2.6-17.7-0.4
     c-3,1.5-3.2,1.5-5.9-1.2C70.9,4.6,68,2.7,66,1.8C61.8,0.1,50.2-0.1,46.1,1.5z M50.7,66c1.1,9.9,0.5,12-2.3,9.2
     c-1.1-1.1-1.8-1.1-3.4,0c-2,1.3-2.1,1-2.1-6.2v-7.5h3.6C50.1,61.5,50.3,61.7,50.7,66z"/>
    </svg>
          """ + f"<h2>{recipe_name}</h2>" + """
          <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
        viewBox="0 0 122.7 131.2" style="enable-background:new 0 0 122.7 131.2;" xml:space="preserve">
       <path d="M46.1,1.5c-5.3,2.1-9.6,6.3-10.8,10.6c-1,3.3-1.8,4.3-3.6,4.3c-1.2,0-4.5,1.4-7.2,3.1c-5.8,3.6-10.5,12.1-10.5,18.8
       c0,7.8,6,14.6,13.1,15c5,0.2,4.5-2.5-0.8-4.3c-5.6-1.9-8-5-8-10.3c0-7.8,5.8-16,12.7-18c3.2-0.9,3.5-0.8,4.9,2.6
       c2,4.8,6.9,8.6,8.9,6.9c1.3-1.1,1.1-1.6-1.2-3.4C34,18.6,38.8,6.7,52.7,4.1c4.9-0.9,11.9,1,15.7,4.2l3,2.6l-2.5,4.4
       c-2.7,4.7-2.8,9.2-0.2,9.2c0.9,0,1.8-1.5,2.3-3.5C73.5,8.1,93.8,6,102,17.7c1.7,2.3,2.6,5.4,2.9,9.7c0.4,5.5,0.1,6.9-2.4,10.6
       c-3.3,4.9-8.2,7.4-14.6,7.4h-4.4l2.1-2.8c2.7-3.3,4.8-9.7,4-11.7c-1.2-3.1-3.5-1.6-4.3,2.7c-0.9,5.8-6.2,11.8-10.5,11.8
       c-2.8,0-3.1-0.3-2.4-2.5c2.1-6.7-0.6-8.2-3.9-1.9c-1.8,3.6-2.7,4.4-5.4,4.4c-2.1,0-3.8-0.9-4.9-2.7c-1.7-2.6-2.3-10.2-1-12.3
       c0.3-0.6-0.1-1.4-1.1-1.8c-1.1-0.3-2.3,0-2.8,0.9c-1.3,2-1.2,9.9,0.1,13.2c0.9,2.4,0.8,2.8-1.1,2.8c-1.4,0-2.9-1.5-4.3-4.3
       c-1.2-2.4-2.7-4.3-3.2-4.3c-1.9,0-2.3,2.3-0.8,5.3c1.4,2.9,1.4,3.2-0.3,3.6c-2.5,0.6-9.4-6.3-10.6-10.6C32.9,33.4,31.8,32,31,32
       c-2.9,0-2.1,4.5,1.7,10.2l3.9,5.7l-2.3,2.4c-5.2,5.5-4.6,14.4,1.1,19.2c2.8,2.3,3.2,3.4,3.2,8c0,2.9,0.5,5.7,1.2,6.1
       c0.6,0.3,2.5-0.5,4.1-2.1l2.9-2.8l2.8,2.8c3.5,3.6,5.2,2.6,5.2-3.3v-4.8l18-0.2c15.1-0.3,17.9-0.5,17.9-1.9s-2.8-1.6-17.9-1.9
       l-18-0.2v-3.8v-3.8l18-0.2c15.1-0.3,17.9-0.5,17.9-1.9c0-1.4-3.5-1.6-25.8-1.6H39.1l-0.5,4.7c-0.4,3.8-0.8,4.4-1.7,3.2
       c-2.3-2.8-2.8-6.4-1.4-9.7c2.4-5.9,4.7-6.3,32.3-6.3c22,0,25.5-0.3,29.3-2C114,39.9,113.3,15.8,96,7.7c-5.3-2.5-13.5-2.6-17.7-0.4
       c-3,1.5-3.2,1.5-5.9-1.2C70.9,4.6,68,2.7,66,1.8C61.8,0.1,50.2-0.1,46.1,1.5z M50.7,66c1.1,9.9,0.5,12-2.3,9.2
       c-1.1-1.1-1.8-1.1-3.4,0c-2,1.3-2.1,1-2.1-6.2v-7.5h3.6C50.1,61.5,50.3,61.7,50.7,66z"/>
      </svg>
      </div>
    
      <!--step number m3 step details-->
      <div class="step-container">
          <div class="step-box">Steps</div>
          """ + f'<div class="details-box">{create_steps(recipe)}</div>' + """
      </div>
    
    
      <div class="top"> <!-- contains ingredients title -->
        <div class="ingredients-box">Ingredients</div>
      </div>
      <div class="step-container"> <!-- contains ingredients-list w edit delete share copy buttons-->
        <div class="details-box"> <!--contains list w copy share buttons-->
          
            """ + f"{create_ingredients(recipe)}" + """
          
        </div>
      </div>
    </div>  
    </body>
    </html>
    """
    with open('open_recipe.html', 'w', encoding='utf-8') as file:
        file.write(html_code)
    webbrowser.open('open_recipe.html')


def display_recipe(recipe: pd.Series):
    '''
    This function displays a recipe as html page
    Args
        - recipe (pandas.Series): recipe to be displayed to user
    '''
    build_recipe_page(recipe)


if __name__ == '__main__':
    df = pd.read_json('data.json')
    display_recipe(df.iloc[random.randint(0, 13), :])
