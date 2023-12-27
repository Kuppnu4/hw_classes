'''
This modul contain classes which implement the Adress Book model
'''

from collections import UserDict
import re
from datetime import datetime

# pylint: disable=too-few-public-methods
class Field:
    '''
    Базовий клас для полів запису. Буде батьківським для всіх полів,
    у ньому реалізується логіка загальна для всіх полів
    '''
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Birthday(Field):
    '''
    Поле для дня народження
    '''
    def __init__(self, value):

        self.regexp_birthday = re.compile(r'^(?:0[1-9]|[12][0-9]|3[01])-(?:0[1-9]|1[0-2])-(?:19\d{2}|20[0-1]\d|202[0-3])$')

        self.__value = value
        if self.regexp_birthday.match(value):
            super().__init__(self.__value)
        else:
            raise ValueError

    @property
    def value(self):
        '''
        value getter
        '''
        return self.__value

    @value.setter
    def value(self, new_value):
        '''
        value setter
        '''
        if self.regexp_birthday.match(new_value):
            self.__value = new_value
        else:
            raise ValueError

# pylint: disable=too-few-public-methods
class Name(Field):
    '''
    Клас для зберігання імені контакту. Обов'язкове поле.
    '''

    def __init__(self, value):
        self.regexp_name = re.compile(r'^[A-Z]{1}[a-zA-Z0-9]{3,15}$')
        self.__value = value
        if self.regexp_name.match(value):
            super().__init__(self.__value)
        else:
            raise ValueError

    @property
    def value(self):
        '''
        value getter
        '''
        return self.__value

    @value.setter
    def value(self, new_value):
        '''
        value setter
        '''
        if self.regexp_name.match(new_value):
            self.__value = new_value
        else:
            raise ValueError


# pylint: disable=too-few-public-methods
class Phone(Field):
    '''
    Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
    Необов'язкове поле з телефоном та таких один запис Record
    може містити декілька.
    '''

    def __init__(self, value):
        self.regexp_10_digits = re.compile(r'^\d{10}$')
        self.__value = value
        if self.regexp_10_digits.match(value):
            super().__init__(value)
        else:
            raise ValueError

    @property
    def value(self):
        '''
        value getter
        '''
        return self.__value

    @value.setter
    def value(self, new_value):
        '''
        value setter
        '''
        if self.regexp_10_digits.match(new_value):
            self.__value = new_value
        else:
            raise ValueError


class Record:
    '''
    Клас для зберігання інформації про контакт, включаючи ім'я
    та список телефонів. Відповідає за логіку додавання/видалення/редагування
    необов'язкових полів та зберігання обов'язкового поля Name
    '''


    def __init__(self, name_value, birthday_value=None):

        self.name = Name(name_value)
        self.phones = []
        if birthday_value:
            self.birthday = Birthday(birthday_value)
        else:
            self.birthday = birthday_value

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


    def days_to_birthday(self):
        '''
        days till next birthday counter
        '''
        result = None
        if self.birthday:
            today = datetime.now()
            this_year = today.year
            days_b4_birthday = 0

            birthday_date_obj = datetime.strptime(self.birthday.value, '%d-%m-%Y')

            this_year_birthday_obj = datetime(
                year = this_year,
                month = birthday_date_obj.month,
                day = birthday_date_obj.day
                )
            next_year_birthday_obj = datetime(
                year = this_year + 1,
                month = birthday_date_obj.month,
                day = birthday_date_obj.day
                )

            if this_year_birthday_obj < today:
                days_b4_birthday = next_year_birthday_obj - today
            else:
                days_b4_birthday = this_year_birthday_obj - today

            result = days_b4_birthday.days

        else:
            print('The birthday was not stated')

        return result


    def add_phone(self, number):
        '''
        Додавання телефонів.
        '''
        self.phones.append(Phone(number))


    def remove_phone(self, number):
        '''
        Видалення телефонів.
        '''
        for phone_obj in self.phones:
            if phone_obj.value == number:
                self.phones.remove(phone_obj)


    def edit_phone(self, old_number, new_number):
        '''
        Редагування телефонів.
        '''

        for phone_obj in self.phones:
            if phone_obj.value == old_number:
                index_of_old_number = self.phones.index(phone_obj)
                self.phones[index_of_old_number] = Phone(new_number)
                break

            else:
                raise ValueError


    def find_phone(self, search_phone):
        '''
        Пошук телефону.
        '''
        find_phone_obj = None
        for phone_obj in self.phones:

            if phone_obj.value == search_phone:
                find_phone_obj = phone_obj

        return find_phone_obj


class AddressBook(UserDict):
    '''
    Клас для зберігання та управління записами. Успадковується від UserDict,
    та містить логіку пошуку за записами до цього класу

    Видалення записів за іменем.
    '''


    def iterator(self):
        '''
        method which iterate address book
        '''
        return Generator(self.data)

    def add_record(self, record_obj):
        '''
        Додавання записів.
        '''
        self.data[record_obj.name.value] = record_obj

    def find(self, search_name):
        '''
        Пошук записів за іменем.
        '''
        for abonent in self.data:
            found_numbers = None
            if abonent == search_name:
                found_numbers = self.data[search_name]

            return found_numbers

    def delete(self, name_str):
        '''
         Видалення записів за іменем.
        '''
        if name_str in self.data:
            del self.data[name_str]


class Generator:
    '''
    class which generate outputs of adress book
    '''

    def __init__(self, data_dict):

        self.N = 3
        self.data_dict = data_dict
        self.contacts_list = []                                 #список контактов из data_dict, этот список мы перебираем в __next__
        for key, value in self.data_dict.items():
            self.contacts_list.append(f'{key} --- {value}')
        self.written_contacts = []                              #список записанных уже взятых контактов для выдачи
        self.result_contacts = []                               #список из 2х контактов для выдачи


    def __iter__(self):
        return self

    def __next__(self):

        if len(self.written_contacts) < len(self.data_dict):
            self.result_contacts = []

            if len(self.contacts_list) > self.N - 1:                        #проверяем колличество оставшихся контактов для обработки
                self.result_contacts = self.contacts_list[0:self.N]         #берем из списка контактов необходимое колличество
                for _ in range(self.N):
                    self.written_contacts.append(self.contacts_list[0])     #добавляем контакт в список уже взятых контактов
                    del self.contacts_list[0]               #удаляем взятый контакт из списка всех контактов оставшихся для обработки

            else:
                self.result_contacts = self.contacts_list[0:self.N]
                for _ in range(len(self.contacts_list)):
                    self.written_contacts.append(self.contacts_list[0])
                    del self.contacts_list[0]

            return self.result_contacts                   #возвращаем результат итерации, в виде списка контактов заданной длины

        else:
            raise StopIteration

    # Створення нової адресної книги
book = AddressBook()

    # Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
book.add_record(john_record)

    # Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

    # Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

john = book.find("John")
print(john, ' <<< before')
john.edit_phone("1234567890", "1112223333")
print(john, ' <<< after')

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
book.delete("Jane")


alex_record = Record('Alex', '20-02-1999')
jeka_record = Record('Jeka', '10-03-1990')
vova_record = Record('Vova', '13-12-2009')
lena_record = Record('Lena', '11-09-1973')
natasha_record = Record('Natasha', '30-09-1963')
sergey_record = Record('Sergey', '05-04-1962')

alex_record.name.value = 'Alexxxx'
print(alex_record.birthday)

book.add_record(alex_record)
book.add_record(jeka_record)
book.add_record(vova_record)
book.add_record(lena_record)
book.add_record(natasha_record)
book.add_record(sergey_record)

for record in book.iterator():
    print(record)
