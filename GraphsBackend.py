import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from GraphsWindow import Ui_BaseWindow
import numpy as np
import matplotlib.pyplot as plt


class GraphsWidget(QMainWindow, Ui_BaseWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.askButton.mousePressEvent = self.help
        self.calcButton.mousePressEvent = self.run

    def calc(self, string_function, x):
        try:  # если требуется постоянная функция y = x

            function = np.array([int(string_function) for _ in range(200)])

        except ValueError:

            try:
                functions = (" arcsin", " arccos", " arctan", " sin", " cos",
                             " tan", " exp", " log", " sqrt", " pi", " e")

                for math_function in functions:

                    # заменяем математические функции, удобные для восприятия человеком,
                    # на те, с которыми может работать matplotlib
                    if math_function in string_function:
                        string_function = string_function.replace(
                            math_function, f" np.{math_function[1:]}")

                function = eval(string_function)

            except (SyntaxError, NameError):
                return None  # в случае некорректного ввода

        return function

    def define_borders(self, border, edge):  # метод для определения границ графика

        if not border:  # значение по умолчанию
            return 100 * int(edge)  # edge - аргумент, указывающий, какойкрай обрабатывается

        if "pi" in border:  # в границах иногда может быть использовано число пи
            border.replace("pi", "np.pi")

            return eval(border)

        return int(border)

    def run(self, event):
        self.messageBox.setText('')
        mini, maxi = self.define_borders(self.leftBorderInput.text(), -1),\
            self.define_borders(self.rightBorderInput.text(), 1)  # границы

        fig, ax = plt.subplots()  # отрисовываем координатную плоскость

        ax.set_xlabel("x")
        ax.set_ylabel("y")
        try:
            graphs = 2  # количество графиков; если их не будет, ничего не получится начертить
            x = np.linspace(mini, maxi, 200)
            y1, y2 = self.calc(
                ' ' + self.functionInput.text(), x), self.calc(' ' + self.functionInput_2.text(), x)
            try:
                ax.plot(x, y1, color="blue", label="y1(x)")  # рисуем график

            except (ValueError, TypeError, SyntaxError):  # если графика нет
                graphs -= 1

            try:
                ax.plot(x, y2, color="red", label="y2(x)")

            except (ValueError, TypeError, SyntaxError):
                graphs -= 1

            if not graphs:
                raise ValueError

        except TypeError:  # некорректно указаны границы функции
            self.messageBox.setText(self.messageBox.text() + "Неверно указаны границы\n")

        except ValueError:  # оба поля для ввода функции пустые, ошибка вызывается намеренно
            self.messageBox.setText(
                self.messageBox.text() + "Укажите корректно хотя бы один график\n")

        else:  # отрисовываем
            ax.plot(x, np.array([0 for _ in range(200)]), color="black")  # ось х
            ax.legend()
            plt.show()

    def help(self, event):  # нажатие на кнопку знака вопроса для вывода вспомогательной информации
        self.messageBox.setText(
            '''1) Вводите только правую часть уравнения
2) Математические функции и константы вводите в следующем виде:
sin(x), cos(x), tan(x), arcsin(x), arccos(x), arctan(x), exp(x), log(x),
sqrt(x), pi, e
и только в области определения
3) Арифметические действия указывайте в формате:
+ - * / **''')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GraphsWidget()
    ex.show()
    sys.exit(app.exec_())
