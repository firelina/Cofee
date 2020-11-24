import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.dao = Dao()
        self.fill()

    def fill(self):
        res = self.dao.get_all()
        listt = ['ID', 'Название', 'Прожарка', 'Тип', 'Описание', 'Цена(рубли)', 'Объём(см^3)']

        self.tableWidget.setColumnCount(len(listt))
        self.tableWidget.setHorizontalHeaderLabels(listt)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                item = QTableWidgetItem()
                elem = str(elem)
                if elem.isdigit():
                    item.setData(Qt.EditRole, int(elem))
                else:
                    item.setData(Qt.EditRole, elem)
                self.tableWidget.setItem(i, j, item)
        self.tableWidget.resizeColumnsToContents()


class Dao:
    def __init__(self):
        self.con = sqlite3.connect("coffee.db")

    def get_all(self):
        cur = self.con.cursor()
        result = cur.execute("""SELECT * FROM coffee""").fetchall()
        return result


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())