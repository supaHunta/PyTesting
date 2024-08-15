import requests
import pytest
import rand


token = None
refreshToken = None
user_id = None

BASE_API_URL = "http://localhost:4000"
BASE_API_SIGNIN = f'{BASE_API_URL}/auth/signin'
BASE_API_SIGNUP = f'{BASE_API_URL}/auth/signup'
BASE_API_BOOK_FAV = f'{BASE_API_URL}/book/add-favorites'
BASE_API_BOOK_REM_FAV = f'{BASE_API_URL}/book/remove-favorites'
BASE_API_CHECK_TOKEN = f'{BASE_API_URL}/auth/check-token'
base_api_user = None
# = f'{BASE_API_URL}/user/1'
def get_user_url(x): return f'{BASE_API_URL}/user/{1}'
# def set_user_url(id):
#     BASE_API_USER = f'{BASE_API_URL}/user/{id}'

# def setUp():
#     print("setUp")


def test_01_registration():
    '''
    This test exists to check out the registration of the new User
    '''
    global token, refreshToken, base_api_user, email, user_id
    email = rand.generate_random_email(6)
    headers = {"Connection": 'keep-alive'}
    body = {"email": email, "password": "180175Ilya"}
    response = requests.post(
        BASE_API_SIGNUP, json=body, headers=headers)
    response_json = response.json()
    token = response_json.get("token", None)
    refreshToken = response_json.get("refreshToken")
    user_id = response_json.get('user', {}).get('id', None)
    assert response.status_code == 201
    assert response_json.get("message").lower() == "user created!"
    assert user_id is not None
    assert token is not None
    # set_user_url(user_id)
    base_api_user = f'{BASE_API_URL}/user/{user_id}'
    print('\n\nbase_api_user', base_api_user, '\n')
    print("test_registration >>>> ", response.text)


def test_02_authorization():
    global token, refreshToken
    headers = {"Connection": 'keep-alive'}
    body = {"email": "super.neyt@yandex.ru", "password": "180175Ilya"}
    response = requests.post(
        BASE_API_SIGNIN, json=body, headers=headers)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json.get("message").lower() == "you are signed in"
    token = response_json["token"]
    refreshToken = response_json['refreshToken']
    print('\n\ntest_02_authorization', response.text, "\n")


def test_03_invalid_registration():
    body = {"email": "2cw4rc1d2@gma", "password": "180175Ilya"}
    response = requests.post(
        BASE_API_SIGNUP, json=body)
    response_json = response.json()
    assert response.status_code == 400
    print('\n\ntest_03_invalid_registration', response.text, '\n')


def test_04_invalid_authorization():
    body = {"email": "2cejio3i0j@gmail.com", "password": "180175Ilya"}
    response = requests.post(
        BASE_API_SIGNIN, json=body)
    response_json = response.json()
    assert response.status_code == 404
    assert response_json.get("data", {}).get(
        'message').lower() == "user with this email not found"
    print('\n\ntest_04_invalid_authorization', response.text, '\n')


def test_05_add_favorites():
    headers = {'Authorization': f'Bearer {token}', "Connection": 'keep-alive'}
    body = {'bookId': 1}
    response = requests.post(
        BASE_API_BOOK_FAV, json=body, headers=headers)
    requests.post(
        'http://localhost:4000/auth/check-token', json={'refreshToken': refreshToken})
    assert response.status_code == 200
    print('\n\ntest_05_add_favorites', response.text, '\n')
    # print(token_response.text)


def test_06_remove_favorites():
    headers = {'Authorization': f'Bearer {token}'}
    body = {'bookId': 1}
    response = requests.delete(
        BASE_API_BOOK_REM_FAV, json=body, headers=headers)
    token_response = requests.post(
        BASE_API_CHECK_TOKEN, json={'refreshToken': refreshToken})
    assert response.status_code == 202
    print('\n\ntest_06_remove_favorites', response.text, '\n')


def test_07_rename_user():
    headers = {'Authorization': f'Bearer {token}'}
    name = rand.generate_random_wrong_email(5)
    body = {"email": email,
            "name": name}
    response = requests.patch(base_api_user, json=body, headers=headers)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json.get("user", {}).get("name") == name
    print('\ntest_07_rename_user', response.text)
    print(f"User {user_id} is now {name}")
