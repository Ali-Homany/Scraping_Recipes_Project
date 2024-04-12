import requests
from PIL import Image
from io import BytesIO
import base64


def scrape_image(image_url):
    '''
    Args:
        image_url (str): link of the image to be scraped
    Returns
        (bytes) data of the image
    '''
    image_response = requests.get(image_url)
    image_data = image_response.content
    return image_data


def save_image(image_data, filename='image.jpg'):
    '''
    This function saves image data as image file
    Args:
        - image_data (bytes): image_data to be saved
        - filename (str): name of the new image file created, default is image.jpg
    '''
    image = Image.open(BytesIO(image_data))
    image.save(filename)


def image_to_string(image_data):
    '''
    Args:
        image_data (bytes)
    Returns
        (str) given image_data as a string
    '''
    image = Image.open(BytesIO(image_data))
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format=image.format)
    encoded_data = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
    return encoded_data


def scrape_image_as_string(image_url):
    '''
    Args:
        - image_url (str): src link or the image
    Returns:
        (str) string containing the base64 encoded image data.
    '''
    try:
        image_data = scrape_image(image_url=image_url)
        image_string = image_to_string(image_data=image_data)
        return image_string
    except Exception as e:
        print('image retrieving failed because:\n', e)
        return 'image retrieving failed'


if __name__ == '__main__':
    image_data = scrape_image('https://pinchofyum.com/wp-content/uploads/Pumpkin-Muffins-with-Cream-Cheese-Filling-10-1365x2048.jpg')
    save_image(image_data=image_data)
