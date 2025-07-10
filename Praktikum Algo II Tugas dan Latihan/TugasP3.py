import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt


class TableDataApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("Latihan3.ui", self)
        self.setWindowTitle("💜 Data Mahasiswa Versi Designer")

        self.pushButton_insert.clicked.connect(self.insert_data)
        self.pushButton_clear.clicked.connect(self.clear_table)
        self.pushButton_load.clicked.connect(self.load_data)

        self.setup_database()

        self.load_data()

    def setup_database(self):
        """Koneksi database"""
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='dar25',
                database='db_latihan'
            )
            self.cursor = self.connection.cursor()
            print("✅ Koneksi DB berhasil!")
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Gagal koneksi DB: {err}")
            sys.exit(1)

    def load_data(self):
        """Load data ke tabel"""
        try:
            query = "SELECT nama, jurusan FROM mhs ORDER BY id ASC"
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnWidth(1, 200)  # Kolom Nama
            self.tableWidget.setColumnWidth(2, 250)  # Kolom Jurusan (dibuat lebih lebar)
            for row_number, row_data in enumerate(results):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget.setItem(row_number, column_number, item)
            self.label_status.setText(f"💜 Loaded {len(results)} data mahasiswa")
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Gagal load data: {err}")

    def clear_table(self):
        """Clear tabel"""
        self.tableWidget.setRowCount(0)
        self.label_status.setText("🗑️ Tabel telah dibersihkan")

    def insert_data(self):
        """Insert data baru"""
        nama = self.lineEdit_nama.text().strip()
        jurusan = self.lineEdit_jurusan.text().strip()

        if not nama or not jurusan:
            QMessageBox.warning(self, "Input Error", "Nama dan Jurusan harus diisi!")
            return

        try:
            query = "INSERT INTO mhs (nama, jurusan) VALUES (%s, %s)"
            self.cursor.execute(query, (nama, jurusan))
            self.connection.commit()
            QMessageBox.information(self, "Success", "Data berhasil ditambahkan!")
            self.lineEdit_nama.clear()
            self.lineEdit_jurusan.clear()
            self.load_data()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Gagal insert data: {err}")

    def closeEvent(self, event):
        """Tutup koneksi DB saat aplikasi ditutup"""
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("🔌 Koneksi DB ditutup.")
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = TableDataApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
