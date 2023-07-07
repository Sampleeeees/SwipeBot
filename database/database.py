from pymongo import MongoClient
from .users import User
from config.config_reader import config

#client = MongoClient(config.mongo_url)
#mydb = client[config.mongo_db]

client = MongoClient()
mydb = client['swipe_tg']



def set_tokens(data: dict, user_id: int) -> None:
    """
    Функція для додавання юзеру токенів або створення нового юзера з токенами
    :param data: Дані в яких буде access, refresh токен
    :param user_id: унікальний id telegram користуача
    :return: повертає None
    """
    user_data = User.find_user(user_id=user_id)
    if user_data:
        user = User(
            user_id=user_data.get('user_id'),
            token=data.get('access'),
            refresh_token=data.get('refresh'),
            is_auth=True,
            language=user_data.get('language')
        )
        user.update()
    else:
        user = User(
            user_id=user_id,
            token=data.get('access'),
            refresh_token=data.get('refresh'),
            is_auth=True,
            language='uk'
        )
        user.save()

async def set_language_user_db(user_id, lang) -> None:
    user_data = User.find_user(user_id=user_id)
    print('user_data', user_data)
    if user_data:
        user = User(
            user_id=user_data.get('user_id'),
            token=user_data.get('token'),
            refresh_token=user_data.get('refresh_token'),
            is_auth=user_data['is_auth'],
            language=lang
        )
        user.update()


def update_token(token: str, user_id: int) -> None:
    """
    Оновлення токену для користувача
    :param token: новий токен
    :param user_id: унікальний id користувача telegram
    :return: None
    """
    user_data = User.find_user(user_id=user_id)
    if user_data:
        user = User(
            user_id=user_data['user_id'],
            token=token,
            refresh_token=user_data['refresh_token'],
            is_auth=user_data['is_auth']
        )
        user.update()


def get_token(user_id: int):
    """
    Отримати токен користувача
    :param user_id: унікальний id користувача telegram
    :return: token user
    """
    user = User.find_user(user_id=user_id)
    return user['token']

def get_refresh_token(user_id: int):
    """
    Отримати refresh токен користувача
    :param user_id: унікальний id користувача телеграма
    :return: User refresh
    """
    user = User.find_user(user_id=user_id)
    return user['refresh_token']


def logout(user_id: int) -> None:
    """
    Вихід з системи
    :param user_id: унікальний id користувача телеграма
    :return: None
    """
    user_data = User.find_user(user_id)
    if user_data:
        user = User(
            user_id=user_data['user_id'],
            token=user_data['token'],
            refresh_token=user_data['refresh_token'],
            is_auth=False,
            language=user_data.get('language')
        )
        user.update()

def is_authenticated(user_id: int) -> bool:
    """
    Перевірка чи авторизований користувач
    :param user_id: унікальний id користувача телеграма
    :return: Bool значення
    """
    user = User.find_user(user_id=user_id)
    print(user)
    if user:
        print(user['is_auth'])
        if user['is_auth'] is True:
            return True
    return False

def get_info_user(user_id) -> str:
    user = User.find_user(user_id=user_id)
    return user.get('language', 'uk')


