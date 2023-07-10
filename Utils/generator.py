import tls_client
from Utils.temps_mail import *
import json
import datetime
from termcolor import colored


class Generate():
    def __init__(self):
        self.email = generateRandomUsername()
        self.session = tls_client.Session(
            client_identifier="chrome_112", random_tls_extension_order=True)

        self.password = self.generate_password()
        self.encryptedValidFrom = ""
        self.nameFieldName = ""
        self.code = ""

        self.generate_password()
        self.generate_token()
        self.send_email()

    def generate_password(self):
        letters = string.ascii_letters
        digits = string.digits

        password = ""
        password += random.choice(letters.upper())  # Une lettre majuscule
        password += ''.join(random.choice(letters.lower())
                            for _ in range(5))  # 5 lettres minuscules
        password += ''.join(random.choice(digits)
                            for _ in range(4))  # 4 chiffres
        password += "$"

        return password

    def generateRandomBirthday(self):
        current_datetime = datetime.datetime.now()
        min_birth_year = current_datetime.year - 18
        max_birth_year = current_datetime.year - 1

        birth_year = random.randint(min_birth_year, max_birth_year)
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)
        birth_hour = current_datetime.hour
        birth_minute = current_datetime.minute
        birth_second = current_datetime.second
        birth_microsecond = current_datetime.microsecond

        birthdate = datetime.datetime(
            birth_year, birth_month, birth_day, birth_hour, birth_minute, birth_second, birth_microsecond
        ).isoformat()

        return birthdate

    def generate_token(self):
        try:
            print(f"{colored('(?)', 'blue')} Generating kick token..")
            headers = {
                'Host': 'kick.com',
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'User-Agent': 'Kick/71 CFNetwork/1404.0.5 Darwin/22.3.0',
                'Accept-Language': 'en_US',
            }

            response = self.session.get(
                'https://kick.com/kick-token-provider/', headers=headers).json()

            self.encryptedValidFrom = response["encryptedValidFrom"]
            self.nameFieldName = response["nameFieldName"]

        except:
            return

    def send_email(self):
        try:
            print(f"{colored('(?)', 'blue')} Sending email..")

            headers = {
                'Host': 'kick.com',
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Accept-Language': 'fr_FR',
                'User-Agent': 'Kick/71 CFNetwork/1404.0.5 Darwin/22.3.0',
            }

            json_data = {
                'email': self.email[0] + '@' + self.email[1],
            }

            response = self.session.post(
                'https://kick.com/api/v1/signup/send/email', headers=headers, json=json_data)

            if response.status_code == 204:
                self.code = getEmail(self.email[0], self.email[1])
                self.send_code()
        except:
            return

    def send_code(self):
        try:
            print(f"{colored('(?)', 'blue')} Activating code..")

            headers = {
                'Host': 'kick.com',
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Accept-Language': 'fr_FR',
                'User-Agent': 'Kick/71 CFNetwork/1404.0.5 Darwin/22.3.0',
            }

            json_data = {
                'code': self.code,
                'email': self.email[0] + '@' + self.email[1],
            }

            response = self.session.post(
                'https://kick.com/api/v1/signup/verify/code', headers=headers, json=json_data)

            if response.status_code == 204:
                self.register()
                pass
        except:
            return

    def register(self):
        try:
            print(f"{colored('(?)', 'blue')} Registering account..")
            headers = {
                'Host': 'kick.com',
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Accept-Language': 'fr_FR',
                'User-Agent': 'Kick/71 CFNetwork/1404.0.5 Darwin/22.3.0',
            }

            payload = json.dumps({
                "agreed_to_terms": True,
                "isMobileRequest": True,
                "birthdate": "2005-06-28T20:26:19.385Z",
                'email': self.email[0] + '@' + self.email[1],
                "cf_captcha_token": "",
                "password": self.password,
                "password_confirmation": self.password,
                "username": self.email[0],
                self.nameFieldName: "",
                "_kick_token_valid_from": self.encryptedValidFrom
            })
            response = self.session.post(
                'https://kick.com/register/', headers=headers, data=payload)

            if response.status_code == 200:
                print(
                    f"{colored('(/)', 'green')} Generated account with username: {self.email[0]}")
                self.token = response.json()["token"]
                self.add_account_to_file()
                self.unlockAccount()
                return

            print(response.text)
            print(response.status_code)

        except Exception as e:
            print(e)
            pass

    def add_account_to_file(self):
        try:
            with open("accounts.txt", "a") as file:
                file.write(
                    f"\n{self.email[0]}@{self.email[1]}:{self.password}:{self.token}")
        except Exception as e:
            print(
                f"{colored('(x)', 'red')} Failed to add the account to accounts.txt. Error: {str(e)}")

    def unlockAccount(self):
        try:
            headers = {
                'Host': 'kick.com',
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Accept-Language': 'fr_FR',
                'Authorization': f'Bearer {self.token}',
                'User-Agent': 'Kick/71 CFNetwork/1404.0.5 Darwin/22.3.0',
            }

            response = self.session.get(
                'https://kick.com/emotes/jupebo', headers=headers)

        except Exception as e:
            print(e)
            pass
