import json
import random
import pytest
import requests
from faker import Faker


# оформление через фикстуры
@pytest.fixture
def fix():
    input_pet = {
        "id": 2022,
        "category": {
            "id": 12,
            "name": "Jora"
        },
        "name": "doggie",
        "photoUrls": [
            "string"
        ],
        "tags": [
            {
                "id": 31,
                "name": "Cat"
            }
        ],
        "status": "available"
    }

    header = {'accept': 'application/json', 'Content-Type': 'application/json'}
    return input_pet, header


def test_add_pet_fix(fix):
    input_pet, header = fix
    res_post = requests.post(url='https://petstore.swagger.io/v2/pet', data=json.dumps(input_pet), headers=header)
    print(res_post)
    res_json = json.loads(res_post.text)
    assert input_pet == res_json


# PetStore

# добавить животное
def test_add_pet():
    input_pet = {
        "id": 2022,
        "category": {
            "id": 12,
            "name": "Jora"
        },
        "name": "doggie",
        "photoUrls": [
            "string"
        ],
        "tags": [
            {
                "id": 31,
                "name": "Cat"
            }
        ],
        "status": "available"
    }

    header = {'accept': 'application/json', 'Content-Type': 'application/json'}

    res_post = requests.post(url='https://petstore.swagger.io/v2/pet', data=json.dumps(input_pet), headers=header)
    print(res_post)
    res_json = json.loads(res_post.text)
    assert input_pet == res_json

    # проверить добавление животного
    res_get = requests.get(url=f'https://petstore.swagger.io/v2/pet/{input_pet["id"]}')
    assert res_get.status_code == 200
    assert json.loads(res_get.text) == input_pet

    # удаление животного
    res_delete = requests.delete(url=f'https://petstore.swagger.io/v2/pet/{input_pet["id"]}')
    out_del = {
        "code": 200,
        "type": "unknown",
        "message": "2022"
    }
    assert json.loads(res_delete.text) == out_del


def test_available_list():
    input_pet = {
        "id": 2910192,
        "category": {
            "id": 12,
            "name": "Gena"
        },
        "name": "parrot",
        "photoUrls": [
            "string"
        ],
        "tags": [
            {
                "id": 31,
                "name": "jako"
            }
        ],
        "status": "available"
    }

    header = {'accept': 'application/json', 'Content-Type': 'application/json'}

    requests.post(url='https://petstore.swagger.io/v2/pet', data=json.dumps(input_pet), headers=header)

    res_get = requests.get(url=f'https://petstore.swagger.io/v2/pet/findByStatus', params={'status': 'available'})
    assert res_get.status_code == 200
    assert input_pet in list(json.loads(res_get.text))
    print(list(json.loads(res_get.text)))


# оформление через фикстуры


def test_add_pet_1(fix_a):
    pet_id, input_pet, header = fix_a
    print(pet_id)
    # создание питомца
    res_post = requests.post(url='https://petstore.swagger.io/v2/pet', data=json.dumps(input_pet), headers=header)
    assert res_post.status_code == 200
    assert res_post.json() == input_pet
    # проверка записи в БД
    res_get = requests.get(url=f'https://petstore.swagger.io/v2/pet/{pet_id}', headers={'accept': 'application/json'})
    assert res_get.status_code == 200
    assert res_get.json() == res_post.json() == input_pet
    # удаление питомца из БД
    res_delete = requests.delete(url=f'https://petstore.swagger.io/v2/pet/{pet_id}',
                                 headers={'accept': 'application/json'})
    assert res_delete.status_code == 200
    assert res_delete.json()['message'] == str(pet_id)
    # проверка удаления из БД
    res_get = requests.get(url=f'https://petstore.swagger.io/v2/pet/{pet_id}', headers={'accept': 'application/json'})
    assert res_get.status_code == 404
    assert res_get.json()['message'] == "Pet not found"


def test_yield_fix(yield_fix):
    pet_id, input_pet = yield_fix
    print(pet_id)
    res_get = requests.get(url=f'https://petstore.swagger.io/v2/pet/{pet_id}', headers={'accept': 'application/json'})
    print('Get pet')
    assert res_get.status_code == 200
    assert res_get.json() == input_pet



