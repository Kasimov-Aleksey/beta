import base64
import json
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read())
    return encoded_string.decode('utf-8')

def write_to_file(contacts):
    with open("contacts.json", "w") as file:
        for contact in contacts:
            json.dump(contact, file)
            file.write("\n")

def load_contacts():
    if not os.path.exists("contacts.json"):
        return []
    with open("contacts.json", "r") as file:
        return [json.loads(line.strip()) for line in file]

@app.route('/add_contact', methods=['POST'])
def add_contact():
    data = request.json
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    father_name = data.get("father_name")
    phone_number = data.get("phone_number")
    mail = data.get("mail")
    password = data.get("password")
    foto_path = data.get("foto_path")

    if not all([first_name, last_name, mail, password]):
        return jsonify({"error": "Недостаточно данных"}), 400

    encoded_image = encode_image(foto_path) if os.path.exists(foto_path) else None

    contact = {
        "first_name": first_name,
        "last_name": last_name,
        "father_name": father_name,
        "phone_number": phone_number,
        "password": password,
        "foto": encoded_image
    }

    contacts = load_contacts()

    if any(mail in contact for contact in contacts):
        return jsonify({"error": "Контакт с такой электронной почтой уже существует."}), 400

    contacts.append({mail: contact})
    write_to_file(contacts)

    return jsonify({"message": "Контакт успешно добавлен."}), 201

@app.route('/find_contact', methods=['GET'])
def find_contact():
    mail = request.args.get("mail")
    contacts = load_contacts()

    for contact in contacts:
        if mail in contact:
            return jsonify(contact), 200

    return jsonify({"error": "Контакт с такой электронной почтой не найден."}), 404

@app.route('/edit_contact', methods=['PUT'])
def edit_contact():
    data = request.json
    mail = data.get("mail")
    field_to_edit = data.get("field")
    new_value = data.get("new_value")

    if not all([mail, field_to_edit, new_value]):
        return jsonify({"error": "Недостаточно данных"}), 400

    contacts = load_contacts()

    for i, contact in enumerate(contacts):
        if mail in contact:
            contact[mail][field_to_edit] = new_value
            write_to_file(contacts)
            return jsonify({"message": "Контакт успешно изменен."}), 200

    return jsonify({"error": "Контакт с такой электронной почтой не найден."}), 404

def create_vcard(contact):
    vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{contact['first_name']} {contact['last_name']}
N:{contact['last_name']};{contact['first_name']};{contact['father_name']}
TEL;TYPE=CELL:{contact['phone_number']}
EMAIL:{contact['mail']}
END:VCARD"""
    return vcard

@app.route('/get_vcard', methods=['GET'])
def get_vcard():
    mail = request.args.get("mail")
    contacts = load_contacts()

    for contact in contacts:
        if mail in contact:
            vcard = create_vcard(contact[mail])
            return vcard, 200, {'Content-Type': 'text/vcard'}

    return jsonify({"error": "Контакт с такой электронной почтой не найден."}), 404

if __name__ == "__main__":
    app.run(debug=True)
