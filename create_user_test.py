import sender_stand_request
import data


def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["first_name"] = first_name
    return current_body


# Функция для позитивной проверки
def positive_assert(first_name):
    user_body = get_user_body(first_name)                                           # В переменную user_body сохраняется обновленное тело запроса
    user_response = sender_stand_request.post_new_user(user_body)                   # В переменную user_response сохраняется результат запроса на создание пользователя:

    assert user_response.status_code == 201                                         # Проверяется, что код ответа равен 201
    assert user_response.json()["authToken"] != ""                                  # Проверяется, что в ответе есть поле authToken, и оно не пустое

    users_table_response = sender_stand_request.get_users_table()                   # В переменную users_table_response сохраняется результат запроса на получение данных из таблицы user_model

    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]   # Строка, которая должна быть в ответе

    assert users_table_response.text.count(str_user) == 1                           # Проверка, что такой пользователь есть, и он единственный



# Функция для негативной проверки
def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)                                                                   # В переменную user_body сохраняется обновлённое тело запроса
    response = sender_stand_request.post_new_user(user_body)                                                # В переменную response сохраняется результат запроса

    assert response.status_code == 400                                                                      # Проверка, что код ответа равен 400
    assert response.json()["code"] == 400                                                                   # Проверка, что в теле ответа атрибут "code" равен 400
    assert response.json()["message"] == "Имя пользователя введено некорректно. " \
                                         "Имя может содержать только русские или латинские буквы, " \
                                         "длина должна быть не менее 2 и не более 15 символов"              # Проверка текста в теле ответа в атрибуте "message"


# Функция для негативной проверки
# В ответе ошибка: "Не все необходимые параметры были переданы"
def negative_assert_no_first_name(user_body):                                           # В переменную response сохрани результат вызова функции
    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400                                                  # Проверь, что код ответа — 400
    assert response.json()["code"] == 400                                               # Проверь, что в теле ответа атрибут "code" — 400
    assert response.json("message") == "Не все необходимые параметры были переданы"     # Проверь текст в теле ответа в атрибуте "message"


# "Тест 1. Успешное создание пользователя"
# Параметр fisrtName состоит из 2 символов
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")


# "Тест 2. Успешное создание пользователя"
# Параметр fisrtName состоит из 15 символов
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Ааааааааааааааа")


# "Тест 3. Ошибка"
# Параметр fisrtName состоит из 1 символа
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")


# "Тест 4. Ошибка"
# Параметр fisrtName состоит из 16 символов
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Аааааааааааааааа")


# "Тест 5. Успешное создание пользователя"
# Параметр fisrtName состоит из английских букв
def test_create_user_english_letter_in_first_name_get_success_response():
    positive_assert("QWErty")


# "Тест 6. Успешное создание пользователя"
# Параметр fisrtName состоит из русских символов
def test_create_user_russian_letter_in_first_name_get_success_response():
    positive_assert("Мария")


# "Тест 7. Ошибка"
# Параметр fisrtName состоит из слов с пробелами
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("Человек и Ко")


# "Тест 8. Ошибка"
# Параметр fisrtName состоит из специсимволов
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("№%@")


# "Тест 9. Ошибка"
# Параметр fisrtName состоит из цифр
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")


# "Тест 10. Ошибка"
# В запросе нет параметра firstName
def test_create_user_no_first_name_get_error_response():
    user_body = data.user_body.copy()           # Копируется словарь с телом запроса из файла data в переменную user_body
                                                # Иначе можно потерять данные из исходного словаря

    user_body.pop("firstName")                  # Удаление параметра firstName из запроса
    negative_assert_no_first_name(user_body)    # Проверка полученного ответа


# "Тест 11. Ошибка"
# Параметр fisrtName состоит из пустой строки
def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body("")                              # В переменную user_body сохраняется обновлённое тело запроса
    negative_assert_no_first_name(user_body)                   # Проверка полученного ответа


# "Тест 12. Ошибка"
# Параметр fisrtName состоит из
def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)                               # В переменную user_body сохраняется обновлённое тело запроса
    response = sender_stand_request.post_new_user(user_body)    # В переменную user_response сохраняется результат запроса на создание пользователя
    assert response.status_code == 400                          # Проверка кода ответа