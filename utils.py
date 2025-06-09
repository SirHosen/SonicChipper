#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SonicCipher - Aplikasi Kriptografi Teks ke Suara
Utils - Fungsi-fungsi utilitas
"""

import os
from PyQt5.QtWidgets import QPushButton, QFrame, QSizePolicy, QApplication
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QColor
from PyQt5.QtCore import Qt, QSize

def create_icon_button(text, icon_path, callback, tooltip=None):
    """
    Membuat tombol dengan ikon
    """
    button = QPushButton(text)
    if os.path.exists(icon_path):
        button.setIcon(QIcon(icon_path))
    button.clicked.connect(callback)
    if tooltip:
        button.setToolTip(tooltip)
    return button

def create_separator():
    """
    Membuat garis pemisah horizontal
    """
    separator = QFrame()
    separator.setFrameShape(QFrame.HLine)
    separator.setFrameShadow(QFrame.Sunken)
    return separator

def set_dark_theme(window):
    """
    Menerapkan tema gelap ke aplikasi
    """
    # Dapatkan instance aplikasi
    app = QApplication.instance()
    
    # Buat palette gelap
    dark_palette = QPalette()
    
    # Warna dasar
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.Active, QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.WindowText, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.Light, QColor(53, 53, 53))
    
    # Terapkan palette
    app.setPalette(dark_palette)
    
    # Style sheet tambahan untuk komponen tertentu
    app.setStyleSheet("""
        QToolTip { 
            color: #ffffff; 
            background-color: #2a82da; 
            border: 1px solid white; 
        }
        
        QGroupBox {
            border: 1px solid #3a3a3a;
            border-radius: 5px;
            margin-top: 1em;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px 0 3px;
        }
        
        QTabWidget::pane {
            border: 1px solid #3a3a3a;
            border-radius: 3px;
        }
        
        QTabBar::tab {
            background: #3a3a3a;
            border: 1px solid #2a2a2a;
            border-bottom-color: #3a3a3a;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            min-width: 8ex;
            padding: 5px;
        }
        
        QTabBar::tab:selected, QTabBar::tab:hover {
            background: #4a4a4a;
        }
        
        QTabBar::tab:selected {
            border-color: #2a82da;
            border-bottom-color: #4a4a4a;
        }
        
        QProgressBar {
            border: 1px solid #3a3a3a;
            border-radius: 3px;
            text-align: center;
        }
        
        QProgressBar::chunk {
            background-color: #2a82da;
            width: 10px;
        }
    """)
