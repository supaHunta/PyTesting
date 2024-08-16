import requests
import pytest
import rand


token = None
refreshToken = None
user_id = None
favorites = []

BASE_API_URL = "http://localhost:4000"
BASE_API_SIGNIN = f'{BASE_API_URL}/auth/signin'
BASE_API_SIGNUP = f'{BASE_API_URL}/auth/signup'
BASE_API_BOOK_GET_FAV_URL = f'{BASE_API_URL}/book/favorites'
BASE_API_BOOK_ADD_FAV_URL = f'{BASE_API_URL}/book/add-favorites'
BASE_API_BOOK_REM_FAV = f'{BASE_API_URL}/book/remove-favorites'
BASE_API_CHECK_TOKEN = f'{BASE_API_URL}/auth/check-token'
base_api_user = None
def get_user_url(x): return f'{BASE_API_URL}/user/{1}'



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
    return token


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
    response = requests.get(BASE_API_BOOK_GET_FAV_URL, headers=headers)
    response_json = response.json()
    print('\n->> resp1', response_json)
    body = {'bookId': 1}
    for item in response_json:
        if body.get('bookId') == item.get('bookId'):
            raise Exception('Book already exists')
    response = requests.post(
        BASE_API_BOOK_ADD_FAV_URL, json=body, headers=headers)
    requests.post(
        'http://localhost:4000/auth/check-token', json={'refreshToken': refreshToken})
    assert response.status_code == 200

    response = requests.get(BASE_API_BOOK_GET_FAV_URL, headers=headers)
    response_json = response.json()
    print('\n->> resp2', response_json)
    
    was_book_found = False
    for item in response_json:
        if body.get('bookId') == item.get('bookId'):
            was_book_found = True

    assert was_book_found == True
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


def test_08_change_profile_image():
    response = requests.get('http://localhost:4000/user/1', headers = {'Authorization': f'Bearer {token}'})
    photo_response = response.json()
    current_result = photo_response.get('data',{}).get("user",{}).get('avatar')
    print(current_result)
    response = requests.get('http://localhost:4000/user/1', headers = {'Authorization': f'Bearer {token}'})
    photo_response = response.json()
    second_result = photo_response.get('data',{}).get("user",{}).get('avatar')
    print(second_result)