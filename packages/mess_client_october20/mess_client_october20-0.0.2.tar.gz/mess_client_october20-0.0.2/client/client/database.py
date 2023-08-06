import os
# import sys
import datetime
# перед сборкой проекта добавляем строку ниже
from sqlalchemy.sql import default_comparator
from sqlalchemy import create_engine, Table, Column, Integer, String, Text, MetaData, DateTime
from sqlalchemy.orm import mapper, sessionmaker
# from common.variables import *


# "sys.path..." добавляем для правильной подгрузки библиотек
# sys.path.append('../')


# Класс - база данных.
class ClientDatabase:
    """
    Класс - оболочка для работы с базой данных клиента.
    Использует SQLite базу данных, реализован с помощью
    SQLAlchemy ORM и используется классический подход.
    """

    class KnownUsers:
        """
        Класс - отображение имени пользователя для таблицы всех пользователей.
        """

        def __init__(self, user):
            self.id = None
            self.username = user

    # class MessageHistory: # правильнее переименовать в статистику
    class MessageStat:
        """
        Класс - отображения таблицы статистики переданных сообщений.
        """

        # def __init__(self, from_user, to_user, message):
        def __init__(self, contact, direction, message):
            self.id = None
            # self.from_user = from_user
            self.contact = contact
            # self.to_user = to_user
            self.direction = direction
            self.message = message
            self.date = datetime.datetime.now()

    class Contacts:
        """
        Класс - отображения таблицы контактов
        """

        def __init__(self, contact):
            self.id = None
            self.name = contact

    # Конструктор класса ClientDatabase:
    def __init__(self, name):
        # Создаём движок базы данных, поскольку разрешено несколько
        # клиентов одновременно, каждый должен иметь свою БД
        # Поскольку клиент мультипоточный необходимо отключить
        # проверки на подключения с разных потоков,
        # иначе sqlite3.ProgrammingError
        # Ищем файл БД для каждого клиента используя модуль 'os'
        # path = os.path.dirname(os.path.realpath(__file__))
        # перед размещением в проде убираем обращения
        # к "os.path.realpath(__file__)" заменяя на "os.getcwd()"
        path = os.path.dirname(os.getcwd())
        filename = f'client_{name}.db3'
        # self.database_engine = create_engine(f'sqlite:///client_{name}.db3', echo=False, pool_recycle=7200,
        self.database_engine = create_engine(
            f'sqlite:///{os.path.join(path, filename)}',
            echo=False, pool_recycle=7200,
            connect_args={'check_same_thread': False})

        # Создаём объект MetaData
        self.metadata = MetaData()

        # Создаём таблицу известных пользователей
        users = Table('known_users', self.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('username', String)
                      )

        # Создаём таблицу истории сообщений
        history = Table('message_history', self.metadata,
                        Column('id', Integer, primary_key=True),
                        # Column('from_user', String),
                        Column('contact', String),
                        # Column('to_user', String),
                        Column('direction', String),
                        Column('message', Text),
                        Column('date', DateTime)
                        )

        # Создаём таблицу контактов
        contacts = Table('contacts', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('name', String, unique=True)
                         )

        # Создаём таблицы
        self.metadata.create_all(self.database_engine)

        # Создаём отображения
        mapper(self.KnownUsers, users)
        # mapper(self.MessageHistory, history)
        mapper(self.MessageStat, history)
        mapper(self.Contacts, contacts)

        # Создаём сессию
        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

        # Необходимо очистить таблицу контактов, т.к. при запуске они
        # подгружаются с сервера.
        self.session.query(self.Contacts).delete()
        self.session.commit()

    def add_contact(self, contact):
        """
        Метод добавления контакта в базу данных.
        """
        if not self.session.query(
                self.Contacts).filter_by(name=contact).count():
            contact_row = self.Contacts(contact)
            self.session.add(contact_row)
            self.session.commit()

    def contacts_clear(self):
        """
        Метод очищающий таблицу со списком контактов.
        """
        self.session.query(self.Contacts).delete()

    def del_contact(self, contact):
        """
        Метод удаления выбранного контакта
        """
        self.session.query(self.Contacts).filter_by(name=contact).delete()

    # Функция добавления известных пользователей.
    # Пользователи получаются только с сервера, поэтому таблица очищается.
    def add_users(self, users_list):
        """
        Метод заполняющий таблицу известных пользователей.
        :param users_list:
        :return:
        """
        self.session.query(self.KnownUsers).delete()
        for user in users_list:
            user_row = self.KnownUsers(user)
            self.session.add(user_row)
        self.session.commit()

    # Функция сохраняющяя сообщения
    # def save_message(self, from_user, to_user, message):
    def save_message(self, contact, direction, message):
        """
        Метод сохраняющий сообщение в базе данных.
        :param contact:
        :param direction:
        :param message:
        :return:
        """
        # message_row = self.MessageHistory(from_user, to_user, message)
        # message_row = self.MessageHistory(contact, direction, message)
        message_row = self.MessageStat(contact, direction, message)
        self.session.add(message_row)
        self.session.commit()

    # Функция возвращающяя контакты
    def get_contacts(self):
        """
        Метод возвращающий список всех контактов.
        :return:
        """
        return [contact[0] for contact in self.session.query(self.Contacts.name).all()]

    # Функция возвращающяя список известных пользователей
    def get_users(self):
        """
        Метод возвращающий список всех известных пользователей.
        :return:
        """
        return [user[0] for user in self.session.query(self.KnownUsers.username).all()]

    # Функция проверяющяя наличие пользователя в известных
    def check_user(self, user):
        """
        Метод проверяющий существует ли пользователь.
        :param user:
        :return:
        """
        if self.session.query(
                self.KnownUsers).filter_by(username=user).count():
            return True
        else:
            return False

    # Функция проверяющяя наличие пользователя контактах
    def check_contact(self, contact):
        """
        Метод проверяющий существует ли контакт.s
        :param contact:
        :return:
        """
        if self.session.query(self.Contacts).filter_by(name=contact).count():
            return True
        else:
            return False

    # Функция возвращающая историю переписки
    # def get_history(self, from_who=None, to_who=None):
    #     query = self.session.query(self.MessageHistory)
    #     if from_who:
    #         query = query.filter_by(from_user=from_who)
    #     if to_who:
    #         query = query.filter_by(to_user=to_who)
    #     return [(history_row.from_user, history_row.to_user, history_row.message, history_row.date)
    #             for history_row in query.all()]
    def get_history(self, contact):
        """
        Функция возвращающая историю переписки определённого пользователя
        """
        query = self.session.query(self.MessageStat).filter_by(contact=contact)
        # используем тернарный оператор для возврата списка историй
        return [(history_row.contact, history_row.direction, history_row.message, history_row.date)
                for history_row in query.all()]


# отладка
if __name__ == '__main__':
    test_db = ClientDatabase('test1')
    # for i in ['test3', 'test4', 'test5']:
    #     test_db.add_contact(i)
    # test_db.add_contact('test4')
    # test_db.add_users(['test1', 'test2', 'test3', 'test4', 'test5'])
    # test_db.save_message('test1', 'in', f'Привет! я тестовое сообщение от {datetime.datetime.now()}!')
    # test_db.save_message('test2', 'out', f'Привет! я другое тестовое сообщение от {datetime.datetime.now()}!')
    # print(test_db.get_contacts())
    # print(test_db.get_users())
    # print(test_db.check_user('test1'))
    # print(test_db.check_user('test10'))
    print(sorted(test_db.get_history('test2'), key=lambda item: item[3]))
    # print(test_db.get_history(to_who='test2'))
    # print(test_db.get_history('test3'))
    # test_db.del_contact('test4')
    # print(test_db.get_contacts())
