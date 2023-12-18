'''
This modul contain classes which implement the Adress Book model
'''

from collections import UserDict
import re

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

# pylint: disable=too-few-public-methods
class Name(Field):
    '''
    Клас для зберігання імені контакту. Обов'язкове поле.
    '''


# pylint: disable=too-few-public-methods
class Phone(Field):
    '''
    Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
    Необов'язкове поле з телефоном та таких один запис Record
    може містити декілька.
    '''
    def __init__(self, value):
        regexp_10_digits = re.compile(r'^\d{10}$')
        if regexp_10_digits.match(value):
            super().__init__(value)
        else:
            raise ValueError


class Record():
    '''
    Клас для зберігання інформації про контакт, включаючи ім'я
    та список телефонів. Відповідає за логіку додавання/видалення/редагування
    необов'язкових полів та зберігання обов'язкового поля Name
    '''
    def __init__(self, name_value):
        self.name = Name(name_value)
        self.phones = []

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

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
        exist = False

        for phone_obj in self.phones:
            if phone_obj.value == old_number:
                index_of_old_number = self.phones.index(phone_obj)
                self.phones[index_of_old_number] = Phone(new_number)
                exist = True

        if not exist:
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
    def __init__(self):
        super().__init__(self)
        self.data = {}


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
