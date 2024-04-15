import requests
from PIL import Image
from io import BytesIO


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


if __name__ == '__main__':
    image_data = scrape_image('https://pinchofyum.com/wp-content/uploads/Pumpkin-Muffins-with-Cream-Cheese-Filling-10-1365x2048.jpg')
    save_image(image_data=image_data)
