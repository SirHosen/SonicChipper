#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SonicCipher - Aplikasi Kriptografi Teks ke Suara
Dikembangkan untuk Tugas Mata Kuliah Kriptografi

File utama untuk menjalankan aplikasi
"""

import sys
import os
import traceback
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QIcon

# Fungsi untuk menangkap error yang tidak tertangani
def exception_hook(exctype, value, tb):
    traceback.print_exception(exctype, value, tb)
    sys.exit(1)

# Set exception hook
sys.excepthook = exception_hook

def main():
    # Inisialisasi aplikasi
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Untuk tampilan yang konsisten di semua platform
    
    # Set ikon aplikasi
    if os.path.exists("resources/icon.png"):
        app.setWindowIcon(QIcon("resources/icon.png"))
    
    # Tampilkan splash screen
    if os.path.exists("resources/splash.png"):
        splash_pix = QPixmap("resources/splash.png")
    else:
        # Buat splash screen sederhana jika gambar tidak ditemukan
        splash_pix = QPixmap(500, 300)
        splash_pix.fill(Qt.white)
    
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    splash.show()
    splash.showMessage("Memuat SonicCipher...", Qt.AlignBottom | Qt.AlignCenter, Qt.black)
    app.processEvents()
    
    # Import UI setelah splash screen ditampilkan
    from ui_design import SonicCipherApp
    
    # Inisialisasi main window dengan delay
    def show_main_window():
        window = SonicCipherApp()
        window.show()
        splash.finish(window)
    
    # Tampilkan main window setelah 1.5 detik
    QTimer.singleShot(1500, show_main_window)
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
