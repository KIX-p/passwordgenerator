import math
import string
import sys
import random

import self
from PyQt6.QtWidgets import QDialog, QApplication, QMessageBox

from layout import Ui_Dialog


class MyForm(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.generate.clicked.connect(self.generate)
        self.ui.easter.clicked.connect(self.easterClicked)
        self.ui.word.toggled.connect(self.readDict)
        # zasobnik znakow
        self.smallChars = [l for l in string.ascii_lowercase]
        self.capitalChars = [l for l in string.ascii_uppercase]
        self.numbers = [l for l in string.digits]
        self.specialChars = [l for l in string.punctuation]


    def generate(self):
        lenght = self.ui.length.text()
        type = self.ui.passwordtype.currentText()
        password = ''

        if int(lenght) <= 6:
            QMessageBox.warning(self, "Blad", "Haslo nie moze byc krotkie")
            return

        if type == 'pin':
            for i in range(int(lenght)):
                password += str(random.randint(0, 9))
        elif self.ui.word.isChecked():
            words = self.readDict('odm.txt')
            while len(password) < int(lenght):
                password += random.choice(words)
        else:
            elements = [self.smallChars]
            if self.ui.specialchar.isChecked():
                elements.append(self.specialChars)
            if self.ui.numbers.isChecked():
                elements.append(self.numbers)
            if self.ui.capital.isChecked():
                elements.append(self.capitalChars)
            for i in range(int(lenght)):
                type = random.randint(0, len(elements) - 1)
                password += elements[type][random.randint(0, len(elements[type]) - 1)]

            if self.ui.easter.isChecked() and len(password) >= 5:
                max_index = len(password) - 6
                start_index = random.randint(0, max_index)
                new_password = ''
                easter = 'zajac'
                for i in range(len(password)):
                    if start_index <= i <= start_index + 5:
                        new_password += easter[i - start_index]
                    else:
                        new_password += password[i]
                password = new_password
                self.ui.generatedpassword.setText(password)

    def readDict(self, path):
        words = []
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                line = line.split(',')[0]
                line = line.replace('\n', '')
                if len(line) > 2 and line.find(' ') == -1:
                    words.append(line)
        return words

    def easterClicked(self):
        if self.ui.easter.isChecked():
            self.ui.numbers.setChecked(False)
            self.ui.capital.setChecked(False)
            self.ui.specialchar.setChecked(False)
            self.ui.word.setChecked(False)
            self.ui.numbers.setDisabled(True)
            self.ui.capital.setDisabled(True)
            self.ui.specialchar.setDisabled(True)
            self.ui.word.setDisabled(True)
        else:
            self.ui.numbers.setChecked(True)
            self.ui.capital.setChecked(True)
            self.ui.specialchar.setChecked(True)
            self.ui.word.setChecked(True)
            self.ui.numbers.setDisabled(False)
            self.ui.capital.setDisabled(False)
            self.ui.specialchar.setDisabled(False)
            self.ui.word.setDisabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MyForm()
    form.show()
    sys.exit(app.exec())
