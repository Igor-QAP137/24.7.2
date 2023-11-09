from api import PetFriends
from settings import valid_email, valid_password
import os


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Kuza', animal_type='Cat', age='5', pet_foto='images/Kuza.jpg'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_foto)

    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0:
       pf.add_new_pet(auth_key, 'Garry', 'Cat', '6', 'images/Garry.jpg')
       _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Mars', animal_type='Cat', age=8):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

    # 10 Тестов

    # 1 "Тест на получение api ключа при неверном E-mail"
def test_get_api_key_for_nonvalid_user(email="nonvalid@maaail.com", password=valid_password):

    status, result = pf.get_api_key(email, password)

    assert status == 403


    # 2 "Тест на получение api ключа при неверном пароле"
def test_get_api_key_for_nonvalid_password(email=valid_email, password="nonvalid"):

    status, result = pf.get_api_key(email, password)

    assert status == 403

    # 3 "Тест на получение списка найденных животных при неверном auth_key"
def test_get_list_of_pets_for_nonvalid_key(filter=''):

    auth_key = {"key": "nonvalid auth_key"}
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 403

    # 4 "Тест на добавление животного на сайт при неверном auth_key"
def test_add_new_pet_with_nonvalid_key(name='Kuza', animal_type='Cat', age='5', pet_photo='images/Kuza.jpg'):

    auth_key = {"key": "nonvalid auth_key"}
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 403

    # 5 "Тест на удаление питомца при неправильном auth_key"
def test_successful_delete_self_pet_with_nonvalid_key():

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Mars", "Cat", "8", "images/Mars.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    auth_key = {"key": "nonvalid auth_key"}
    status, _ = pf.delete_pet(auth_key, pet_id)

    assert status == 403

    # 6 "Тест на добавление питомца без фото с корректными данными"
def test_add_new_pet_simple_with_valid_data(name='Garry', animal_type='Cat', age='6'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

    # 7 "Тест на добавление питомца с неверным auth_key"
def test_add_new_pet_with_nonvalid_key(name='Kuza', animal_type='Cat', age='3'):

    auth_key = {"key": "nonvalid auth_key"}
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    assert status == 403

    # 8 "Тест на добавление фото питомца с корректными данными"
def test_add_new_pet_without_photo_and_valid_data(pet_photo='images/Garry.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    pf.add_new_pet_simple(auth_key, "Garry", "Cat", "6")
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)

    assert status == 200

    # 9 "Тест на добавление фото питомца при неверном auth_key"
def test_add_new_pet_without_photo_and_nonvalid_key(pet_photo='images/Garry.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    pf.add_new_pet_simple(auth_key, "Garry", "Cat", "5")
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']

    auth_key = {"key": "nonvalid auth_key"}

    status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)

    assert status == 403

    # 10 "Тест на обновление информации о питомце при неверном auth_key"
def test_unsuccessful_update_self_pet_info_with_nonvalid_key(name='Mars', animal_type='Cat', age=8):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    auth_key = {"key": "nonvalid auth_key"}

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 403

    else:
        raise Exception("There is no my pets")