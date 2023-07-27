# -*- coding: utf-8 -*-
from settings import Settings
import os
import subprocess
import json

"""
Created on Sun August 8th 2021

@author Dan Asafo-Agyei

This file includes the Main class. This class is a child class to the Settings class so the settings are easily 
retrieved. This class is responsible for running the program.

Run this module to run the cipher.
"""

class Main(Settings):

    def __init__(self):

        """Initialises all lists and values that are needed in program,
        defines some folder and file paths"""

        super().__init__()
        self.cipher_multiple = 0
        self.rotation = 1
        self.top_ten_list = []
        self.temp_dict = {}
        self.cwd = os.getcwd()
        self.counter_file = self.cwd + "\\counter.txt"
        self.common_words = self.cwd + "\\common_words.txt"
        self.logs = self.cwd + "\\logs\\"
        self.run()

    def run(self):

        """Main function in the class. Runs other functions in the class."""

        self.get_inputs()
        self.create_folders()
        if self.cipher_mode == "auto-decrypt":
            self.auto_decrypt()
        else:
            self.encrypt_decrypt(self.rotation_value, self.get_multiple())
            if self.cipher_mode == "encrypt":
                self.get_words(self.message)
            else:
                self.get_words(self.new_message)
        self.add_to_dict()
        self.add_to_log()
        self.print_output()

    def create_folders(self):

        """Creates folder when called. Each new folder has a label with n+1 compared to
        previous folder. Creates files for message and writes input message to file."""

        number = int(self.counter())
        os.mkdir(self.logs + f"message_{number}")
        original_message = self.logs + f"message_{number}\\input_message.txt"
        with open(original_message, 'w') as f:
            f.write(self.message)
        new_number = number + 1
        with open(self.counter_file, 'w') as f:
            f.write(str(new_number))

    def encrypt_decrypt(self, rotation, multiple):

        """Converts each letter to numerical value. Letters A-Z correspond to numbers 65-90 using function ord().
        Changes each letter by rotation value, combines letters to generate new message."""

        self.new_message = ''
        for char in self.message:
            char_num = ord(char)
            if char.isalpha():
                char_num += rotation * multiple
                if char_num < 65:
                    new_num = (26 + char_num)
                elif char_num > 90:
                    new_num = (char_num - 26)
                else:
                    new_num = (char_num)
                self.new_message = self.new_message + chr(new_num)
            else:
                self.new_message += char
                pass

    def auto_decrypt(self):

        """Makes use of functions encrypt_decrypt() and check_decryption() to generate multiple messages from
        different rotation values. Asks user if message decryption successful."""

        while self.rotation <= 25:
            self.encrypt_decrypt(self.rotation, 1)
            self.rotation += 1
            if self.check_decryption(self.new_message):
                while True:
                    user_input = input("\nSuccessfully decrypted? Y/N: ").upper()
                    valid_inputs = ('Y', 'N')
                    if self.is_valid_input(user_input, valid_inputs):
                        if user_input == 'Y':
                            self.rotation = 100
                            break
                        else:
                            break
                    else:
                        continue
        if self.rotation == 100:
            pass
        else:
            print("\nNo possible decryption found.")
            self.new_message = "No possible decryption found."

    def check_decryption(self, message):

        """Is called in auto_decrypt(), compares all words in message to words in common_words.txt.
        Returns True if word matches."""

        with open(self.common_words) as f:
            common_words = f.readlines()
        common_words = [word.replace('\n', '') for word in common_words]
        self.get_words(message)
        for word in self.words:
            if word in common_words:
                print(f"\nMessage found: {message.upper()}")
                return True
            else:
                pass

    def get_multiple(self):

        """Is called in encrypt_decrypt, provides value that determines whether message encrypted or decrypted."""

        if self.cipher_mode == "encrypt":
            self.cipher_multiple = 1
        elif self.cipher_mode == "decrypt":
            self.cipher_multiple = -1
        return self.cipher_multiple

    def get_words(self, message):

        """Is called whenever a message needs to split into words. Filters out non letter characters.
        Adds all words to a list, list reset everytime function called so is reusable."""

        self.words = []
        for word in message.split():
            all_chars = list(word)
            for char in all_chars:
                if not char.isalpha():
                    word = word.replace(char, '')
            self.words.append(word.lower())
            if word == '':
                self.words.remove(word)

    def add_to_dict(self):

        """Adds to words_dict.json for every message. Creates dictionary of the frequency of all words entered."""

        with open(self.cwd + "\\words_dict.json") as f:
            dict = json.load(f)
        for word in self.words:
            self.temp_dict[word] = 0
        keys = []
        for k in dict:
            keys.append(k)
        for word in self.words:
            if word in keys:
                dict[word] += 1
            else:
                dict[word] = self.words.count(word)
            self.temp_dict[word] += 1
        with open(self.cwd + "\\words_dict.json", 'w') as f:
            json.dump(dict, f, indent=2)

    def statistics(self):

        """Generates basics statistics about non-encrypted message.
        Total number of words.
        Min/max word length.
        Unique words.
        Returns string containing all these values when called"""

        with open(self.common_words) as f:
            common_words = f.readlines()
        common_words = [word.replace('\n', '') for word in common_words]
        unique_words_list = []
        for word in self.words:
            if word not in common_words:
                unique_words_list.append(word)
        total_words = f"Total number of words: {len(self.words)}"
        min_length = f"Minimum word length: {min([len(word) for word in self.words])}"
        max_length = f"Maximum word length: {max([len(word) for word in self.words])}"
        unique_words = f"Unique words: {unique_words_list}"
        return f"{total_words}\n\n{unique_words}\n\n{min_length}\n\n{max_length}" \
               f"\n\nTen most common words:\n"

    def top_ten(self):

        """Generates another statistic, top ten most common words in inputted message.
        Returns list of ten most common."""

        sort = sorted(self.temp_dict.items(), key=lambda x: x[1], reverse=True)
        for i in range(0, len(sort)):
            word = sort[i][0]
            frequency = sort[i][1]
            if len(self.top_ten_list) < 10:
                self.top_ten_list.append(f"\nWord: {word}\t\t\tFrequency: {frequency}")
            else:
                pass
        return self.top_ten_list

    def counter(self):
        with open(self.counter_file, 'r') as f:
            number = f.readline()
            return number

    def add_to_log(self):

        """Writes too statistics.txt and encrypted/decrypted_message.txt with relevant data. Calls statistics()
        and top_ten() to get strings."""

        number = int(self.counter()) - 1
        new_message = self.logs + f"message_{number}\\{self.cipher_mode}ed_message.txt"
        self.stats = self.logs + f"message_{number}\\statistics.txt"
        with open(new_message, 'w') as f:
            f.write(self.new_message)
        with open(self.stats, 'w') as f:
            f.write(self.statistics())
            for word in self.top_ten():
                f.write(word)

    def print_output(self):

        """Prints output message in console and opens logs folder in file explorer."""

        print("\n-----OUTPUT MESSAGE-----")
        print(f"Message: {self.new_message}")
        subprocess.Popen(f"explorer {self.logs}message_{int(self.counter()) -1}")

if __name__ == "__main__":
    Main()