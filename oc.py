import base64
import json
import os


def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read())
    return encoded_string.decode('utf-8')


def write_to_file(contacts):
    with open("contacts.json", "w") as file:
        for contact in contacts:
            json.dump(contact, file)
            file.write("\n")


def add_contact():
    first_name = input("Введите имя: ")
    last_name = input("Введите фамилию: ")
    father_name = input("Введите отчество: ")
    phone_number = input("Введите номер телефона: ")
    mail = input("Введите адрес электронной почты: ")
    password = input("Введите пароль: ")
    foto_path = input("Введите путь к фотографии: ")

    # Convert image to base64
    if os.path.exists(foto_path):
        encoded_image = encode_image(foto_path)
    else:
        encoded_image = None

    contact = {
        "first_name": first_name,
        "last_name": last_name,
        "father_name": father_name,
        "phone_number": phone_number,
        "password": password,
        "foto": encoded_image
    }

    if os.path.exists("contacts.json"):
        with open("contacts.json", "r") as file:
            contacts = [json.loads(line.strip()) for line in file]
        # Check if the email already exists
        existing_emails = [list(contact.keys())[0] for contact in contacts]
        if mail in existing_emails:
            print("Контакт с такой электронной почтой уже существует.")
            return
    else:
        contacts = []

    contacts.append({mail: contact})

    write_to_file(contacts)
    print("Контакт успешно добавлен.")


def find_contact():
    mail = input("Введите адрес электронной почты контакта: ")
    if os.path.exists("contacts.json"):
        with open("contacts.json", "r") as file:
            contacts = [json.loads(line.strip()) for line in file]
        for contact in contacts:
            if mail in contact:
                print("Контакт найден:")
                print(json.dumps(contact, indent=4, ensure_ascii=False))
                return
        print("Контакт с такой электронной почтой не найден.")
    else:
        print("Файл контактов не найден.")


def edit_contact():
    mail = input("Введите адрес электронной почты контакта для изменения: ")
    if os.path.exists("contacts.json"):
        with open("contacts.json", "r") as file:
            contacts = [json.loads(line.strip()) for line in file]
        for i, contact in enumerate(contacts):
            if mail in contact:
                print("Контакт найден:")
                print(json.dumps(contact, indent=4, ensure_ascii=False))
                field_to_edit = input("Введите поле, которое хотите изменить: ")
                new_value = input(f"Введите новое значение для поля '{field_to_edit}': ")
                contacts[i][mail][field_to_edit] = new_value
                # Write updated contacts to file
                write_to_file(contacts)
                print("Контакт успешно изменен.")
                return
        print("Контакт с такой электронной почтой не найден.")
    else:
        print("Файл контактов не найден.")


def main():
    while True:
        print("\n1. Добавить контакт")
        print("2. Найти контакт по почте")
        print("3. Изменить контакт")
        print("4. Выйти")
        choice = input("Выберите действие: ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            find_contact()
        elif choice == "3":
            edit_contact()
        elif choice == "4":
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")


if __name__ == "__main__":
    main()
