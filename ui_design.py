#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SonicCipher - Aplikasi Kriptografi Teks ke Suara
UI Design - Antarmuka pengguna utama
"""

import os
import numpy as np
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QTabWidget, QLabel, QLineEdit, QTextEdit, 
                            QPushButton, QFileDialog, QSpinBox, QProgressBar,
                            QMessageBox, QSlider, QGroupBox, QSplitter, 
                            QComboBox, QCheckBox, QInputDialog, QToolTip, 
                            QStatusBar, QAction, QMenu, QToolBar, QFrame,
                            QRadioButton, QButtonGroup, QSizePolicy, QApplication)  # Tambahkan QApplication di sini
from PyQt5.QtCore import Qt, QUrl, QSize, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPalette, QColor, QDesktopServices
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Qt5Agg')

from audio_processor import AudioProcessor
from visualizer import AudioVisualizer
from utils import create_icon_button, set_dark_theme, create_separator

class EncryptionThread(QThread):
    """Thread terpisah untuk proses enkripsi"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    progress = pyqtSignal(int)
    
    def __init__(self, audio_processor, text, key, base_freq, base_duration):
        super().__init__()
        self.audio_processor = audio_processor
        self.text = text
        self.key = key
        self.base_freq = base_freq
        self.base_duration = base_duration
    
    def run(self):
        try:
            # Simulasi progress
            for i in range(0, 101, 5):
                self.progress.emit(i)
                self.msleep(50)  # Delay kecil untuk simulasi proses
                
            # Proses enkripsi sebenarnya
            result = self.audio_processor.encrypt_to_audio(
                self.text, self.key, self.base_freq, self.base_duration
            )
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

class DecryptionThread(QThread):
    """Thread terpisah untuk proses dekripsi"""
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    progress = pyqtSignal(int)
    
    def __init__(self, audio_processor, audio_data, sample_rate, key, tolerance, metadata):
        super().__init__()
        self.audio_processor = audio_processor
        self.audio_data = audio_data
        self.sample_rate = sample_rate
        self.key = key
        self.tolerance = tolerance
        self.metadata = metadata
    
    def run(self):
        try:
            # Simulasi progress
            for i in range(0, 101, 5):
                self.progress.emit(i)
                self.msleep(50)  # Delay kecil untuk simulasi proses
            
            # Proses dekripsi sebenarnya
            result = self.audio_processor.decrypt_from_audio(
                self.audio_data, self.sample_rate, self.key, self.tolerance, self.metadata
            )
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

class SonicCipherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Inisialisasi processor dan visualizer
        self.audio_processor = AudioProcessor()
        self.visualizer = AudioVisualizer()
        
        # Variabel untuk menyimpan data
        self.encrypted_data = None
        self.audio_file_path = None
        self.is_dark_mode = False
        
        # Setup UI
        self.init_ui()
        
        # Tampilkan pesan selamat datang
        self.statusBar().showMessage("Selamat datang di SonicCipher! Aplikasi siap digunakan.")
        
    def init_ui(self):
        # Setup window
        self.setWindowTitle('SonicCipher - Aplikasi Kriptografi Teks ke Suara')
        self.setGeometry(100, 100, 1000, 700)
        
        # Menu bar
        self.create_menu_bar()
        
        # Toolbar
        self.create_toolbar()
        
        # Widget utama dan layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Header dengan logo
        header_layout = QHBoxLayout()
        
        # Logo (jika tersedia)
        if os.path.exists("resources/logo.png"):
            logo_label = QLabel()
            logo_pixmap = QPixmap("resources/logo.png").scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(logo_pixmap)
            header_layout.addWidget(logo_label)
        
        # Judul aplikasi
        title_layout = QVBoxLayout()
        title_label = QLabel('SonicCipher')
        title_label.setFont(QFont('Segoe UI', 28, QFont.Bold))
        title_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel('Aplikasi Kriptografi Teks ke Suara')
        subtitle_label.setFont(QFont('Segoe UI', 14))
        title_layout.addWidget(subtitle_label)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        
        main_layout.addLayout(header_layout)
        
        # Garis pemisah
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setFont(QFont('Segoe UI', 10))
        main_layout.addWidget(self.tab_widget)
        
        # Tab Enkripsi
        encrypt_tab = QWidget()
        self.tab_widget.addTab(encrypt_tab, "Enkripsi")
        self.setup_encrypt_tab(encrypt_tab)
        
        # Tab Dekripsi
        decrypt_tab = QWidget()
        self.tab_widget.addTab(decrypt_tab, "Dekripsi")
        self.setup_decrypt_tab(decrypt_tab)
        
        # Tab Visualisasi
        visual_tab = QWidget()
        self.tab_widget.addTab(visual_tab, "Visualisasi")
        self.setup_visual_tab(visual_tab)
        
        # Tab Tentang
        about_tab = QWidget()
        self.tab_widget.addTab(about_tab, "Tentang")
        self.setup_about_tab(about_tab)
        
        # Footer
        footer_layout = QHBoxLayout()
        footer_label = QLabel("© 2025 SonicCipher - Tugas Mata Kuliah Kriptografi")
        footer_label.setFont(QFont('Segoe UI', 8))
        footer_layout.addWidget(footer_label)
        
        # Version
        version_label = QLabel("v1.0.0")
        version_label.setFont(QFont('Segoe UI', 8))
        version_label.setAlignment(Qt.AlignRight)
        footer_layout.addWidget(version_label)
        
        main_layout.addLayout(footer_layout)
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # Menu File
        file_menu = menubar.addMenu('File')
        
        # Action untuk membuka file
        open_action = QAction('Buka File Audio', self)
        if os.path.exists('resources/open.png'):
            open_action.setIcon(QIcon('resources/open.png'))
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.browse_audio_file)
        file_menu.addAction(open_action)
        
        # Action untuk menyimpan file
        save_action = QAction('Simpan Audio', self)
        if os.path.exists('resources/save.png'):
            save_action.setIcon(QIcon('resources/save.png'))
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_encrypted_sound)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        # Action untuk keluar
        exit_action = QAction('Keluar', self)
        if os.path.exists('resources/exit.png'):
            exit_action.setIcon(QIcon('resources/exit.png'))
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menu Edit
        edit_menu = menubar.addMenu('Edit')
        
        # Action untuk clear input
        clear_action = QAction('Bersihkan Input', self)
        clear_action.triggered.connect(self.clear_inputs)
        edit_menu.addAction(clear_action)
        
        edit_menu.addSeparator()
        
        # Action untuk preferensi
        pref_action = QAction('Preferensi', self)
        pref_action.triggered.connect(self.show_preferences)
        edit_menu.addAction(pref_action)
        
        # Menu Alat
        tools_menu = menubar.addMenu('Alat')
        
        # Action untuk pengujian
        test_action = QAction('Uji Enkripsi-Dekripsi', self)
        test_action.triggered.connect(self.run_encryption_test)
        tools_menu.addAction(test_action)
        
        # Action untuk analisis audio
        analyze_action = QAction('Analisis Audio', self)
        analyze_action.triggered.connect(self.analyze_audio)
        tools_menu.addAction(analyze_action)
        
        # Menu Bantuan
        help_menu = menubar.addMenu('Bantuan')
        
        # Action untuk bantuan
        help_action = QAction('Panduan Pengguna', self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)
        
        # Action untuk tentang
        about_action = QAction('Tentang SonicCipher', self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)
        
        # Tombol enkripsi
        encrypt_action = QAction('Enkripsi', self)
        if os.path.exists('resources/encrypt.png'):
            encrypt_action.setIcon(QIcon('resources/encrypt.png'))
        encrypt_action.triggered.connect(self.quick_encrypt)
        toolbar.addAction(encrypt_action)
        
        # Tombol dekripsi
        decrypt_action = QAction('Dekripsi', self)
        if os.path.exists('resources/decrypt.png'):
            decrypt_action.setIcon(QIcon('resources/decrypt.png'))
        decrypt_action.triggered.connect(self.quick_decrypt)
        toolbar.addAction(decrypt_action)
        
        toolbar.addSeparator()
        
        # Tombol putar
        play_action = QAction('Putar Audio', self)
        if os.path.exists('resources/play.png'):
            play_action.setIcon(QIcon('resources/play.png'))
        play_action.triggered.connect(self.play_current_audio)
        toolbar.addAction(play_action)
        
        # Tombol stop
        stop_action = QAction('Stop Audio', self)
        if os.path.exists('resources/stop.png'):
            stop_action.setIcon(QIcon('resources/stop.png'))
        stop_action.triggered.connect(self.stop_audio)
        toolbar.addAction(stop_action)
        
        toolbar.addSeparator()
        
        # Tombol bantuan
        help_action = QAction('Bantuan', self)
        if os.path.exists('resources/help.png'):
            help_action.setIcon(QIcon('resources/help.png'))
        help_action.triggered.connect(self.show_help)
        toolbar.addAction(help_action)
    
    def setup_encrypt_tab(self, tab):
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Splitter untuk membagi area input dan visualisasi
        splitter = QSplitter(Qt.Vertical)
        splitter.setChildrenCollapsible(False)
        
        # Panel atas: input dan pengaturan
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        
        # Area input teks
        text_group = QGroupBox("Pesan untuk Dienkripsi")
        text_group.setFont(QFont('Segoe UI', 10, QFont.Bold))
        text_layout = QVBoxLayout(text_group)
        
        self.plaintext_input = QTextEdit()
        self.plaintext_input.setPlaceholderText("Masukkan pesan yang ingin dienkripsi...")
        self.plaintext_input.setFont(QFont('Segoe UI', 10))
        self.plaintext_input.setMinimumHeight(100)
        text_layout.addWidget(self.plaintext_input)
        
        # Informasi karakter
        char_layout = QHBoxLayout()
        self.char_count_label = QLabel("Karakter: 0")
        char_layout.addWidget(self.char_count_label)
        char_layout.addStretch()
        
        # Tombol bersihkan
        clear_btn = create_icon_button("Bersihkan", "resources/clear.png", lambda: self.plaintext_input.clear())
        char_layout.addWidget(clear_btn)
        
        text_layout.addLayout(char_layout)
        
        # Connect text changed signal
        self.plaintext_input.textChanged.connect(self.update_char_count)
        
        top_layout.addWidget(text_group)
        
        # Pengaturan enkripsi
        settings_group = QGroupBox("Pengaturan Enkripsi")
        settings_group.setFont(QFont('Segoe UI', 10, QFont.Bold))
        settings_layout = QHBoxLayout(settings_group)
        
        # Kunci enkripsi
        key_layout = QVBoxLayout()
        key_layout.addWidget(QLabel("Kunci Enkripsi (1-25):"))
        self.encrypt_key = QSpinBox()
        self.encrypt_key.setRange(1, 25)
        self.encrypt_key.setValue(7)
        self.encrypt_key.setFont(QFont('Segoe UI', 10))
        key_layout.addWidget(self.encrypt_key)
        settings_layout.addLayout(key_layout)
        
        # Pengaturan frekuensi
        freq_layout = QVBoxLayout()
        freq_label = QLabel("Frekuensi Dasar (Hz):")
        freq_label.setToolTip("Frekuensi dasar untuk pemetaan karakter.\nNilai yang lebih tinggi menghasilkan suara yang lebih tinggi.")
        freq_layout.addWidget(freq_label)
        
        self.base_freq = QSpinBox()
        self.base_freq.setRange(200, 500)
        self.base_freq.setValue(220)
        self.base_freq.setSingleStep(10)
        self.base_freq.setFont(QFont('Segoe UI', 10))
        self.base_freq.setToolTip(freq_label.toolTip())
        freq_layout.addWidget(self.base_freq)
        settings_layout.addLayout(freq_layout)
        
        # Pengaturan durasi
        duration_layout = QVBoxLayout()
        duration_label = QLabel("Durasi Dasar (ms):")
        duration_label.setToolTip("Durasi dasar untuk setiap nada.\nNilai yang lebih tinggi membuat suara lebih lambat tetapi lebih jelas.")
        duration_layout.addWidget(duration_label)
        
        self.base_duration = QSpinBox()
        self.base_duration.setRange(50, 500)
        self.base_duration.setValue(100)
        self.base_duration.setSingleStep(10)
        self.base_duration.setFont(QFont('Segoe UI', 10))
        self.base_duration.setToolTip(duration_label.toolTip())
        duration_layout.addWidget(self.base_duration)
        settings_layout.addLayout(duration_layout)
        
        # Pengaturan algoritma
        algo_layout = QVBoxLayout()
        algo_layout.addWidget(QLabel("Algoritma:"))
        
        self.algorithm_combo = QComboBox()
        self.algorithm_combo.addItem("FSAE Standard")
        self.algorithm_combo.addItem("FSAE Enhanced")
        self.algorithm_combo.addItem("FSAE + AES")
        self.algorithm_combo.setFont(QFont('Segoe UI', 10))
        self.algorithm_combo.setToolTip("Algoritma enkripsi yang digunakan.\nFSAE Standard: Algoritma dasar\nFSAE Enhanced: Dengan variasi durasi tambahan\nFSAE + AES: Dengan enkripsi AES tambahan")
        algo_layout.addWidget(self.algorithm_combo)
        settings_layout.addLayout(algo_layout)
        
        top_layout.addWidget(settings_group)
        
        # Tombol aksi
        buttons_layout = QHBoxLayout()
        
        self.encrypt_btn = QPushButton("Enkripsi ke Suara")
        if os.path.exists('resources/encrypt.png'):
            self.encrypt_btn.setIcon(QIcon('resources/encrypt.png'))
        self.encrypt_btn.setFont(QFont('Segoe UI', 10))
        self.encrypt_btn.clicked.connect(self.encrypt_message)
        buttons_layout.addWidget(self.encrypt_btn)
        
        self.play_btn = QPushButton("Putar Suara")
        if os.path.exists('resources/play.png'):
            self.play_btn.setIcon(QIcon('resources/play.png'))
        self.play_btn.setFont(QFont('Segoe UI', 10))
        self.play_btn.clicked.connect(self.play_encrypted_sound)
        self.play_btn.setEnabled(False)
        buttons_layout.addWidget(self.play_btn)
        
        self.save_btn = QPushButton("Simpan Suara")
        if os.path.exists('resources/save.png'):
            self.save_btn.setIcon(QIcon('resources/save.png'))
        self.save_btn.setFont(QFont('Segoe UI', 10))
        self.save_btn.clicked.connect(self.save_encrypted_sound)
        self.save_btn.setEnabled(False)
        buttons_layout.addWidget(self.save_btn)
        
        top_layout.addLayout(buttons_layout)
        
        # Progress bar
        self.encrypt_progress = QProgressBar()
        self.encrypt_progress.setRange(0, 100)
        self.encrypt_progress.setValue(0)
        self.encrypt_progress.setTextVisible(True)
        self.encrypt_progress.setFormat("%p% - %v dari %m")
        self.encrypt_progress.setVisible(False)
        top_layout.addWidget(self.encrypt_progress)
        
        splitter.addWidget(top_widget)
        
        # Panel bawah: visualisasi
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        
        # Visualisasi
        visual_group = QGroupBox("Visualisasi Audio")
        visual_group.setFont(QFont('Segoe UI', 10, QFont.Bold))
        visual_layout = QVBoxLayout(visual_group)
        
        # Tabs untuk visualisasi berbeda
        visual_tabs = QTabWidget()
        
        # Tab spektrogram
        spec_tab = QWidget()
        spec_layout = QVBoxLayout(spec_tab)
        
        self.encrypt_figure = Figure(figsize=(5, 4), dpi=100)
        self.encrypt_canvas = FigureCanvas(self.encrypt_figure)
        spec_layout.addWidget(self.encrypt_canvas)
        
        visual_tabs.addTab(spec_tab, "Spektrogram")
        
        # Tab waveform
        wave_tab = QWidget()
        wave_layout = QVBoxLayout(wave_tab)
        
        self.encrypt_wave_figure = Figure(figsize=(5, 4), dpi=100)
        self.encrypt_wave_canvas = FigureCanvas(self.encrypt_wave_figure)
        wave_layout.addWidget(self.encrypt_wave_canvas)
        
        visual_tabs.addTab(wave_tab, "Waveform")
        
        # Tab frekuensi
        freq_tab = QWidget()
        freq_layout = QVBoxLayout(freq_tab)
        
        self.encrypt_freq_figure = Figure(figsize=(5, 4), dpi=100)
        self.encrypt_freq_canvas = FigureCanvas(self.encrypt_freq_figure)
        freq_layout.addWidget(self.encrypt_freq_canvas)
        
        visual_tabs.addTab(freq_tab, "Analisis Frekuensi")
        
        visual_layout.addWidget(visual_tabs)
        
        bottom_layout.addWidget(visual_group)
        
        splitter.addWidget(bottom_widget)
        
        # Set proporsi splitter
        splitter.setSizes([400, 300])
        
        layout.addWidget(splitter)
        
    def setup_decrypt_tab(self, tab):
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Splitter untuk membagi area input dan hasil
        splitter = QSplitter(Qt.Vertical)
        splitter.setChildrenCollapsible(False)
        
        # Panel atas: input file dan pengaturan
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        
        # Area input file
        file_group = QGroupBox("File Audio Terenkripsi")
        file_group.setFont(QFont('Segoe UI', 10, QFont.Bold))
        file_layout = QVBoxLayout(file_group)
        
        # Drag & drop area
        drop_area = QGroupBox()
        drop_area.setStyleSheet("""
            QGroupBox {
                border: 2px dashed #aaa;
                border-radius: 5px;
                padding: 20px;
                background-color: rgba(200, 200, 200, 0.1);
            }
        """)
        drop_layout = QVBoxLayout(drop_area)
        
        drop_icon = QLabel()
        if os.path.exists("resources/upload.png"):
            drop_pixmap = QPixmap("resources/upload.png").scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            drop_icon.setPixmap(drop_pixmap)
            drop_icon.setAlignment(Qt.AlignCenter)
        drop_layout.addWidget(drop_icon)
        
        drop_label = QLabel("Seret file audio terenkripsi ke sini atau klik untuk memilih file")
        drop_label.setFont(QFont('Segoe UI', 10))
        drop_label.setAlignment(Qt.AlignCenter)
        drop_layout.addWidget(drop_label)
        
        browse_btn = QPushButton("Pilih File")
        browse_btn.setFont(QFont('Segoe UI', 10))
        browse_btn.clicked.connect(self.browse_audio_file)
        browse_btn.setMaximumWidth(150)
        drop_layout.addWidget(browse_btn, alignment=Qt.AlignCenter)
        
        file_layout.addWidget(drop_area)
        
        # Display file path
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("File:"))
        
        self.file_path_display = QLineEdit()
        self.file_path_display.setReadOnly(True)
        self.file_path_display.setPlaceholderText("Belum ada file yang dipilih")
        self.file_path_display.setFont(QFont('Segoe UI', 10))
        path_layout.addWidget(self.file_path_display)
        
        file_layout.addLayout(path_layout)
        
        # Metadata status
        self.metadata_status = QLabel("Status Metadata: Belum diperiksa")
        self.metadata_status.setFont(QFont('Segoe UI', 10))
        file_layout.addWidget(self.metadata_status)
        
        top_layout.addWidget(file_group)
        
        # Pengaturan dekripsi
        settings_group = QGroupBox("Pengaturan Dekripsi")
        settings_group.setFont(QFont('Segoe UI', 10, QFont.Bold))
        settings_layout = QHBoxLayout(settings_group)
        
        # Kunci dekripsi
        key_layout = QVBoxLayout()
        key_label = QLabel("Kunci Dekripsi (1-25):")
        key_label.setToolTip("Kunci yang digunakan untuk dekripsi.\nHarus sama dengan kunci yang digunakan saat enkripsi.")
        key_layout.addWidget(key_label)
        
        self.decrypt_key = QSpinBox()
        self.decrypt_key.setRange(1, 25)
        self.decrypt_key.setValue(7)
        self.decrypt_key.setFont(QFont('Segoe UI', 10))
        self.decrypt_key.setToolTip(key_label.toolTip())
        key_layout.addWidget(self.decrypt_key)
        settings_layout.addLayout(key_layout)
        
        # Toleransi frekuensi
        tolerance_layout = QVBoxLayout()
        tolerance_label = QLabel("Toleransi Frekuensi (%):")
        tolerance_label.setToolTip(
            "Toleransi frekuensi membantu dekripsi saat ada distorsi audio.\n"
            "Nilai rendah (1-2%): Lebih akurat, tetapi sensitif terhadap distorsi.\n"
            "Nilai sedang (5-10%): Keseimbangan antara akurasi dan toleransi distorsi.\n"
            "Nilai tinggi (>10%): Dapat mengatasi distorsi besar, tetapi berisiko kesalahan dekripsi."
        )
        tolerance_layout.addWidget(tolerance_label)
        
        self.freq_tolerance = QSpinBox()
        self.freq_tolerance.setRange(1, 20)
        self.freq_tolerance.setValue(5)
        self.freq_tolerance.setFont(QFont('Segoe UI', 10))
        self.freq_tolerance.setToolTip(tolerance_label.toolTip())
        tolerance_layout.addWidget(self.freq_tolerance)
        settings_layout.addLayout(tolerance_layout)
        
        # Metode dekripsi
        method_layout = QVBoxLayout()
        method_label = QLabel("Metode Dekripsi:")
        method_label.setToolTip("Pilih metode dekripsi yang akan digunakan.")
        method_layout.addWidget(method_label)
        
        self.decrypt_method = QComboBox()
        self.decrypt_method.addItem("Otomatis (Metadata jika tersedia)")
        self.decrypt_method.addItem("Gunakan Metadata")
        self.decrypt_method.addItem("Analisis Audio")
        self.decrypt_method.setFont(QFont('Segoe UI', 10))
        self.decrypt_method.setToolTip(method_label.toolTip())
        method_layout.addWidget(self.decrypt_method)
        settings_layout.addLayout(method_layout)
        
        # Pengaturan frekuensi dasar
        base_freq_layout = QVBoxLayout()
        base_freq_label = QLabel("Frekuensi Dasar (Hz):")
        base_freq_label.setToolTip("Frekuensi dasar untuk dekripsi tanpa metadata.\nHarus sama dengan nilai yang digunakan saat enkripsi.")
        base_freq_layout.addWidget(base_freq_label)
        
        self.decrypt_base_freq = QSpinBox()
        self.decrypt_base_freq.setRange(200, 500)
        self.decrypt_base_freq.setValue(220)
        self.decrypt_base_freq.setSingleStep(10)
        self.decrypt_base_freq.setFont(QFont('Segoe UI', 10))
        self.decrypt_base_freq.setToolTip(base_freq_label.toolTip())
        base_freq_layout.addWidget(self.decrypt_base_freq)
        settings_layout.addLayout(base_freq_layout)
        
        top_layout.addWidget(settings_group)
        
        # Tombol aksi
        buttons_layout = QHBoxLayout()
        
        self.play_encrypted_btn = QPushButton("Putar Audio Terenkripsi")
        if os.path.exists('resources/play.png'):
            self.play_encrypted_btn.setIcon(QIcon('resources/play.png'))
        self.play_encrypted_btn.setFont(QFont('Segoe UI', 10))
        self.play_encrypted_btn.clicked.connect(self.play_loaded_audio)
        self.play_encrypted_btn.setEnabled(False)
        buttons_layout.addWidget(self.play_encrypted_btn)
        
        self.decrypt_btn = QPushButton("Dekripsi Suara")
        if os.path.exists('resources/decrypt.png'):
            self.decrypt_btn.setIcon(QIcon('resources/decrypt.png'))
        self.decrypt_btn.setFont(QFont('Segoe UI', 10))
        self.decrypt_btn.clicked.connect(self.decrypt_audio)
        self.decrypt_btn.setEnabled(False)
        buttons_layout.addWidget(self.decrypt_btn)
        
        self.copy_result_btn = QPushButton("Salin Hasil")
        if os.path.exists('resources/copy.png'):
            self.copy_result_btn.setIcon(QIcon('resources/copy.png'))
        self.copy_result_btn.setFont(QFont('Segoe UI', 10))
        self.copy_result_btn.clicked.connect(self.copy_decrypted_text)
        self.copy_result_btn.setEnabled(False)
        buttons_layout.addWidget(self.copy_result_btn)
        
        top_layout.addLayout(buttons_layout)
        
        # Progress bar
        self.decrypt_progress = QProgressBar()
        self.decrypt_progress.setRange(0, 100)
        self.decrypt_progress.setValue(0)
        self.decrypt_progress.setTextVisible(True)
        self.decrypt_progress.setFormat("%p% - %v dari %m")
        self.decrypt_progress.setVisible(False)
        top_layout.addWidget(self.decrypt_progress)
        
        splitter.addWidget(top_widget)
        
        # Panel bawah: hasil dekripsi dan visualisasi
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        
        # Tab untuk hasil dan visualisasi
        result_tabs = QTabWidget()
        
        # Tab hasil teks
        text_tab = QWidget()
        text_layout = QVBoxLayout(text_tab)
        
        # Hasil dekripsi
        result_group = QGroupBox("Pesan Terdekripsi")
        result_group.setFont(QFont('Segoe UI', 10, QFont.Bold))
        result_layout = QVBoxLayout(result_group)
        
        self.decrypted_text = QTextEdit()
        self.decrypted_text.setReadOnly(True)
        self.decrypted_text.setFont(QFont('Segoe UI', 10))
        self.decrypted_text.setPlaceholderText("Hasil dekripsi akan ditampilkan di sini...")
        result_layout.addWidget(self.decrypted_text)
        
        text_layout.addWidget(result_group)
        
        result_tabs.addTab(text_tab, "Hasil Teks")
        
        # Tab visualisasi
        visual_tab = QWidget()
        visual_layout = QVBoxLayout(visual_tab)
        
        self.decrypt_figure = Figure(figsize=(5, 4), dpi=100)
        self.decrypt_canvas = FigureCanvas(self.decrypt_figure)
        visual_layout.addWidget(self.decrypt_canvas)
        
        result_tabs.addTab(visual_tab, "Spektrogram")
        
        # Tab debug
        debug_tab = QWidget()
        debug_layout = QVBoxLayout(debug_tab)
        
        self.debug_text = QTextEdit()
        self.debug_text.setReadOnly(True)
        self.debug_text.setFont(QFont('Courier New', 9))
        self.debug_text.setPlaceholderText("Informasi debug akan ditampilkan di sini...")
        debug_layout.addWidget(self.debug_text)
        
        result_tabs.addTab(debug_tab, "Debug Info")
        
        bottom_layout.addWidget(result_tabs)
        
        splitter.addWidget(bottom_widget)
        
        # Set proporsi splitter
        splitter.setSizes([400, 300])
        
        layout.addWidget(splitter)
    
    def setup_visual_tab(self, tab):
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Instruksi
        info_label = QLabel("Tab ini menyediakan alat visualisasi dan analisis lanjutan untuk audio terenkripsi.")
        info_label.setFont(QFont('Segoe UI', 10))
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Pilih file
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("File Audio:"))
        
        self.visual_file_path = QLineEdit()
        self.visual_file_path.setReadOnly(True)
        self.visual_file_path.setPlaceholderText("Pilih file audio untuk dianalisis...")
        file_layout.addWidget(self.visual_file_path)
        
        browse_visual_btn = QPushButton("Browse")
        browse_visual_btn.clicked.connect(self.browse_visual_file)
        file_layout.addWidget(browse_visual_btn)
        
        layout.addLayout(file_layout)
        
        # Pengaturan visualisasi
        settings_group = QGroupBox("Pengaturan Visualisasi")
        settings_group.setFont(QFont('Segoe UI', 10, QFont.Bold))
        settings_layout = QHBoxLayout(settings_group)
        
        # Jenis visualisasi
        type_layout = QVBoxLayout()
        type_layout.addWidget(QLabel("Jenis Visualisasi:"))
        
        self.visual_type = QComboBox()
        self.visual_type.addItem("Spektrogram")
        self.visual_type.addItem("Waveform")
        self.visual_type.addItem("Analisis Frekuensi")
        self.visual_type.addItem("3D Spektrogram")
        self.visual_type.addItem("Analisis Gabungan")
        self.visual_type.currentIndexChanged.connect(self.update_visualization)
        type_layout.addWidget(self.visual_type)
        settings_layout.addLayout(type_layout)
        
        # Resolusi
        resolution_layout = QVBoxLayout()
        resolution_layout.addWidget(QLabel("Resolusi:"))
        
        self.visual_resolution = QComboBox()
        self.visual_resolution.addItem("Rendah")
        self.visual_resolution.addItem("Sedang")
        self.visual_resolution.addItem("Tinggi")
        self.visual_resolution.addItem("Sangat Tinggi")
        self.visual_resolution.setCurrentIndex(1)  # Default: Sedang
        self.visual_resolution.currentIndexChanged.connect(self.update_visualization)
        resolution_layout.addWidget(self.visual_resolution)
        settings_layout.addLayout(resolution_layout)
        
        # Palet warna
        color_layout = QVBoxLayout()
        color_layout.addWidget(QLabel("Palet Warna:"))
        
        self.visual_colormap = QComboBox()
        self.visual_colormap.addItem("viridis")
        self.visual_colormap.addItem("plasma")
        self.visual_colormap.addItem("inferno")
        self.visual_colormap.addItem("magma")
        self.visual_colormap.addItem("cividis")
        self.visual_colormap.addItem("jet")
        self.visual_colormap.currentIndexChanged.connect(self.update_visualization)
        color_layout.addWidget(self.visual_colormap)
        settings_layout.addLayout(color_layout)
        
        # Rentang frekuensi
        freq_range_layout = QVBoxLayout()
        freq_range_layout.addWidget(QLabel("Rentang Frekuensi (Hz):"))
        
        freq_range_widget = QWidget()
        freq_range_inner = QHBoxLayout(freq_range_widget)
        freq_range_inner.setContentsMargins(0, 0, 0, 0)
        
        self.visual_freq_min = QSpinBox()
        self.visual_freq_min.setRange(0, 5000)
        self.visual_freq_min.setValue(0)
        self.visual_freq_min.setSingleStep(100)
        self.visual_freq_min.valueChanged.connect(self.update_visualization)
        freq_range_inner.addWidget(self.visual_freq_min)
        
        freq_range_inner.addWidget(QLabel("-"))
        
        self.visual_freq_max = QSpinBox()
        self.visual_freq_max.setRange(100, 10000)
        self.visual_freq_max.setValue(1000)
        self.visual_freq_max.setSingleStep(100)
        self.visual_freq_max.valueChanged.connect(self.update_visualization)
        freq_range_inner.addWidget(self.visual_freq_max)
        
        freq_range_layout.addWidget(freq_range_widget)
        settings_layout.addLayout(freq_range_layout)
        
        layout.addWidget(settings_group)
        
        # Tombol aksi
        buttons_layout = QHBoxLayout()
        
        analyze_btn = QPushButton("Analisis")
        if os.path.exists('resources/analyze.png'):
            analyze_btn.setIcon(QIcon('resources/analyze.png'))
        analyze_btn.clicked.connect(self.analyze_visual_file)
        buttons_layout.addWidget(analyze_btn)
        
        export_btn = QPushButton("Ekspor Gambar")
        if os.path.exists('resources/export.png'):
            export_btn.setIcon(QIcon('resources/export.png'))
        export_btn.clicked.connect(self.export_visualization)
        buttons_layout.addWidget(export_btn)
        
        reset_btn = QPushButton("Reset")
        if os.path.exists('resources/reset.png'):
            reset_btn.setIcon(QIcon('resources/reset.png'))
        reset_btn.clicked.connect(self.reset_visualization)
        buttons_layout.addWidget(reset_btn)
        
        layout.addLayout(buttons_layout)
        
        # Area visualisasi
        visual_group = QGroupBox("Visualisasi")
        visual_group.setFont(QFont('Segoe UI', 10, QFont.Bold))
        visual_layout = QVBoxLayout(visual_group)
        
        self.visual_figure = Figure(figsize=(8, 6), dpi=100)
        self.visual_canvas = FigureCanvas(self.visual_figure)
        visual_layout.addWidget(self.visual_canvas)
        
        layout.addWidget(visual_group)
        
        # Informasi analisis
        info_group = QGroupBox("Informasi Analisis")
        info_group.setFont(QFont('Segoe UI', 10, QFont.Bold))
        info_layout = QVBoxLayout(info_group)
        
        self.visual_info = QTextEdit()
        self.visual_info.setReadOnly(True)
        self.visual_info.setFont(QFont('Segoe UI', 9))
        self.visual_info.setMaximumHeight(100)
        info_layout.addWidget(self.visual_info)
        
        layout.addWidget(info_group)
    
    def setup_about_tab(self, tab):
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Splitter untuk membagi area info dan tools
        splitter = QSplitter(Qt.Vertical)
        splitter.setChildrenCollapsible(False)
        
        # Panel atas: informasi aplikasi
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        
        # Logo dan judul
        header_layout = QHBoxLayout()
        
        if os.path.exists("resources/logo_large.png"):
            logo_label = QLabel()
            logo_pixmap = QPixmap("resources/logo_large.png").scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(logo_pixmap)
            header_layout.addWidget(logo_label)
        
        title_layout = QVBoxLayout()
        title_label = QLabel("SonicCipher")
        title_label.setFont(QFont('Segoe UI', 24, QFont.Bold))
        title_layout.addWidget(title_label)
        
        version_label = QLabel("Versi 1.0.0")
        version_label.setFont(QFont('Segoe UI', 12))
        title_layout.addWidget(version_label)
        
        subtitle_label = QLabel("Aplikasi Kriptografi Teks ke Suara")
        subtitle_label.setFont(QFont('Segoe UI', 14))
        title_layout.addWidget(subtitle_label)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        top_layout.addLayout(header_layout)
        
        # Garis pemisah
        separator1 = create_separator()
        top_layout.addWidget(separator1)
        
        # Tentang aplikasi
        about_scroll = QTextEdit()
        about_scroll.setReadOnly(True)
        about_scroll.setFont(QFont('Segoe UI', 10))
        
        about_text = """
        <h2>Tentang SonicCipher</h2>
        <p>SonicCipher adalah aplikasi kriptografi inovatif yang dikembangkan untuk tugas mata kuliah Kriptografi. 
        Aplikasi ini mengubah pesan teks menjadi pola suara yang unik, menyediakan metode enkripsi yang kreatif 
        dan tidak konvensional.</p>
        
        <h3>Cara Kerja</h3>
        <p>SonicCipher menggunakan algoritma Frequency-Shift Audio Encryption (FSAE) yang menggabungkan konsep 
        enkripsi klasik dengan teknik pemrosesan sinyal digital:</p>
        <ol>
            <li>Setiap karakter dalam teks diubah menjadi nilai ASCII</li>
            <li>Nilai ASCII dimodifikasi menggunakan kunci enkripsi (shift)</li>
            <li>Nilai yang dimodifikasi dipetakan ke frekuensi audio tertentu</li>
            <li>Frekuensi-frekuensi ini dikombinasikan untuk membuat pola suara unik</li>
            <li>Durasi setiap nada bervariasi berdasarkan posisi karakter dalam pesan</li>
        </ol>
        
        <h3>Fitur Utama</h3>
        <ul>
            <li>Enkripsi teks menjadi audio dengan algoritma FSAE</li>
            <li>Dekripsi audio kembali menjadi teks</li>
            <li>Visualisasi spektrum audio dengan berbagai metode</li>
            <li>Penyesuaian parameter enkripsi (kunci, frekuensi, durasi)</li>
            <li>Analisis audio terenkripsi</li>
            <li>Antarmuka pengguna yang intuitif dan modern</li>
        </ul>
        
        <h3>Keamanan</h3>
        <p>FSAE menawarkan beberapa keuntungan keamanan:</p>
        <ul>
            <li><b>Obscurity by Medium</b>: Menggunakan suara sebagai medium membuat pesan tidak langsung terlihat seperti teks terenkripsi.</li>
            <li><b>Kunci Enkripsi</b>: Tanpa kunci yang benar, penerima tidak dapat mendekripsi pesan.</li>
            <li><b>Variasi Durasi</b>: Pola durasi yang bervariasi membuat analisis frekuensi lebih sulit.</li>
            <li><b>Metadata Terpisah</b>: Metadata disimpan dalam file terpisah, sehingga hanya orang yang memiliki akses ke kedua file yang dapat mendekripsi dengan mudah.</li>
        </ul>
        
        <h3>Pengembangan</h3>
        <p>Aplikasi ini dikembangkan menggunakan Python dengan pustaka-pustaka berikut:</p>
        <ul>
            <li>PyQt5 untuk antarmuka grafis</li>
            <li>NumPy dan SciPy untuk pemrosesan sinyal</li>
            <li>Matplotlib untuk visualisasi</li>
            <li>Pygame untuk pemutaran audio</li>
        </ul>
        """
        
        about_scroll.setHtml(about_text)
        top_layout.addWidget(about_scroll)
        
        splitter.addWidget(top_widget)
        
        # Panel bawah: tools dan bantuan
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        
        # Tabs untuk tools dan bantuan
        tools_tabs = QTabWidget()
        
        # Tab pengujian
        test_tab = QWidget()
        test_layout = QVBoxLayout(test_tab)
        
        test_label = QLabel("Pengujian Enkripsi-Dekripsi")
        test_label.setFont(QFont('Segoe UI', 12, QFont.Bold))
        test_layout.addWidget(test_label)
        
        test_desc = QLabel("Lakukan pengujian untuk memverifikasi bahwa enkripsi dan dekripsi berfungsi dengan benar.")
        test_desc.setWordWrap(True)
        test_layout.addWidget(test_desc)
        
        test_input_layout = QHBoxLayout()
        test_input_layout.addWidget(QLabel("Teks Pengujian:"))
        
        self.test_input = QLineEdit("Ini adalah tes enkripsi dan dekripsi!")
        test_input_layout.addWidget(self.test_input)
        
        test_input_layout.addWidget(QLabel("Kunci:"))
        
        self.test_key = QSpinBox()
        self.test_key.setRange(1, 25)
        self.test_key.setValue(7)
        test_input_layout.addWidget(self.test_key)
        
        test_layout.addLayout(test_input_layout)
        
        test_btn = QPushButton("Jalankan Pengujian")
        test_btn.clicked.connect(self.run_encryption_test)
        test_layout.addWidget(test_btn)
        
        self.test_result = QTextEdit()
        self.test_result.setReadOnly(True)
        self.test_result.setFont(QFont('Courier New', 10))
        self.test_result.setPlaceholderText("Hasil pengujian akan ditampilkan di sini...")
        test_layout.addWidget(self.test_result)
        
        tools_tabs.addTab(test_tab, "Pengujian")
        
        # Tab pemecahan masalah
        troubleshoot_tab = QWidget()
        troubleshoot_layout = QVBoxLayout(troubleshoot_tab)
        
        trouble_label = QLabel("Pemecahan Masalah")
        trouble_label.setFont(QFont('Segoe UI', 12, QFont.Bold))
        troubleshoot_layout.addWidget(trouble_label)
        
        trouble_scroll = QTextEdit()
        trouble_scroll.setReadOnly(True)
        trouble_scroll.setFont(QFont('Segoe UI', 10))
        
        trouble_text = """
        <h3>Masalah Umum dan Solusinya</h3>
        
        <h4>1. "File metadata tidak ditemukan. Dekripsi mungkin kurang akurat."</h4>
        <p><b>Penyebab:</b> Aplikasi tidak dapat menemukan file metadata yang seharusnya disimpan bersamaan dengan file audio.</p>
        <p><b>Solusi:</b></p>
        <ul>
            <li>Pastikan file metadata (.wav.metadata) berada di lokasi yang sama dengan file audio.</li>
            <li>Coba simpan ulang file audio terenkripsi.</li>
            <li>Gunakan metode dekripsi "Analisis Audio" jika metadata tidak tersedia.</li>
            <li>Sesuaikan parameter dekripsi manual (frekuensi dasar, toleransi) jika menggunakan analisis audio.</li>
        </ul>
        
        <h4>2. Dekripsi tidak akurat atau menghasilkan karakter yang salah</h4>
        <p><b>Penyebab:</b> Parameter dekripsi tidak sesuai dengan parameter yang digunakan saat enkripsi.</p>
        <p><b>Solusi:</b></p>
        <ul>
            <li>Pastikan menggunakan kunci dekripsi yang sama dengan kunci enkripsi.</li>
            <li>Sesuaikan toleransi frekuensi (coba nilai antara 5-10%).</li>
            <li>Jika tidak menggunakan metadata, pastikan frekuensi dasar yang dimasukkan sama dengan yang digunakan saat enkripsi.</li>
            <li>Coba berbagai kombinasi parameter hingga mendapatkan hasil yang benar.</li>
        </ul>
        
        <h4>3. Audio tidak terdengar atau terputus-putus</h4>
        <p><b>Penyebab:</b> Masalah dengan pemutaran audio atau pengaturan sistem.</p>
        <p><b>Solusi:</b></p>
        <ul>
            <li>Pastikan perangkat audio (speaker/headphone) terhubung dan berfungsi.</li>
            <li>Periksa volume sistem dan aplikasi.</li>
            <li>Coba simpan audio dan putar dengan aplikasi lain.</li>
            <li>Restart aplikasi jika masalah berlanjut.</li>
        </ul>
        
        <h4>4. Aplikasi lambat atau tidak responsif</h4>
        <p><b>Penyebab:</b> Proses enkripsi/dekripsi yang berat atau visualisasi yang kompleks.</p>
        <p><b>Solusi:</b></p>
        <ul>
            <li>Kurangi panjang teks yang dienkripsi.</li>
            <li>Gunakan resolusi visualisasi yang lebih rendah.</li>
            <li>Tutup aplikasi lain yang berjalan di latar belakang.</li>
            <li>Restart aplikasi jika masalah berlanjut.</li>
        </ul>
        """
        
        trouble_scroll.setHtml(trouble_text)
        troubleshoot_layout.addWidget(trouble_scroll)
        
        tools_tabs.addTab(troubleshoot_tab, "Pemecahan Masalah")
        
        # Tab bantuan
        help_tab = QWidget()
        help_layout = QVBoxLayout(help_tab)
        
        help_label = QLabel("Bantuan Penggunaan")
        help_label.setFont(QFont('Segoe UI', 12, QFont.Bold))
        help_layout.addWidget(help_label)
        
        help_scroll = QTextEdit()
        help_scroll.setReadOnly(True)
        help_scroll.setFont(QFont('Segoe UI', 10))
        
        help_text = """
        <h3>Panduan Penggunaan SonicCipher</h3>
        
        <h4>Enkripsi Pesan</h4>
        <ol>
            <li>Buka tab "Enkripsi"</li>
            <li>Masukkan pesan yang ingin dienkripsi dalam kotak teks</li>
            <li>Sesuaikan pengaturan enkripsi:
                <ul>
                    <li>Kunci Enkripsi (1-25): Nilai yang digunakan untuk menggeser karakter</li>
                    <li>Frekuensi Dasar (Hz): Frekuensi awal untuk pemetaan karakter</li>
                    <li>Durasi Dasar (ms): Durasi dasar untuk setiap nada</li>
                    <li>Algoritma: Pilih algoritma enkripsi yang diinginkan</li>
                </ul>
            </li>
            <li>Klik tombol "Enkripsi ke Suara"</li>
            <li>Lihat visualisasi audio yang dihasilkan</li>
            <li>Gunakan tombol "Putar Suara" untuk mendengarkan hasil enkripsi</li>
            <li>Gunakan tombol "Simpan Suara" untuk menyimpan file audio terenkripsi</li>
        </ol>
        
        <h4>Dekripsi Pesan</h4>
        <ol>
            <li>Buka tab "Dekripsi"</li>
            <li>Klik tombol "Pilih File" atau seret file audio terenkripsi ke area yang disediakan</li>
            <li>Sesuaikan pengaturan dekripsi:
                <ul>
                    <li>Kunci Dekripsi: Harus sama dengan kunci yang digunakan saat enkripsi</li>
                    <li>Toleransi Frekuensi: Sesuaikan jika dekripsi tidak akurat</li>
                    <li>Metode Dekripsi: Pilih metode yang sesuai</li>
                    <li>Frekuensi Dasar: Diperlukan jika tidak menggunakan metadata</li>
                </ul>
            </li>
            <li>Klik tombol "Putar Audio Terenkripsi" untuk mendengarkan audio</li>
            <li>Klik tombol "Dekripsi Suara" untuk mendekripsi pesan</li>
            <li>Lihat hasil dekripsi di kotak teks "Pesan Terdekripsi"</li>
            <li>Gunakan tombol "Salin Hasil" untuk menyalin hasil ke clipboard</li>
        </ol>
        
        <h4>Visualisasi Audio</h4>
        <ol>
            <li>Buka tab "Visualisasi"</li>
            <li>Pilih file audio untuk dianalisis</li>
            <li>Sesuaikan pengaturan visualisasi sesuai kebutuhan</li>
            <li>Klik tombol "Analisis" untuk menghasilkan visualisasi</li>
            <li>Gunakan tombol "Ekspor Gambar" untuk menyimpan visualisasi sebagai gambar</li>
        </ol>
        """
        
        help_scroll.setHtml(help_text)
        help_layout.addWidget(help_scroll)
        
        tools_tabs.addTab(help_tab, "Bantuan")
        
        bottom_layout.addWidget(tools_tabs)
        
        splitter.addWidget(bottom_widget)
        
        # Set proporsi splitter
        splitter.setSizes([500, 200])
        
        layout.addWidget(splitter)
    
    # ===== Fungsi-fungsi untuk Tab Enkripsi =====
    
    def update_char_count(self):
        """Update penghitung karakter pada input teks"""
        count = len(self.plaintext_input.toPlainText())
        self.char_count_label.setText(f"Karakter: {count}")
    
    def encrypt_message(self):
        """Enkripsi pesan teks menjadi audio"""
        plaintext = self.plaintext_input.toPlainText()
        if not plaintext:
            QMessageBox.warning(self, "Input Kosong", "Silakan masukkan pesan untuk dienkripsi!")
            return
        
        key = self.encrypt_key.value()
        base_freq = self.base_freq.value()
        base_duration = self.base_duration.value() / 1000.0  # Convert to seconds
        algorithm = self.algorithm_combo.currentText()
        
        # Tampilkan progress bar
        self.encrypt_progress.setValue(0)
        self.encrypt_progress.setVisible(True)
        self.encrypt_btn.setEnabled(False)
        self.statusBar().showMessage("Memproses enkripsi...")
        
        # Jalankan enkripsi dalam thread terpisah
        self.encrypt_thread = EncryptionThread(
            self.audio_processor, plaintext, key, base_freq, base_duration
        )
        self.encrypt_thread.progress.connect(self.update_encrypt_progress)
        self.encrypt_thread.finished.connect(self.handle_encryption_finished)
        self.encrypt_thread.error.connect(self.handle_encryption_error)
        self.encrypt_thread.start()
    
    def update_encrypt_progress(self, value):
        """Update progress bar enkripsi"""
        self.encrypt_progress.setValue(value)
    
    def handle_encryption_finished(self, result):
        """Menangani hasil enkripsi yang berhasil"""
        self.encrypted_data = result
        plaintext = self.plaintext_input.toPlainText()
        
        # Visualisasi
        self.visualizer.plot_spectrogram(
            self.encrypted_data['audio'], 
            self.encrypted_data['sample_rate'], 
            self.encrypt_figure,
            colormap=self.visual_colormap.currentText() if hasattr(self, 'visual_colormap') else 'viridis'
        )
        self.encrypt_canvas.draw()
        
        self.visualizer.plot_waveform(
            self.encrypted_data['audio'], 
            self.encrypted_data['sample_rate'], 
            self.encrypt_wave_figure
        )
        self.encrypt_wave_canvas.draw()
        
        self.visualizer.plot_frequency_analysis(
            self.encrypted_data['audio'], 
            self.encrypted_data['sample_rate'], 
            self.encrypt_freq_figure
        )
        self.encrypt_freq_canvas.draw()
        
        # Aktifkan tombol
        self.play_btn.setEnabled(True)
        self.save_btn.setEnabled(True)
        self.encrypt_btn.setEnabled(True)
        
        # Sembunyikan progress bar
        self.encrypt_progress.setVisible(False)
        
        # Update status
        self.statusBar().showMessage(f"Enkripsi berhasil! {len(plaintext)} karakter dienkripsi.", 5000)
        
        QMessageBox.information(self, "Sukses", "Pesan berhasil dienkripsi!")
    
    def handle_encryption_error(self, error_msg):
        """Menangani error pada proses enkripsi"""
        self.encrypt_btn.setEnabled(True)
        self.encrypt_progress.setVisible(False)
        self.statusBar().showMessage("Enkripsi gagal!", 5000)
        
        QMessageBox.critical(self, "Error", f"Terjadi kesalahan saat enkripsi: {error_msg}")
        
    def play_encrypted_sound(self):
        """Memutar suara hasil enkripsi"""
        if self.encrypted_data:
            self.statusBar().showMessage("Memutar audio terenkripsi...", 3000)
            self.audio_processor.play_audio(self.encrypted_data['audio'], self.encrypted_data['sample_rate'])
    
    def save_encrypted_sound(self):
        """Menyimpan suara hasil enkripsi ke file"""
        if not self.encrypted_data:
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Simpan Audio Terenkripsi", "", "WAV Files (*.wav);;All Files (*)"
        )
        
        if file_path:
            try:
                self.statusBar().showMessage(f"Menyimpan audio ke {file_path}...", 3000)
                
                # Simpan audio dan metadata
                self.audio_processor.save_audio(
                    file_path, 
                    self.encrypted_data['audio'], 
                    self.encrypted_data['sample_rate'],
                    self.encrypted_data['metadata']
                )
                
                # Tampilkan pesan sukses dengan detail path
                success_msg = f"File audio berhasil disimpan ke:\n{file_path}\n\nFile metadata disimpan ke:\n{file_path}.metadata"
                QMessageBox.information(self, "Sukses", success_msg)
                
                self.statusBar().showMessage(f"Audio berhasil disimpan ke {file_path}", 5000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Gagal menyimpan file: {str(e)}")
                self.statusBar().showMessage("Gagal menyimpan audio", 5000)
    
    # ===== Fungsi-fungsi untuk Tab Dekripsi =====
    
    def browse_audio_file(self):
        """Memilih file audio untuk didekripsi"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Pilih File Audio Terenkripsi", "", "WAV Files (*.wav);;All Files (*)"
        )
        
        if file_path:
            self.load_audio_file(file_path)
    
    def load_audio_file(self, file_path):
        """Memuat file audio untuk didekripsi"""
        self.audio_file_path = file_path
        self.file_path_display.setText(file_path)
        
        # Periksa apakah file metadata ada
        metadata_file = file_path + ".metadata"
        if os.path.exists(metadata_file):
            self.metadata_status.setText("Status Metadata: ✅ Ditemukan")
            self.metadata_status.setStyleSheet("color: green;")
            self.debug_text.append(f"File metadata ditemukan: {metadata_file}")
        else:
            self.metadata_status.setText("Status Metadata: ❌ Tidak ditemukan")
            self.metadata_status.setStyleSheet("color: red;")
            self.debug_text.append(f"File metadata tidak ditemukan: {metadata_file}")
            self.debug_text.append("Dekripsi akan menggunakan analisis audio langsung yang mungkin kurang akurat.")
        
        try:
            # Load audio dan visualisasi
            audio_data, sample_rate, metadata = self.audio_processor.load_audio(file_path)
            
            self.visualizer.plot_spectrogram(audio_data, sample_rate, self.decrypt_figure)
            self.decrypt_canvas.draw()
            
            # Tampilkan informasi audio
            self.debug_text.clear()
            self.debug_text.append(f"File audio dimuat: {file_path}")
            self.debug_text.append(f"Sample rate: {sample_rate} Hz")
            self.debug_text.append(f"Durasi: {len(audio_data)/sample_rate:.2f} detik")
            self.debug_text.append(f"Jumlah sampel: {len(audio_data)}")
            
            if metadata:
                self.debug_text.append("\nInformasi Metadata:")
                for key, value in metadata.items():
                    if key not in ['frequencies', 'durations', 'original_chars', 'shifted_chars']:
                        self.debug_text.append(f"- {key}: {value}")
                
                if 'frequencies' in metadata:
                    self.debug_text.append(f"- Jumlah karakter: {len(metadata['frequencies'])}")
                    self.debug_text.append(f"- Frekuensi (5 pertama): {[f'{f:.1f}' for f in metadata['frequencies'][:5]]}")
            
            # Aktifkan tombol
            self.play_encrypted_btn.setEnabled(True)
            self.decrypt_btn.setEnabled(True)
            
            self.statusBar().showMessage(f"File audio dimuat: {os.path.basename(file_path)}", 5000)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal memuat file audio: {str(e)}")
            self.debug_text.append(f"ERROR: {str(e)}")
            self.statusBar().showMessage("Gagal memuat file audio", 5000)
    
    def play_loaded_audio(self):
        """Memutar file audio yang telah dimuat"""
        if self.audio_file_path:
            self.statusBar().showMessage("Memutar audio...", 3000)
            audio_data, sample_rate, _ = self.audio_processor.load_audio(self.audio_file_path)
            self.audio_processor.play_audio(audio_data, sample_rate)
    
    def decrypt_audio(self):
        """Mendekripsi file audio yang telah dimuat"""
        if not self.audio_file_path:
            return
            
        key = self.decrypt_key.value()
        tolerance = self.freq_tolerance.value() / 100.0  # Convert to decimal
        
        # Tampilkan progress bar
        self.decrypt_progress.setValue(0)
        self.decrypt_progress.setVisible(True)
        self.decrypt_btn.setEnabled(False)
        self.statusBar().showMessage("Memproses dekripsi...")
        
        try:
            # Load audio
            audio_data, sample_rate, metadata = self.audio_processor.load_audio(self.audio_file_path)
            
            if metadata is None and self.decrypt_method.currentText() == "Gunakan Metadata":
                QMessageBox.warning(self, "Peringatan", 
                    "File metadata tidak ditemukan tetapi metode 'Gunakan Metadata' dipilih.\nSilakan pilih metode lain atau gunakan file dengan metadata.")
                self.decrypt_progress.setVisible(False)
                self.decrypt_btn.setEnabled(True)
                return
            
            # Jika metode analisis audio dipilih, gunakan parameter manual
            if self.decrypt_method.currentText() == "Analisis Audio" or (metadata is None and self.decrypt_method.currentText() == "Otomatis (Metadata jika tersedia)"):
                metadata = {
                    'base_freq': self.decrypt_base_freq.value(),
                    'freq_range': 660  # Default
                }
                self.debug_text.append("\nMenggunakan parameter manual:")
                self.debug_text.append(f"- Frekuensi dasar: {metadata['base_freq']} Hz")
                self.debug_text.append(f"- Rentang frekuensi: {metadata['freq_range']} Hz")
            
            # Jalankan dekripsi dalam thread terpisah
            self.decrypt_thread = DecryptionThread(
                self.audio_processor, audio_data, sample_rate, key, tolerance, metadata
            )
            self.decrypt_thread.progress.connect(self.update_decrypt_progress)
            self.decrypt_thread.finished.connect(self.handle_decryption_finished)
            self.decrypt_thread.error.connect(self.handle_decryption_error)
            self.decrypt_thread.start()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan saat dekripsi: {str(e)}")
            self.decrypt_progress.setVisible(False)
            self.decrypt_btn.setEnabled(True)
            self.debug_text.append(f"ERROR: {str(e)}")
            self.statusBar().showMessage("Dekripsi gagal!", 5000)
    
    def update_decrypt_progress(self, value):
        """Update progress bar dekripsi"""
        self.decrypt_progress.setValue(value)
    
    def handle_decryption_finished(self, result):
        """Menangani hasil dekripsi yang berhasil"""
        # Tampilkan hasil
        self.decrypted_text.setText(result)
        
        # Aktifkan tombol
        self.decrypt_btn.setEnabled(True)
        self.copy_result_btn.setEnabled(True)
        
        # Sembunyikan progress bar
        self.decrypt_progress.setVisible(False)
        
        # Update debug info
        self.debug_text.append("\nDekripsi selesai!")
        self.debug_text.append(f"Jumlah karakter hasil: {len(result)}")
        
        # Update status
        self.statusBar().showMessage("Dekripsi berhasil!", 5000)
    
    def handle_decryption_error(self, error_msg):
        """Menangani error pada proses dekripsi"""
        self.decrypt_btn.setEnabled(True)
        self.decrypt_progress.setVisible(False)
        self.statusBar().showMessage("Dekripsi gagal!", 5000)
        
        self.debug_text.append(f"ERROR: {error_msg}")
        QMessageBox.critical(self, "Error", f"Terjadi kesalahan saat dekripsi: {error_msg}")
    
    def copy_decrypted_text(self):
        """Menyalin hasil dekripsi ke clipboard"""
        text = self.decrypted_text.toPlainText()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            self.statusBar().showMessage("Teks berhasil disalin ke clipboard!", 3000)
    
    # ===== Fungsi-fungsi untuk Tab Visualisasi =====
    
    def browse_visual_file(self):
        """Memilih file audio untuk visualisasi"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Pilih File Audio", "", "WAV Files (*.wav);;All Files (*)"
        )
        
        if file_path:
            self.visual_file_path.setText(file_path)
            self.analyze_visual_file()
    
    def analyze_visual_file(self):
        """Menganalisis file audio untuk visualisasi"""
        file_path = self.visual_file_path.text()
        if not file_path or not os.path.exists(file_path):
            QMessageBox.warning(self, "File Tidak Ditemukan", "Silakan pilih file audio terlebih dahulu.")
            return
        
        try:
            # Load audio
            audio_data, sample_rate, metadata = self.audio_processor.load_audio(file_path)
            
            # Update visualisasi
            self.update_visualization(audio_data=audio_data, sample_rate=sample_rate)
            
            # Tampilkan informasi audio
            self.visual_info.clear()
            self.visual_info.append(f"File: {os.path.basename(file_path)}")
            self.visual_info.append(f"Sample rate: {sample_rate} Hz")
            self.visual_info.append(f"Durasi: {len(audio_data)/sample_rate:.2f} detik")
            
            if metadata:
                self.visual_info.append(f"Karakter terenkripsi: {metadata.get('char_count', 'Tidak diketahui')}")
                self.visual_info.append(f"Algoritma: {metadata.get('algorithm', 'Tidak diketahui')}")
            
            self.statusBar().showMessage(f"Analisis selesai: {os.path.basename(file_path)}", 5000)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal menganalisis file: {str(e)}")
            self.statusBar().showMessage("Analisis gagal", 5000)
    
    def update_visualization(self, index=None, audio_data=None, sample_rate=None):
        """Update visualisasi berdasarkan pengaturan yang dipilih"""
        if audio_data is None or sample_rate is None:
            # Jika tidak ada data audio yang diberikan, coba muat dari file
            file_path = self.visual_file_path.text()
            if not file_path or not os.path.exists(file_path):
                return
                
            try:
                audio_data, sample_rate, _ = self.audio_processor.load_audio(file_path)
            except:
                return
        
        # Dapatkan pengaturan visualisasi
        visual_type = self.visual_type.currentText()
        colormap = self.visual_colormap.currentText()
        freq_min = self.visual_freq_min.value()
        freq_max = self.visual_freq_max.value()
        
        # Resolusi berdasarkan pilihan
        resolution_map = {
            "Rendah": 512,
            "Sedang": 1024,
            "Tinggi": 2048,
            "Sangat Tinggi": 4096
        }
        resolution = resolution_map[self.visual_resolution.currentText()]
        
        # Bersihkan figure
        self.visual_figure.clear()
        
        # Buat visualisasi berdasarkan jenis yang dipilih
        if visual_type == "Spektrogram":
            self.visualizer.plot_spectrogram(
                audio_data, sample_rate, self.visual_figure,
                colormap=colormap, freq_range=(freq_min, freq_max),
                resolution=resolution
            )
        elif visual_type == "Waveform":
            self.visualizer.plot_waveform(
                audio_data, sample_rate, self.visual_figure
            )
        elif visual_type == "Analisis Frekuensi":
            self.visualizer.plot_frequency_analysis(
                audio_data, sample_rate, self.visual_figure,
                freq_range=(freq_min, freq_max)
            )
        elif visual_type == "3D Spektrogram":
            self.visualizer.plot_3d_spectrogram(
                audio_data, sample_rate, self.visual_figure,
                colormap=colormap, freq_range=(freq_min, freq_max),
                resolution=resolution
            )
        elif visual_type == "Analisis Gabungan":
            self.visualizer.plot_combined_analysis(
                audio_data, sample_rate, self.visual_figure,
                colormap=colormap, freq_range=(freq_min, freq_max)
            )
        
        # Refresh canvas
        self.visual_canvas.draw()
    
    def export_visualization(self):
        """Ekspor visualisasi saat ini sebagai gambar"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Simpan Visualisasi", "", "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)"
        )
        
        if file_path:
            try:
                self.visual_figure.savefig(file_path, dpi=300, bbox_inches='tight')
                QMessageBox.information(self, "Sukses", f"Visualisasi berhasil disimpan ke:\n{file_path}")
                self.statusBar().showMessage(f"Visualisasi disimpan ke {file_path}", 5000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Gagal menyimpan visualisasi: {str(e)}")
    
    def reset_visualization(self):
        """Reset pengaturan visualisasi ke default"""
        self.visual_type.setCurrentIndex(0)
        self.visual_resolution.setCurrentIndex(1)
        self.visual_colormap.setCurrentIndex(0)
        self.visual_freq_min.setValue(0)
        self.visual_freq_max.setValue(1000)
        
        # Clear figure
        self.visual_figure.clear()
        self.visual_canvas.draw()
        
        # Clear info
        self.visual_info.clear()
        
        self.statusBar().showMessage("Pengaturan visualisasi direset", 3000)
    
    # ===== Fungsi-fungsi Umum =====
    
    def run_encryption_test(self):
        """Menjalankan tes enkripsi-dekripsi sederhana"""
        test_text = self.test_input.text() if hasattr(self, 'test_input') else "Ini adalah tes enkripsi dan dekripsi!"
        test_key = self.test_key.value() if hasattr(self, 'test_key') else 7
        
        if not test_text:
            QMessageBox.warning(self, "Input Kosong", "Silakan masukkan teks untuk pengujian!")
            return
        
        self.statusBar().showMessage("Menjalankan pengujian enkripsi-dekripsi...", 3000)
        
        try:
            # Tampilkan informasi pengujian
            if hasattr(self, 'test_result'):
                self.test_result.clear()
                self.test_result.append(f"Teks asli: '{test_text}'")
                self.test_result.append(f"Kunci: {test_key}")
                self.test_result.append("\nMemulai pengujian...")
            
            # Enkripsi
            encrypted_data = self.audio_processor.encrypt_to_audio(test_text, test_key)
            
            if hasattr(self, 'test_result'):
                self.test_result.append("\nEnkripsi berhasil!")
                self.test_result.append(f"Jumlah karakter: {len(test_text)}")
                self.test_result.append(f"Jumlah frekuensi: {len(encrypted_data['metadata']['frequencies'])}")
                self.test_result.append(f"Frekuensi (5 pertama): {[f'{f:.1f}' for f in encrypted_data['metadata']['frequencies'][:5]]}...")
            
            # Dekripsi langsung dari metadata
            decrypted_text = self.audio_processor.decrypt_from_audio(
                encrypted_data['audio'],
                encrypted_data['sample_rate'],
                test_key,
                0.05,
                encrypted_data['metadata']
            )
            
            if hasattr(self, 'test_result'):
                self.test_result.append("\nDekripsi berhasil!")
                self.test_result.append(f"Teks terdekripsi: '{decrypted_text}'")
            
            # Verifikasi
            if test_text == decrypted_text:
                if hasattr(self, 'test_result'):
                    self.test_result.append("\n✅ SUKSES: Teks asli dan teks terdekripsi sama!")
                
                QMessageBox.information(self, "Hasil Pengujian", 
                    "Pengujian BERHASIL!\nEnkripsi dan dekripsi berfungsi dengan benar.")
                self.statusBar().showMessage("Pengujian berhasil!", 5000)
            else:
                if hasattr(self, 'test_result'):
                    self.test_result.append("\n❌ GAGAL: Teks asli dan teks terdekripsi berbeda!")
                    self.test_result.append("\nAnalisis perbedaan:")
                    
                    for i, (orig, decrypted) in enumerate(zip(test_text, decrypted_text)):
                        if orig != decrypted:
                            self.test_result.append(f"  Indeks {i}: Asli='{orig}' ({ord(orig)}) vs Dekripsi='{decrypted}' ({ord(decrypted)})")
                
                QMessageBox.warning(self, "Hasil Pengujian", 
                    "Pengujian GAGAL!\nAda perbedaan antara teks asli dan hasil dekripsi.")
                self.statusBar().showMessage("Pengujian gagal", 5000)
            
            return test_text == decrypted_text
            
        except Exception as e:
            if hasattr(self, 'test_result'):
                self.test_result.append(f"\n❌ ERROR: {str(e)}")
            
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan saat pengujian: {str(e)}")
            self.statusBar().showMessage("Pengujian gagal karena error", 5000)
            return False
    
    def clear_inputs(self):
        """Membersihkan semua input"""
        if self.tab_widget.currentIndex() == 0:  # Tab Enkripsi
            self.plaintext_input.clear()
        elif self.tab_widget.currentIndex() == 1:  # Tab Dekripsi
            self.file_path_display.clear()
            self.decrypted_text.clear()
            self.debug_text.clear()
            self.audio_file_path = None
            self.metadata_status.setText("Status Metadata: Belum diperiksa")
            self.metadata_status.setStyleSheet("")
            self.play_encrypted_btn.setEnabled(False)
            self.decrypt_btn.setEnabled(False)
            self.copy_result_btn.setEnabled(False)
            
            # Clear figure
            self.decrypt_figure.clear()
            self.decrypt_canvas.draw()
    
    def show_preferences(self):
        """Menampilkan dialog preferensi"""
        # Implementasi sederhana, bisa dikembangkan lebih lanjut
        QMessageBox.information(self, "Preferensi", 
            "Fitur preferensi akan ditambahkan di versi mendatang.")
    
    def analyze_audio(self):
        """Menampilkan analisis audio lanjutan"""
        # Pindah ke tab visualisasi
        self.tab_widget.setCurrentIndex(2)  # Tab Visualisasi
        
        # Jika sudah ada file yang dimuat di tab dekripsi, gunakan file tersebut
        if hasattr(self, 'audio_file_path') and self.audio_file_path:
            self.visual_file_path.setText(self.audio_file_path)
            self.analyze_visual_file()
    
    def show_help(self):
        """Menampilkan bantuan penggunaan"""
        # Pindah ke tab bantuan
        self.tab_widget.setCurrentIndex(3)  # Tab Tentang
        
        # Pilih tab bantuan
        if hasattr(self, 'tools_tabs'):
            self.tools_tabs.setCurrentIndex(2)  # Tab Bantuan
    
    def show_about_dialog(self):
        """Menampilkan dialog tentang aplikasi"""
        about_text = """
        <h2>SonicCipher v1.0.0</h2>
        <p>Aplikasi Kriptografi Teks ke Suara</p>
        <p>Dikembangkan untuk Tugas Mata Kuliah Kriptografi</p>
        <br>
        <p>SonicCipher menggunakan algoritma Frequency-Shift Audio Encryption (FSAE) 
        untuk mengenkripsi pesan teks menjadi pola suara yang unik.</p>
        <br>
        <p>© 2025 SonicCipher</p>
        """
        
        QMessageBox.about(self, "Tentang SonicCipher", about_text)
    
    def quick_encrypt(self):
        """Fungsi cepat untuk enkripsi dari toolbar"""
        self.tab_widget.setCurrentIndex(0)  # Tab Enkripsi
        if self.plaintext_input.toPlainText():
            self.encrypt_message()
    
    def quick_decrypt(self):
        """Fungsi cepat untuk dekripsi dari toolbar"""
        self.tab_widget.setCurrentIndex(1)  # Tab Dekripsi
        if self.audio_file_path:
            self.decrypt_audio()
        else:
            self.browse_audio_file()
    
    def play_current_audio(self):
        """Memutar audio saat ini berdasarkan tab aktif"""
        current_tab = self.tab_widget.currentIndex()
        
        if current_tab == 0 and hasattr(self, 'encrypted_data') and self.encrypted_data:  # Tab Enkripsi
            self.play_encrypted_sound()
        elif current_tab == 1 and hasattr(self, 'audio_file_path') and self.audio_file_path:  # Tab Dekripsi
            self.play_loaded_audio()
    
    def stop_audio(self):
        """Menghentikan pemutaran audio"""
        self.audio_processor.stop_audio()
        self.statusBar().showMessage("Pemutaran audio dihentikan", 3000)
