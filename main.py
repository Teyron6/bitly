from urllib.parse import urlparse
import requests
import argparse
from dotenv import load_dotenv
import os


def shorten_link(token, url):
    shorten_url = 'https://api-ssl.bitly.com/v4/shorten'
    params = {
        "long_url": url,
    }
    headers = {
        "Authorization": f"Bearer {token}",
    }
    response = requests.post(shorten_url, headers=headers, json=params)
    response.raise_for_status()

    return response.json()['link']


def count_clicks(token, bitlink):
    clicks_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    params = {
        'unit': 'month',
        'units': '-1',
    }
    headers = {
        "Authorization": f"Bearer {token}",
    }
    response = requests.get(clicks_url, params=params, headers=headers)
    response.raise_for_status()

    return response.json()['total_clicks']


def is_bitlink(token, url):
    bit_url = f'https://api-ssl.bitly.com/v4/bitlinks/{url}'
    headers = {
        "Authorization": f"Bearer {token}",
    }
    response = requests.get(bit_url, headers=headers)
    return response.ok


def main():
    load_dotenv
    token = os.getenv('BITLY_TOKEN')
    parser = argparse.ArgumentParser(description='Эта программа может сокротить ссылки и получать количество кликов по сокращенной ссылке. Для того что бы сократить ссылку надо ввесть "--url" и вставить обычную ссылку, после этого в терминал выведеться сокращенная ссылка. Что бы получить количество кликов по ссылке надо также написать "--url" и ввести уже сокращенную ссылку, тогда вам выведеться количество кликов по ссылке')
    parser.add_argument('--url', help='Введите ссылку')
    args = parser.parse_args()
    parsed_url = urlparse(args.url)
    parsed_url = f'{parsed_url.netloc}{parsed_url.path}'

    try:
        if not is_bitlink(token, parsed_url):
            print(shorten_link(token, args.url))
        else:
            print(count_clicks(token, parsed_url))
    except requests.exceptions.HTTPError:
        print('Ой! Что то пошло не так. Проверьте вашу ссылку, скорее всего ошибка в ней.')


if __name__ == '__main__':
    main()

