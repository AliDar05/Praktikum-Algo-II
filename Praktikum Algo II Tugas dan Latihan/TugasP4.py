import sys
import mysql.connector as mc
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QTableWidgetItem
)
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

class MahasiswaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        print("DEBUG: Memulai aplikasi...")

        try:
            loadUi("TugasP4.ui", self)
            print("DEBUG: UI berhasil dimuat")
        except Exception as e:
            print(f"DEBUG: ERROR loadUi = {e}")
            sys.exit(1)

        self.btnLoad.clicked.connect(self.tambahData)
        self.btnSimpan.clicked.connect(self.ubahData)
        self.btnEdit.clicked.connect(self.hapusData)
        self.btnBatal.clicked.connect(self.clearForm)
        print("DEBUG: Semua tombol berhasil dikoneksikan")

        self.tableWidget.cellClicked.connect(self.tampilKeForm)

        self.loadData()

    def connectDB(self):
        try:
            db = mc.connect(
                host="localhost",
                user="root",
                password="dar25",
                database="db_mahasiswa"
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
            cursor.execute("SELECT * FROM mahasiswa ORDER BY npm ASC")
            results = cursor.fetchall()

            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(8)
            self.tableWidget.setHorizontalHeaderLabels([
                "NPM", "Nama Lengkap", "Nama Panggilan", "Telepon",
                "Email", "Kelas", "Matakuliah", "Lokasi Kampus"
            ])
            self.tableWidget.setColumnWidth(0, 100)
            self.tableWidget.setColumnWidth(1, 150)
            self.tableWidget.setColumnWidth(2, 120)
            self.tableWidget.setColumnWidth(3, 120)
            self.tableWidget.setColumnWidth(4, 180)
            self.tableWidget.setColumnWidth(5, 200)
            self.tableWidget.setColumnWidth(6, 150)
            self.tableWidget.setColumnWidth(7, 150)


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
        self.lineEditNpm.setText(self.tableWidget.item(row, 0).text())
        self.lineEditNamaLengkap.setText(self.tableWidget.item(row, 1).text())
        self.lineEditNamaPanggilan.setText(self.tableWidget.item(row, 2).text())
        self.lineEditTelepon.setText(self.tableWidget.item(row, 3).text())
        self.lineEditEmail.setText(self.tableWidget.item(row, 4).text())
        self.lineEditKelas.setText(self.tableWidget.item(row, 5).text())
        self.lineEditMatakuliah.setText(self.tableWidget.item(row, 6).text())
        self.lineEditLokasiKampus.setText(self.tableWidget.item(row, 7).text())

    def tambahData(self):
        npm = self.lineEditNpm.text().strip()
        nama = self.lineEditNamaLengkap.text().strip()
        panggilan = self.lineEditNamaPanggilan.text().strip()
        telepon = self.lineEditTelepon.text().strip()
        email = self.lineEditEmail.text().strip()
        kelas = self.lineEditKelas.text().strip()
        matakuliah = self.lineEditMatakuliah.text().strip()
        lokasi = self.lineEditLokasiKampus.text().strip()

        if not npm or not nama:
            QMessageBox.warning(self, "Input Error", "NPM dan Nama Lengkap wajib diisi!")
            return

        db = self.connectDB()
        if not db:
            return

        try:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO mahasiswa 
                (npm, nama_lengkap, nama_panggilan, telepon, email, kelas, matakuliah, lokasi_kampus)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (npm, nama, panggilan, telepon, email, kelas, matakuliah, lokasi))
            db.commit()
            QMessageBox.information(self, "Success", "Data berhasil ditambahkan!")
            self.loadData()
            self.clearForm()
        except mc.Error as err:
            print(f"DEBUG: tambahData ERROR = {err}")
            QMessageBox.critical(self, "Insert Error", str(err))
        db.close()

    def ubahData(self):
        npm = self.lineEditNpm.text().strip()
        nama = self.lineEditNamaLengkap.text().strip()
        panggilan = self.lineEditNamaPanggilan.text().strip()
        telepon = self.lineEditTelepon.text().strip()
        email = self.lineEditEmail.text().strip()
        kelas = self.lineEditKelas.text().strip()
        matakuliah = self.lineEditMatakuliah.text().strip()
        lokasi = self.lineEditLokasiKampus.text().strip()

        if not npm:
            QMessageBox.warning(self, "Input Error", "Pilih data dari tabel untuk diedit!")
            return

        db = self.connectDB()
        if not db:
            return

        try:
            cursor = db.cursor()
            cursor.execute("""
                UPDATE mahasiswa SET
                nama_lengkap=%s, nama_panggilan=%s, telepon=%s, email=%s, kelas=%s, matakuliah=%s, lokasi_kampus=%s
                WHERE npm=%s
            """, (nama, panggilan, telepon, email, kelas, matakuliah, lokasi, npm))
            db.commit()
            QMessageBox.information(self, "Success", "Data berhasil diupdate!")
            self.loadData()
            self.clearForm()
        except mc.Error as err:
            print(f"DEBUG: ubahData ERROR = {err}")
            QMessageBox.critical(self, "Update Error", str(err))
        db.close()

    def hapusData(self):
        npm = self.lineEditNpm.text().strip()
        if not npm:
            QMessageBox.warning(self, "Input Error", "Pilih data dari tabel untuk dihapus!")
            return

        db = self.connectDB()
        if not db:
            return

        try:
            cursor = db.cursor()
            cursor.execute("DELETE FROM mahasiswa WHERE npm=%s", (npm,))
            db.commit()
            QMessageBox.information(self, "Success", "Data berhasil dihapus!")
            self.loadData()
            self.clearForm()
        except mc.Error as err:
            print(f"DEBUG: hapusData ERROR = {err}")
            QMessageBox.critical(self, "Delete Error", str(err))
        db.close()

    def clearForm(self):
        self.lineEditNpm.clear()
        self.lineEditNamaLengkap.clear()
        self.lineEditNamaPanggilan.clear()
        self.lineEditTelepon.clear()
        self.lineEditEmail.clear()
        self.lineEditKelas.clear()
        self.lineEditMatakuliah.clear()
        self.lineEditLokasiKampus.clear()

def main():
    print("DEBUG: Memulai aplikasi")
    app = QApplication(sys.argv)
    window = MahasiswaApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()