import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        uic.loadUi('main.ui', self)
        self.flag = None
        self.dao = Dao()
        self.tableWidget.itemClicked.connect(self.click)
        self.btn_change.clicked.connect(self.change_row)
        self.btn_add.clicked.connect(self.add_row)
        self.fill()

    def click(self):
        row = self.tableWidget.currentRow()
        id = int(self.tableWidget.item(row, 0).text())
        title = self.tableWidget.item(row, 1).text()
        roast = self.tableWidget.item(row, 2).text()
        type = self.tableWidget.item(row, 3).text()
        disc = self.tableWidget.item(row, 4).text()
        price = self.tableWidget.item(row, 5).text()
        vol = self.tableWidget.item(row, 6).text()
        self.coffee = Coffee(id, title, roast, type, disc, price, vol)
        self.btn_change.setEnabled(True)

    def change_row(self):
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.flag = True
        self.lineEdit_title.setText(self.coffee.title)
        self.lineEdit_roast.setText(self.coffee.roast)
        self.lineEdit_type.setText(self.coffee.type)
        self.lineEdit_descrip.setText(self.coffee.disc)
        self.lineEdit_price.setText(str(self.coffee.price))
        self.lineEdit_volume.setText(str(self.coffee.vol))
        self.btn_ok.clicked.connect(self.get_obj)

    def add_row(self):
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.flag = False
        self.btn_ok.clicked.connect(self.get_obj)
        self.btn_cancel.clicked.connect(self.close)

    def close(self):
        self.init()

    def get_obj(self):
        id = self.coffee.id
        title = self.lineEdit_title.text()
        roast = self.lineEdit_roast.text()
        type = self.lineEdit_type.text()
        disc = self.lineEdit_descrip.text()
        price = self.lineEdit_price.text()
        vol = self.lineEdit_volume.text()
        self.coffee = Coffee(id, title, roast, type, disc, price, vol)
        if self.flag:
            self.dao.update_row(self.coffee)
        elif not self.flag:
            self.dao.insert_row(self.coffee)
        self.init()

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
        self.conn = sqlite3.connect("coffee.db")

    def get_all(self):
        cur = self.conn.cursor()
        result = cur.execute("""SELECT * FROM coffee""").fetchall()
        return result

    def insert_row(self, obj):
        cursor = self.conn.cursor()
        cursor.execute("""insert into coffee(title, roast, type, discription, price, volume) 
        VALUES (?, ?, ?, ?, ?, ?)""", (obj.title, obj.roast, obj.type, obj.disc, obj.price, obj.vol))
        self.conn.commit()

    def update_row(self, obj):
        cursor = self.conn.cursor()
        cursor.execute("""update coffee set title = ?, roast = ?, type = ?, discription = ?, price = ?, volume = ? 
        where id = ?""",
                       (obj.title, obj.roast, obj.type, obj.disc, obj.price, obj.vol, obj.id))
        self.conn.commit()


class Coffee:
    def __init__(self, id, title, roast, type, disc, price, vol):
        self.id = id
        self.title = title
        self.roast = roast
        self.type = type
        self.disc = disc
        self.price = price
        self.vol = vol


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())