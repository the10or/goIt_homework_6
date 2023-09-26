
from collections import UserDict
from datetime import date


class Field:
    def __init__(self, value):
        self.__value = None

    def __str__(self):
        return str(self.__value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val: str):
        if val.isalpha():
            self.__value = val
        else:
            raise ValueError("Name should contain letters only ")

    def __str__(self):
        return str(self.__value)


class Phone(Field):
    def __init__(self, value: str):
        super().__init__(value)
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val):

        if val.isdigit() and len(val) == 10:
            self.__value = val
        else:
            raise ValueError("Number should be 10 digits long")

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()


class Birthday(Field):
    def __init__(self, value: tuple):
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val: tuple):
        if val:
            if len(val) == 3 and all(isinstance(item, int) for item in val):
                self.__value = date(*val)
            else:
                raise ValueError("Birthday should be a tuple of three integers (year, month, day)")


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        for number in self.phones:
            if number.value == phone:
                raise ValueError("Phone is already in this record, try to edit it")
        self.phones.append(Phone(phone))

    def find_phone(self, phone):
        number_found = False
        for number in self.phones:
            if number.value == phone:
                number_found = True
                return number
        if not number_found:
            raise ValueError("No such phone in this record")

    def remove_phone(self, phone):
        phone_found = self.find_phone(phone)
        self.phones.remove(phone_found)

    def edit_phone(self, phone_old, phone_new):
        phone = self.find_phone(phone_old)
        phone.value = phone_new

    def days_to_birthday(self):

        birthday = self.birthday.value
        if birthday:
            today = date.today()
            b_month = birthday.month
            b_day = birthday.day
            this_year = today.year
            birthday_this_year = date(this_year, b_month, b_day)
            birthday_next_year = date(this_year + 1, b_month, b_day)

            if birthday_this_year >= today:
                diff = (birthday_this_year - today).days
            else:
                diff = (birthday_next_year - today).days

            return diff
        else:
            return "birthday is unknown"

    def __repr__(self):
        phone_strings = [str(phone) for phone in self.phones]
        view = f"Contact name: {self.name.value}, phones: {'; '.join(phone_strings) if phone_strings else 'unknown'}"
        days_to_birthday = self.days_to_birthday()
        if type(days_to_birthday) == int and days_to_birthday <= 7:
            blue = "\033[94m"
            reset = "\033[0m"
            view += (f"\n{blue} {self.name.value}'s birthday is in {days_to_birthday} "
                     f"days!!! Call him or her now!{reset}")
        return view


class AddressBook(UserDict):

    def __init__(self):
        super().__init__()
        self._current_index = 0

    def add_record(self, record):
        self[record.name.value] = record

    def find(self, name):
        return self[name] if name in self.keys() else None

    def delete(self, name):
        if name in self.keys():
            self.pop(name)

    def __iter__(self):
        return self.data.values().__iter__()


