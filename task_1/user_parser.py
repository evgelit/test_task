from telethon.sync import TelegramClient
from telethon.tl.custom.dialog import Dialog
from env import env
from pandas import DataFrame
from re import compile
from pathlib import Path
import json


class UserParser:

    VOWEL_SET = {"а", "я", "y", "a", "e"}
    FEMALE_USERS_FILE = "female.txt"
    MALE_USERS_FILE = "male.txt"
    JSON_USERS_FILE = "users.json"

    def __init__(self, session_name: str):
        self.client = TelegramClient(
            session_name,
            int(env['api_id']),
            env['api_hash']
        )
        self.client.start()

    def parse_users(self, dialog_name: str, incl_bots=False):
        dialog = self.__get_dialog(dialog_name)
        if dialog is None:
            raise Exception(f"Dialog with name\"{dialog_name}\" not found")
        users = self.__get_users(dialog, incl_bots)
        users['gender'] = [self.__get_gender(x) for x in users['name']]
        self.__write_result(users)

    def __get_users(self, dialog: Dialog, incl_bots=False) -> DataFrame:
        users = DataFrame(columns=["username", "name", "last_name"])
        for user in self.client.get_participants(dialog):
            if user.bot is True and incl_bots is False:
                continue
            users.loc[len(users.index)] = [
                user.username,
                user.first_name,
                user.last_name
            ]
        return users

    def __get_dialog(self, dialog_name) -> Dialog or None:
        for dialog in self.client.iter_dialogs():
            if dialog.title == dialog_name:
                return dialog
        return None

    def __get_gender(self, name):
        regex = compile('[^a-zA-Zа-яА-Я]')
        name = regex.sub('', name)
        return 'f' if name.strip()[-1] in self.VOWEL_SET else 'm'

    def __get_path(self, file_name: str) -> str:
        path = Path(__file__).with_name('data')
        return f"{path.absolute()}/{file_name}"

    def __write_result(self, users: DataFrame) -> None:
        with open(self.__get_path(self.MALE_USERS_FILE), 'w') as male_file:
            male_data = users[users.gender == "m"].username.to_string(
                header=False,
                index=False
            )
            male_file.write(male_data)
        with open(self.__get_path(self.FEMALE_USERS_FILE), 'w') as female_file:
            female_data = users[users.gender == "f"].username.to_string(
                header=False,
                index=False
            )
            female_file.write(female_data)
        users.drop('gender', axis='columns', inplace=True)
        with open(self.__get_path(self.JSON_USERS_FILE), "w") as json_file:
            json.dump(
                dict(
                    zip(
                        users.username,
                        users.set_index('username').to_dict('records')
                    )
                ),
                json_file,
                indent=4,
                ensure_ascii=False
            )
