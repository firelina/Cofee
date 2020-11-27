import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

from Ui.add import UiAddEditForm
from Ui.main_inter import Ui_MainWindow


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.form = EditForm()
        self.setupUi(self)
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
        self.form.show()
        self.form.lineEdit_title.setText(self.coffee.title)
        self.form.lineEdit_roast.setText(self.coffee.roast)
        self.form.lineEdit_type.setText(self.coffee.type)
        self.form.lineEdit_descrip.setText(self.coffee.disc)
        self.form.lineEdit_price.setText(str(self.coffee.price))
        self.form.lineEdit_volume.setText(str(self.coffee.vol))
        self.form.btn_ok.clicked.connect(self.change_obj)
        self.form.btn_cancel.clicked.connect(self.close)

    def add_row(self):
        self.form.show()
        self.form.lineEdit_title.setText('')
        self.form.lineEdit_roast.setText('')
        self.form.lineEdit_type.setText('')
        self.form.lineEdit_descrip.setText('')
        self.form.lineEdit_price.setText('')
        self.form.lineEdit_volume.setText('')
        self.form.btn_ok.clicked.connect(self.add_obj)
        self.form.btn_cancel.clicked.connect(self.close)

    def close(self):
        # print(self.form.sender())
        self.form.close()
        self.form = EditForm()
        self.fill()

    def add_obj(self):
        id = None
        title = self.form.lineEdit_title.text()
        roast = self.form.lineEdit_roast.text()
        type = self.form.lineEdit_type.text()
        disc = self.form.lineEdit_descrip.text()
        price = self.form.lineEdit_price.text()
        vol = self.form.lineEdit_volume.text()
        coffee = Coffee(id, title, roast, type, disc, price, vol)
        self.dao.insert_row(coffee)
        self.close()

    def change_obj(self):
        id = self.coffee.id
        title = self.form.lineEdit_title.text()
        roast = self.form.lineEdit_roast.text()
        type = self.form.lineEdit_type.text()
        disc = self.form.lineEdit_descrip.text()
        price = self.form.lineEdit_price.text()
        vol = self.form.lineEdit_volume.text()
        coffee = Coffee(id, title, roast, type, disc, price, vol)
        self.dao.update_row(coffee)
        self.close()

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
        self.conn = sqlite3.connect("Data\coffee.db")

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


class EditForm(QMainWindow, UiAddEditForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Form')


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