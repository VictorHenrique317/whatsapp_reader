import re
import tkinter
from tkinter.filedialog import askopenfilename


class WhatsappReader:
    def __init__(self):
        self._file_path = None
        self._name_exp = r"\d+?/\d+?/\d+, \d+?:\d+? .+? - (.+?): (.+)"
        self._date_exp = r"(\d+)/(\d+)/(\d+)"

        self._names = set()

    def read(self):
        self._names = set()

        try:
            temp_path = self._pick_file()
            if temp_path == "":
                return False
            else:
                self._file_path = temp_path
            with open(self._file_path, "r", encoding="utf-8") as file:
                while True:
                    current_line = file.readline()
                    if not current_line:
                        break
                    results = re.findall(self._name_exp, current_line)
                    if results is not None and len(results) != 0:
                        self._names.add(results[0][0])
            self._names = tuple(self._names)
            return True
            # self._test()
        except FileNotFoundError:
            return False

    @staticmethod
    def _pick_file():
        tkinter.Tk().withdraw()
        return askopenfilename()

    def message_count(self, users=None):
        if users is None:
            count = {"total": 0}
        else:
            count = {x: 0 for x in users if users}
        with open(self._file_path, "r", encoding="utf-8") as count_file:
            while True:
                line = count_file.readline()
                if not line:
                    break
                current_user = re.findall(self._name_exp, line)[0][0] \
                    if len(re.findall(self._name_exp, line)) != 0 else None
                # prevents nameless user
                if users is None:
                    count["total"] += 1
                    continue
                for user in users:
                    if current_user == user:  ## +1 message for user
                        count[user] += 1
                        break
        return count

    def average_msg_size(self, users=None):
        if users is None:
            users = self._names
        average = {user: 0 for user in users}
        msg_count = {user: 0 for user in users}
        with open(self._file_path, "r", encoding="utf-8") as average_file:
            while True:
                line = average_file.readline()
                if not line:
                    break
                if re.search(self._name_exp, line) is None:
                    continue
                msg = re.findall(self._name_exp, line)[0][1].split(" ")
                current_user = re.findall(self._name_exp, line)[0][0]

                if current_user in average:  # could be any dict
                    average[current_user] += len(msg) # for each of the users
                    msg_count[current_user] += 1
        for key in average:
            average[key] = float(str(average[key] / msg_count[key])[:4])
        return average

    def most_said_words(self, users=None, words=1):
        if users is None:
            users = self._names
        users_words = {user: dict() for user in users}  # each user has a dict containing the words and the count
        with open(self._file_path, "r", encoding="utf-8") as word_file:
            while True:
                line = word_file.readline()
                if not line:
                    break
                if re.search(self._name_exp, line) is None:
                    continue
                try:
                    current_user = re.findall(self._name_exp, line)[0][0]
                    current_word_dict = users_words[current_user]
                except KeyError:
                    continue
                for word in re.findall(self._name_exp, line)[0][1].split(" "):
                    word = word.casefold().strip()
                    if word == "omitted>":
                        continue
                    word = "Imagem Enviada" if word == "<media" else word

                    current_word_dict[word] = 0 if word not in current_word_dict else current_word_dict[word]
                    current_word_dict[word] += 1

        user_most_said = {user: dict() for user in users}
        for current_user in user_most_said:
            for i in range(words):
                current_words = users_words[current_user]
                max_count = max(current_words.values())
                max_key = None
                for key in current_words:
                    if current_words[key] == max_count:
                        max_key = key
                user_most_said[current_user][max_key] = users_words[current_user][max_key]
                del users_words[current_user][max_key]
        return user_most_said

    def how_many_words(self, word: str, users=None):
        if users is None:
            users = self._names
        users_counter = {user: 0 for user in users}
        with open(self._file_path, "r", encoding="utf-8") as word_file:
            while True:
                line = word_file.readline()
                if not line:
                    break
                if re.search(self._name_exp, line) is None:
                    continue
                current_user = re.findall(self._name_exp, line)[0][0]
                line = [x.casefold().strip() for x in re.findall(self._name_exp, line)[0][1].split(" ")]
                for user in users:
                    if user == current_user:
                        users_counter[user] += line.count(word.strip().casefold())
                        break
        return users_counter

    def extract_temporal_data(self, users=None, per_month=False):
        # month / day / year
        if users is None:
            users = self._names
        users_data = {user: dict() for user in users}
        with open(self._file_path, "r", encoding="utf-8") as date_file:
            while True:
                line = date_file.readline()
                if not line:
                    break
                if not re.search(self._date_exp, line) or not re.search(self._name_exp, line):
                    continue
                current_user = re.findall(self._name_exp, line)[0][0]
                if current_user in users:
                    # current_date: tuple = re.findall(self._date_exp, line)[0]
                    results = re.findall(self._date_exp, line)[0]
                    if not per_month:
                        current_date = "{}/{}/{}".format(results[1], results[0], results[2])
                    else:
                        current_date = str(results[0])
                    # print(re.findall(self._date_exp, line))
                    if current_date not in users_data[current_user]:
                        users_data[current_user][current_date] = 0
                    users_data[current_user][current_date] += 1
        return users_data

    def get_users(self):
        return self._names
