import json
import random
import pytest
import requests
from faker import Faker

@pytest.fixture
def fix_a():
    fake = Faker()
    pet_id = random.randint(1, 99999999999999)
    input_pet = {
        "id": pet_id,
        "category": {
            "id": random.randint(1, 99999999999999),
            "name": fake.name()
        },
        "name": "doggie",
        "photoUrls": [
            "string"
        ],
        "tags": [
            {
                "id": random.randint(1, 99999999999999),
                "name": fake.name()
            }
        ],
        "status": "available"
    }
    header = {'accept': 'application/json', 'Content-Type': 'application/json'}
    return pet_id, input_pet, header


@pytest.fixture
def yield_fix(fix_a):
    pet_id, input_pet, header = fix_a
    requests.post(url='https://petstore.swagger.io/v2/pet', data=json.dumps(input_pet), headers=header)
    print("Add pet")
    yield pet_id, input_pet
    requests.delete(url=f'https://petstore.swagger.io/v2/pet/{pet_id}',
                    headers={'accept': 'application/json'})
    print("Del pet")



