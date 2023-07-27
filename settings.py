# -*- coding: utf-8 -*-
from random import randint

"""
This file includes the Settings class, parent class to Main class in main.py. 
Gets all user inputs and stores them.
Uses function is_valid_input to reject non valid user input until valid input entered.
"""

class Settings:

    def __init__(self):
        self.cipher_mode = ""
        self.entry_mode = ""
        self.rotation_value = 0
        self.rotation_range = range(-25,26)
        self.filename = ""
        self.message = ""

    def get_inputs(self):
        while True:
            self.get_cipher_mode()
            self.get_entry_mode()
            self.filename = ""
            self.get_message()
            if self.cipher_mode != "auto-decrypt":
                self.get_rotation_value()
            else:
                self.rotation_value = "auto"
            self.selections()
            if self.confirm_selections():
                break
            else:
                continue

    def is_valid_input(self, user_input, valid_inputs):
        if user_input in valid_inputs:
            return True
        else:
            print("-----INVALID INPUT-----")
            return False

    def get_cipher_mode(self):
        while True:
            print("\n-----CIPHER MODE-----")
            user_input = input("Encrypt, Decrypt or Auto-Decrypt? E/D/A: ").upper()
            valid_inputs = ("E", "D", "A")
            if self.is_valid_input(user_input, valid_inputs):
                if user_input == "E":
                    self.cipher_mode = "encrypt"
                elif user_input == "D":
                    self.cipher_mode = "decrypt"
                elif user_input == "A":
                    self.cipher_mode = "auto-decrypt"
                break
            else:
                continue

    def get_entry_mode(self):
        while True:
            print("\n-----MESSAGE ENTRY MODE-----")
            user_input = input("Read message from file or input manually? F/M: ").upper()
            valid_inputs = ("F", "M")
            if self.is_valid_input(user_input, valid_inputs):
                if user_input == "F":
                    self.entry_mode = "read from file"
                elif user_input == "M":
                    self.entry_mode = "manual entry"
                break
            else:
                continue

    def get_rotation_value(self):
        while True:
            print("\n-----ROTATION VALUE-----")
            user_input = input("Enter rotation value or select random value? -25 - 25/R: ").upper()
            valid_inputs = ["R", "r"]
            for i in self.rotation_range:
                valid_inputs.append(str(i))
            if self.is_valid_input(user_input, valid_inputs):
                if user_input == "R":
                    self.rotation_value = randint(-25,26)
                else:
                    self.rotation_value = int(user_input)
                break
            else:
                continue

    def get_message(self):
        while True:
            if self.entry_mode == "manual entry":
                self.message = input("Enter message: ").upper()
                break
            else:
                self.filename = input("\nEnter file directory: ")
                try:
                    file = open(self.filename, 'r')
                except (FileNotFoundError, PermissionError, OSError):
                    print("-----FILE NOT FOUND-----")
                else:
                    with file:
                        self.message = file.read().upper()
                    break

    def selections(self):
        print(f"\nCipher mode: {self.cipher_mode}")
        print(f"Entry mode: {self.entry_mode}")
        print(f"Rotation value: {self.rotation_value}")
        print(f"Filename: {self.filename}")
        print(f"Message: {self.message}")

    def confirm_selections(self):
        while True:
            print("\n-----CONFIRM SELECTIONS-----")
            user_input = input("Keep these selections? Y/N: ").upper()
            valid_inputs = ("Y", "N")
            if self.is_valid_input(user_input, valid_inputs):
                if user_input == "Y":
                    return True
                else:
                    return False
            else:
                continue