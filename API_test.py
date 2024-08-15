import requests
import pytest
import rand


token = "none"
refrToken = "none"

BASE_API_URL = "http://localhost:4000"
BASE_API_SIGNIN = f'{BASE_API_URL}/auth/signin'
BASE_API_SIGNUP = f'{BASE_API_URL}/auth/signup'
BASE_API_BOOK_FAV = f'{BASE_API_URL}/book/add-favorites'
BASE_API_BOOK_REM_FAV = f'{BASE_API_URL}/book/remove-favorites'
BASE_API_CHECK_TOKEN = f'{BASE_API_URL}/auth/check-token'
BASE_API_USER_1 = f'{BASE_API_URL}/user/1'


def setUp():
    print("setUp")


def test_registration():
    '''
    This test exists to check out the registration of the new User
    '''
    global token, refrToken
    headers = {"Connection": 'keep-alive'}
    body = {"email": rand.generate_random_email(6), "password": "180175Ilya"}
    response = requests.post(
        BASE_API_SIGNUP, json=body, headers=headers)
    json = response.json()
    token = json["token"]
    refrToken = json['refreshToken']
    assert response.status_code == 201
    print(response.text)


def test_authorization():
    global token, refrToken
    headers = {"Connection": 'keep-alive'}
    body = {"email": "super.neyt@yandex.ru", "password": "180175Ilya"}
    response = requests.post(
        BASE_API_SIGNIN, json=body, headers=headers)
    assert response.status_code == 200
    json = response.json()
    token = json["token"]
    refrToken = json['refreshToken']
    print(response.text)


def test_invalid_registration():
    body = {"email": "2cw4rc1d2@gma", "password": "180175Ilya"}
    response = requests.post(
        BASE_API_SIGNUP, json=body)
    assert response.status_code == 400
    print(response.text)


def test_invalid_authorization():
    body = {"email": "2cejio3i0j@gmail.com", "password": "180175Ilya"}
    response = requests.post(
        BASE_API_SIGNIN, json=body)
    assert response.status_code == 404
    print(response.text)


def test_zadd_favorites():
    headers = {'Authorization': f'Bearer {token}', "Connection": 'keep-alive'}
    body = {'bookId': 1}
    response = requests.post(
        BASE_API_BOOK_FAV, json=body, headers=headers)
    requests.post(
        'http://localhost:4000/auth/check-token', json={'refreshToken': refrToken})
    assert response.status_code == 200
    print(response.text)
    # print(token_response.text)


def test_zremove_favorites():
    headers = {'Authorization': f'Bearer {token}'}
    body = {'bookId': 1}
    response = requests.delete(
        BASE_API_BOOK_REM_FAV, json=body, headers=headers)
    token_response = requests.post(
        BASE_API_CHECK_TOKEN, json={'refreshToken': refrToken})
    assert response.status_code == 202


def test_rename_user():
    headers = {'Authorization': f'Bearer {token}'}
    body = {"email": "super.neyt@yandex.ru",
            "name": rand.generate_random_wrong_email(5)}
    response = requests.patch(BASE_API_USER_1, json=body, headers=headers)
    assert response.status_code == 200


def tearDown():
    print("tearDown")
