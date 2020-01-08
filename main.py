import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QAbstractItemView, QMessageBox
from PyQt5 import uic
import sqlite3


class CoffeeForm(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.parent = parent
        self.pb_add.clicked.connect(self.add)
        self.pb_save.clicked.connect(self.save)

        self.con = sqlite3.connect('coffee.db')
        self.cur = self.con.cursor()
        res = self.cur.execute("SELECT * FROM varieties").fetchall()
        self.table_edit.setColumnCount(7)
        self.table_edit.setHorizontalHeaderLabels(
            ['ID', 'name', "degree of\n\troasting",
             'grinding', 'description', 'price', 'volume']
        )

        self.row_count = len(res)
        self.table_edit.setRowCount(self.row_count)
        for i, row in enumerate(res):
            for j, elem in enumerate(row):
                self.table_edit.setItem(i, j, QTableWidgetItem(str(elem)))
        self.table_edit.resizeColumnsToContents()

    def add(self):
        self.table_edit.setRowCount(self.table_edit.rowCount() + 1)

    def save(self):
        self.cur.execute(
            f"DELETE FROM varieties"
        )
        for i in range(self.table_edit.rowCount()):
            row = []
            for j in range(self.table_edit.columnCount()):
                elem = self.table_edit.item(i, j).text()
                if elem != '':
                    row.append(elem)
                else:
                    self.lbl.setText('Нельзя оставлять пустые ячейки')
                    return
            self.cur.execute("INSERT INTO varieties VALUES ('" + "', '".join(row) + "');")
        self.con.commit()
        self.lbl.setText('Успешно сохраненно')
        self.parent.update_table()


class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.pb_edit.clicked.connect(self.edit)

        self.con = sqlite3.connect('coffee.db')
        self.cur = self.con.cursor()

        self.update_table()

    def edit(self):
        self.edit_widget = CoffeeForm(self)
        self.edit_widget.show()

    def update_table(self):
        res = self.cur.execute("SELECT * FROM varieties").fetchall()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ['ID', 'name', "degree of\n\troasting",
             'grinding', 'description', 'price', 'volume']
        )
        self.table.setRowCount(len(res))
        for i, row in enumerate(res):
            for j, elem in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(elem)))
        self.table.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffee()
    ex.show()
    sys.exit(app.exec_())
