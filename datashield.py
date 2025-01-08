import os
import base64
from cryptography.fernet import Fernet
import getpass

class DataShield:
    def __init__(self):
        self.key = None
        self.fernet = None
        self.load_key()

    def load_key(self):
        if os.path.exists("secret.key"):
            with open("secret.key", "rb") as key_file:
                self.key = key_file.read()
        else:
            self.key = Fernet.generate_key()
            with open("secret.key", "wb") as key_file:
                key_file.write(self.key)
        self.fernet = Fernet(self.key)

    def encrypt_file(self, file_path):
        with open(file_path, "rb") as file:
            file_data = file.read()
        encrypted_data = self.fernet.encrypt(file_data)
        with open(file_path, "wb") as file:
            file.write(encrypted_data)
        print(f"File '{file_path}' encrypted successfully.")

    def decrypt_file(self, file_path):
        with open(file_path, "rb") as file:
            encrypted_data = file.read()
        decrypted_data = self.fernet.decrypt(encrypted_data)
        with open(file_path, "wb") as file:
            file.write(decrypted_data)
        print(f"File '{file_path}' decrypted successfully.")

    def encrypt_message(self, message):
        encoded_message = message.encode()
        encrypted_message = self.fernet.encrypt(encoded_message)
        return base64.urlsafe_b64encode(encrypted_message).decode()

    def decrypt_message(self, encrypted_message):
        decoded_encrypted_message = base64.urlsafe_b64decode(encrypted_message)
        decrypted_message = self.fernet.decrypt(decoded_encrypted_message)
        return decrypted_message.decode()

def main():
    print("Welcome to DataShield!")
    ds = DataShield()

    while True:
        print("\nOptions:")
        print("1. Encrypt a file")
        print("2. Decrypt a file")
        print("3. Encrypt a message")
        print("4. Decrypt a message")
        print("5. Exit")

        choice = input("Please select an option (1-5): ")

        if choice == '1':
            file_path = input("Enter the path of the file to encrypt: ")
            ds.encrypt_file(file_path)
        elif choice == '2':
            file_path = input("Enter the path of the file to decrypt: ")
            ds.decrypt_file(file_path)
        elif choice == '3':
            message = input("Enter the message to encrypt: ")
            encrypted_message = ds.encrypt_message(message)
            print(f"Encrypted message: {encrypted_message}")
        elif choice == '4':
            encrypted_message = input("Enter the message to decrypt: ")
            try:
                decrypted_message = ds.decrypt_message(encrypted_message)
                print(f"Decrypted message: {decrypted_message}")
            except Exception as e:
                print("Failed to decrypt message. Please ensure it is correct.")
        elif choice == '5':
            print("Exiting DataShield. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()