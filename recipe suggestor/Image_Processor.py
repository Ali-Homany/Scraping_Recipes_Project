import requests
from PIL import Image
from io import BytesIO
import base64


def scrape_image(img_url):
    image_response = requests.get(img_url)
    image_data = image_response.content
    return image_data


def image_to_string(image_data):
    image = Image.open(BytesIO(image_data))
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format=image.format)
    encoded_data = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
    return encoded_data


def scrape_image_as_string(img_url):
    '''
    Args:
        - img_url (str): src link or the image
    Returns:
        (str) string containing the base64 encoded image data.
    '''
    try:
        image_data = scrape_image(img_url=img_url)
        image_string = image_to_string(image_data=image_data)
        return image_string
    except Exception as e:
        print('image retrieving failed because:\n', e)
        return 'image retrieving failed'


if __name__ == '__main__':
    image_data = scrape_image('https://pinchofyum.com/wp-content/uploads/Pumpkin-Muffins-with-Cream-Cheese-Filling-10-1365x2048.jpg')
    image_string = image_to_string(image_data)
    print(image_string)
