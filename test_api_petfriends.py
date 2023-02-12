from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password, valid_email_2, valid_password_2
import os

pf = PetFriends()

# Примеры тестов из модуля
#1
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем, что запрос api ключа возвращает статус 200 и в результате содержится слово 'key'"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert "key" in result

#2
def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем, что запрос всех питомцев возвращает не пустой список.
    Сначала получаем api ключ, который сохраняем в переменную auth_key. Далее, используя этого ключ,
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

#3
def test_add_new_pet_with_valid_data(name='Gena', animal_type='кот',
                                     age='3', pet_photo='images/cat.jpg'):
    """Проверяем, что можно добавить питомца с корректными данными"""

    # Полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

#4
def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "GrumpyCat", "cat", '7', 'images/cat.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Проверяем, что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

#5
def test_successful_update_self_pet_info(name='Goga', animal_type='smurf', age=13):
    """Проверяем возможность обновления информации о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


# Тесты для самостоятельного задания
# 01
def test_get_api_key_for_valid_user_and_invalid_password(email=valid_email, password=invalid_password):
    """ Проверяем, что запрос api ключа возвращает статус 403 при условии, что auth_key неверный"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert "key" not in result

# 02
def test_get_api_key_for_invalid_user_and_invalid_password(email=invalid_email, password=invalid_password):
    """ Проверяем, что запрос api ключа возвращает статус 403 при условии, что Пользователь не существует"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert "key" not in result

# 03
def test_get_empty_list_of_pets_with_valid_key(filter='my_pets'):
    """ Проверяем, что запрос наших питомцев возвращает без ошибок пустой список, если нет добавленных животных.
    Используем альтернативные данные учетной записи_2 без добавленных ранее животных.
        Значение параметра filter - 'my_pets'"""
    _, auth_key = pf.get_api_key_for_emty_list(valid_email_2, valid_password_2)
    status, result = pf.get_list_of_pets(auth_key, filter)
    print(result)
    assert status == 200
    assert len(result['pets']) == 0

# 04
def test_add_new_pet_without_photo_with_valid_data(name='Karl', animal_type='monkey',
                                     age='10'):
    """Проверяем, что можно добавить питомца с корректными данными без фото"""

    # Полный путь изображения питомца и сохраняем в переменную pet_photo
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


# 05
def test_add_photo_for_the_pet_with_valid_data(pet_photo='images/monkey.jpg'):
    """Проверяем, что можно добавить фото с корректными данными к существующему питомцу"""
    # Полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)
    assert status == 200
    assert result['pet_photo'] is not None


# 06
def test_successful_update_ago_added_pet_info(name='Жора', animal_type='Попугай', age=9):
    """Проверяем возможность обновления информации о давно добавленном питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Если список не пустой, то пробуем обновить имя, тип и возраст у 3-го по списку питомца
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][-3]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

# 07
def test_add_new_pet_with_negative_age(name='Qubasic', animal_type='bird',
                                     age='-33', pet_photo='images/coderbird.jpg'):
    """Проверяем, что можно добавить питомца с отрицательным возрастом"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

# 08
def test_add_new_pet_with_empty_fields(name='', animal_type='',
                                     age=''):
    """Проверяем, что можно добавить питомца с пустыми данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

# 09
def test_add_new_pet_with_unicode_symbols(name='関東弁五人の会社員اللغة العربية', animal_type='ภาษาไทย δθφ',
                                     age='①❸⓷¾', pet_photo='images/dog.jpg'):
    """Проверяем, что можно при добавлении питомца поля принимают различные символы"""

    # Полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

# 10

def test_successful_delete_self_pet_by_position():
    """Проверяем возможность удаления питомца по номеру в списке"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "GrumpyCat", "cat", '7', 'images/cat.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Берём id 2-го с конца по списку питомца и отправляем запрос на удаление
    pet_id = my_pets['pets'][1]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Проверяем, что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()





# 11
def test_successful_delete_group_pet_by_position():
    """Проверяем возможность массового удаления питомцев по номерам в списке"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']

    # Берём id с 1-го до 100-го с конца по списку питомца и отправляем запрос на удаление
    while len(my_pets['pets']) > 20:
        for num in range(100):
            pet_id = my_pets['pets'][num]['id']
            pf.delete_pet(auth_key, pet_id)
    else:
        status, _ = pf.delete_pet(auth_key, pet_id)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем, что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()