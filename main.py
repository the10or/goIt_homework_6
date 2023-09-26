from classes import *
from itertools import islice

INVITE_MESSAGE = "Please enter your command here >>> "
NO_RECORD_ERROR_MESSAGE = "Sorry, there's no such record, enter another name or check your spelling"
QUIT_COMMANDS = ("good bye", "close", "exit")
WRONG_NUMBER_OF_PARAMETERS_ERROR_MESSAGE = "Wrong number of parameters, please check your input"
EMPTY_MESSAGE = "No records in this address book"
HELLO_MESSAGE = "How can I help you?"
INVALID_COMMAND_ERROR_MESSAGE = "Invalid command, please check your input"
BYE_MESSAGE = "Good bye!"


def input_error(func):
    """
    Decorator function that catches specific exceptions raised by the decorated function,
    and returns the appropriate error message or value.

    Parameters:
        func (function): The decorated function.

    Returns:
        function: The wrapper function that handles the exceptions and returns the result.
    """

    def wrapper(*args):
        try:
            return func(*args)
        except KeyError as e:
            return e
        except IndexError:

            return None, WRONG_NUMBER_OF_PARAMETERS_ERROR_MESSAGE
        except TypeError as e:
            return None, e
        except ValueError as e:
            return e

    return wrapper


def hello(*args):
    return HELLO_MESSAGE


@input_error
def add_contact(name, phone):
    """
    Adds a new contact to the address book with the given name and phone number.

    Args:
        name (str): The name of the contact.
        phone (str): The phone number of the contact.

    Raises:
        KeyError: If a contact with the same name already exists in the address book.

    Returns:
        str: A message indicating that the contact has been successfully added.
    """
    if address_book.find(name):
        raise KeyError(f"{name} already is in contacts. If you want to make changes to the record,"
                       f" use 'change [name] [phone]' command instead")

    contact_record = Record(name)
    contact_record.add_phone(phone)
    address_book.add_record(contact_record)

    return f"{name}'s phone has been added to contacts"


@input_error
def change_contact(name, phone_old, phone_new):
    """
    A function that changes the phone number of a contact in the address book.

    Parameters:
        name (str): The name of the contact.
        phone_old (str): The old phone number of the contact.
        phone_new (str): The new phone number to be replaced.

    Returns:
        str: A message indicating the success of the operation.

    Raises:
        KeyError: If the contact with the given name does not exist in the address book.
    """
    if address_book.find(name):
        contact_record = address_book[name]
        contact_record.edit_phone(phone_old, phone_new)
        address_book[name] = contact_record
        return f"{name}'s phone has been changed in contacts"
    else:
        raise KeyError(NO_RECORD_ERROR_MESSAGE)


@input_error
def add_phone(name, phone):
    """
    Adds a phone number to a contact in the address book.

    Parameters:
        name (str): The name of the contact.
        phone (str): The phone number to add to the contact.

    Returns:
        str: A message indicating that the phone number has been added to the contact.

    Raises:
        KeyError: If the contact does not exist in the address book.
        ValueError: If the phone number is invalid.
    """
    record = address_book.find(name)
    if not record:
        raise KeyError(NO_RECORD_ERROR_MESSAGE)
    else:
        try:
            record.add_phone(phone)
        except ValueError as e:
            return e

    return f"{name}'s phone has been added to contacts"


@input_error
def get_phone(name):
    """
    Adds a phone number to a contact in the address book.

    Parameters:
        name (str): The name of the contact.
        phone (str): The phone number to add to the contact.

    Returns:
        str: A message indicating that the phone number has been added to the contact.

    Raises:
        KeyError: If the contact does not exist in the address book.
        ValueError: If the phone number is invalid.
    """
    record = address_book.find(name)
    if not record:
        return TypeError(NO_RECORD_ERROR_MESSAGE)
    return f"{name}'s phone(s): {'; '.join(phone.value for phone in record.phones)}"


def add_birthday(name, birthday):
    """
    Adds a phone number to a contact in the address book.

    Parameters:
        name (str): The name of the contact.
        phone (str): The phone number to add to the contact.

    Returns:
        str: A message indicating that the phone number has been added to the contact.

    Raises:
        KeyError: If the contact does not exist in the address book.
        ValueError: If the phone number is invalid.
    """
    record = address_book.find(name)
    if not record:
        raise KeyError(NO_RECORD_ERROR_MESSAGE)
    else:
        try:
            record.birthday.value = birthday
        except ValueError as e:
            return e

    return f"{name}'s birthday has been added to contacts"


def show_all_contacts(num=None):
    """
    Returns a string representation of all contacts in the address book.

    Parameters:
        num (int, optional): The number of contacts to display. If not provided, all contacts will be displayed.

    Returns:
        str: A string representation of the contacts. If there are no contacts, returns an empty message.
    """
    global address_book
    view = ""
    contacts = islice(address_book, num) if num else address_book
    for record in contacts:
        view += str(record) + "\n"
    return EMPTY_MESSAGE if not view else view


@input_error
def parse_command(user_input):
    """
    Parses the user input and returns the corresponding function and arguments.

    Parameters:
        user_input (str): The input provided by the user.

    Returns:
        tuple: A tuple containing the function to be executed and its arguments.

    Raises:
        TypeError: If the user input does not match any known command.
    """
    if user_input.startswith('hello'):
        return hello, []
    if user_input.startswith("show all"):
        num = int(user_input.split()[2]) \
            if len(user_input.split()) == 3 else []

        return show_all_contacts, num
    if user_input.startswith('phone'):
        name = user_input.split()[1].capitalize()
        return get_phone, name

    if user_input.startswith("add"):
        if 'phone' in user_input:
            user_input = user_input.replace('add phone', 'add')
            name, phone = parse_complex_data(user_input)
            return add_phone, name, phone

        elif 'birthday' in user_input:
            user_input = user_input.replace('add birthday', 'add')
            name, birthday = parse_birthday(user_input)
            return add_birthday, name, birthday

        name, phone = parse_complex_data(user_input)
        return add_contact, name, phone

    if user_input.startswith("change"):
        user_data = user_input.split()
        name, phone_old, phone_new = user_data[1].capitalize(), user_data[2], user_data[3]
        print(name, phone_old, phone_new)
        return change_contact, name, phone_old, phone_new
    else:

        raise TypeError(INVALID_COMMAND_ERROR_MESSAGE)


def parse_complex_data(user_input):
    """
        Parses complex data provided by the user.

        Args:
            user_input (str): The input string provided by the user.

        Returns:
            tuple: A tuple containing the parsed name and phone number.
    """
    data = user_input.split()
    name, phone = data[1].capitalize(), data[2]
    return name, phone


def parse_birthday(user_input):
    """
        Parse the user input to extract the name and birthday.

        Args:
            user_input (str): The user input containing the name and birthday.

        Returns:
            tuple: A tuple containing the parsed name (str) and birthday (tuple of ints).
    """
    data = user_input.split()
    name, birthday = data[1].capitalize(), data[2:]

    return name, (tuple(map(int, birthday)))


def main():
    while True:
        user_input = input(INVITE_MESSAGE)
        if user_input in QUIT_COMMANDS:
            print(BYE_MESSAGE)
            break
        run, *args = parse_command(user_input.lower())
        if run:
            print(run(*args))
        else:
            print(args[0])


if __name__ == '__main__':
    address_book = AddressBook()
    record = Record("Jim", (2000, 9, 27))
    record2 = Record("Bob", (2000, 5, 27))
    record.add_phone("3456343651")
    # record.add_phone("3456343659")
    address_book.add_record(record)
    address_book.add_record(record2)

    main()
