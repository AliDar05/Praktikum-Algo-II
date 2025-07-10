import sys
import mysql.connector as mc
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QTableWidgetItem
)
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

class TableDataApp(QMainWindow):
    def __init__(self):
        super().__init__()
        print("DEBUG: Memulai aplikasi")

        try:
            loadUi("LatihanP4.ui", self)  # Pastikan file UI ada
            print("DEBUG: UI berhasil dimuat")
        except Exception as e:
            print(f"DEBUG: ERROR loadUi = {e}")
            sys.exit(1)

        # Connect tombol
        self.btnLoad.clicked.connect(self.loadData)
        self.btnSimpan.clicked.connect(self.simpanData)
        self.btnEdit.clicked.connect(self.editData)
        self.btnHapus.clicked.connect(self.hapusData)
        self.btnBatal.clicked.connect(self.clearForm)
        print("DEBUG: Semua tombol berhasil dikoneksikan")

        # Saat klik table, tampilkan di LineEdit
        self.tableWidget.cellClicked.connect(self.tampilKeForm)

        # Panggil load pertama kali
        self.loadData()

    def connectDB(self):
        try:
            db = mc.connect(
                host="localhost",
                user="root",
                password="dar25",
                database="db_latihan"
            )
            print("✅ Koneksi DB berhasil!")
            return db
        except mc.Error as err:
            print(f"❌ Koneksi DB gagal: {err}")
            QMessageBox.critical(self, "Database Error", str(err))
            return None

    def loadData(self):
        print("DEBUG: loadData dipanggil")
        db = self.connectDB()
        if not db:
            return

        cursor = db.cursor()
        try:
            cursor.execute("SELECT nama, jurusan FROM mhs_p4 ORDER BY nama ASC")
            results = cursor.fetchall()

            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnWidth(0, 250)
            self.tableWidget.setColumnWidth(1, 250)
            for row_num, row_data in enumerate(results):
                self.tableWidget.insertRow(row_num)
                for col_num, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget.setItem(row_num, col_num, item)

            print(f"DEBUG: {len(results)} data berhasil dimuat")
        except mc.Error as err:
            print(f"DEBUG: loadData ERROR = {err}")
            QMessageBox.critical(self, "Query Error", str(err))
        db.close()

    def tampilKeForm(self, row, _):
        nama = self.tableWidget.item(row, 0).text()
        jurusan = self.tableWidget.item(row, 1).text()
        self.lineEditNama.setText(nama)
        self.lineEditJurusan.setText(jurusan)

    def simpanData(self):
        nama = self.lineEditNama.text().strip()
        jurusan = self.lineEditJurusan.text().strip()
        if not nama or not jurusan:
            QMessageBox.warning(self, "Input Error", "Nama dan Jurusan harus diisi!")
            return

        db = self.connectDB()
        if not db:
            return

        try:
            cursor = db.cursor()
            cursor.execute("INSERT INTO mhs_p4 (nama, jurusan) VALUES (%s, %s)", (nama, jurusan))
            db.commit()
            QMessageBox.information(self, "Success", "Data berhasil disimpan!")
            self.loadData()
            self.clearForm()
        except mc.Error as err:
            print(f"DEBUG: simpanData ERROR = {err}")
            QMessageBox.critical(self, "Insert Error", str(err))
        db.close()

    def editData(self):
        nama = self.lineEditNama.text().strip()
        jurusan = self.lineEditJurusan.text().strip()
        if not nama or not jurusan:
            QMessageBox.warning(self, "Input Error", "Pilih data dari tabel untuk diedit!")
            return

        db = self.connectDB()
        if not db:
            return

        try:
            cursor = db.cursor()
            cursor.execute("UPDATE mhs_p4 SET jurusan=%s WHERE nama=%s", (jurusan, nama))
            db.commit()
            QMessageBox.information(self, "Success", "Data berhasil diupdate!")
            self.loadData()
            self.clearForm()
        except mc.Error as err:
            print(f"DEBUG: editData ERROR = {err}")
            QMessageBox.critical(self, "Update Error", str(err))
        db.close()

    def hapusData(self):
        nama = self.lineEditNama.text().strip()
        if not nama:
            QMessageBox.warning(self, "Input Error", "Pilih data dari tabel untuk dihapus!")
            return

        db = self.connectDB()
        if not db:
            return

        try:
            cursor = db.cursor()
            cursor.execute("DELETE FROM mhs_p4 WHERE nama=%s", (nama,))
            db.commit()
            QMessageBox.information(self, "Success", "Data berhasil dihapus!")
            self.loadData()
            self.clearForm()
        except mc.Error as err:
            print(f"DEBUG: hapusData ERROR = {err}")
            QMessageBox.critical(self, "Delete Error", str(err))
        db.close()

    def clearForm(self):
        self.lineEditNama.clear()
        self.lineEditJurusan.clear()

def main():
    print("DEBUG: Memulai aplikasi")
    app = QApplication(sys.argv)
    window = TableDataApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()