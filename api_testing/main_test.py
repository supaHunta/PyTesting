import requests
import rand
import pytest


class TestRegistration:
    def test_registration(self):
        body = {"email": rand.generate_random_email(8), "password": "180175Ilya"}
        response = requests.post("http://localhost:3000/signup", json=body)
        assert response.status_code == 201
        assert response.json().get('message') == 'User created!'
        assert response.json().get('id')
        assert isinstance(response.json().get('id'), int)
        print(response.text)
