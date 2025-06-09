#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SonicCipher - Aplikasi Kriptografi Teks ke Suara
Visualizer - Visualisasi audio
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from scipy import signal
from mpl_toolkits.mplot3d import Axes3D

class AudioVisualizer:
    def __init__(self):
        pass
    
    def plot_waveform(self, audio_data, sample_rate, figure):
        """
        Menggambar bentuk gelombang audio
        """
        figure.clear()
        ax = figure.add_subplot(111)
        
        # Buat array waktu
        time = np.arange(0, len(audio_data)) / sample_rate
        
        # Plot waveform
        ax.plot(time, audio_data, color='#3498db')
        ax.set_xlabel('Waktu (detik)')
        ax.set_ylabel('Amplitudo')
        ax.set_title('Bentuk Gelombang Audio')
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Set batas y
        ax.set_ylim(-1.1, 1.1)
        
        # Tambahkan info durasi
        duration = len(audio_data) / sample_rate
        ax.text(0.02, 0.95, f"Durasi: {duration:.2f} detik", transform=ax.transAxes, 
                bbox=dict(facecolor='white', alpha=0.8))
        
        figure.tight_layout()
    
    def plot_spectrogram(self, audio_data, sample_rate, figure, colormap='viridis', freq_range=(0, 1000), resolution=1024):
        """
        Menggambar spektrogram audio
        """
        figure.clear()
        ax = figure.add_subplot(111)
        
        # Buat spektrogram
        f, t, Sxx = signal.spectrogram(audio_data, fs=sample_rate, nperseg=resolution)
        
        # Plot spektrogram
        pcm = ax.pcolormesh(t, f, 10 * np.log10(Sxx + 1e-10), shading='gouraud', cmap=colormap)
        ax.set_ylabel('Frekuensi (Hz)')
        ax.set_xlabel('Waktu (detik)')
        ax.set_title('Spektrogram Audio')
        
        # Set batas frekuensi
        ax.set_ylim(freq_range)
        
        # Tambahkan colorbar
        cbar = figure.colorbar(pcm, ax=ax, label='Intensitas (dB)')
        
        # Tambahkan info
        duration = len(audio_data) / sample_rate
        info_text = f"Durasi: {duration:.2f} detik\n"
        info_text += f"Sample rate: {sample_rate} Hz\n"
        info_text += f"Resolusi: {resolution} points"
        
        ax.text(0.02, 0.95, info_text, transform=ax.transAxes, 
                bbox=dict(facecolor='white', alpha=0.8), fontsize=8)
        
        figure.tight_layout()
    
    def plot_frequency_analysis(self, audio_data, sample_rate, figure, freq_range=(0, 1000)):
        """
        Menggambar analisis frekuensi (FFT)
        """
        figure.clear()
        ax = figure.add_subplot(111)
        
        # Hitung FFT
        n = len(audio_data)
        fft_data = np.abs(np.fft.rfft(audio_data))
        freqs = np.fft.rfftfreq(n, d=1/sample_rate)
        
        # Normalisasi
        fft_data = fft_data / np.max(fft_data)
        
        # Plot FFT
        ax.plot(freqs, fft_data, color='#2ecc71')
        ax.set_xlabel('Frekuensi (Hz)')
        ax.set_ylabel('Magnitude (normalisasi)')
        ax.set_title('Analisis Frekuensi')
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Batasi tampilan frekuensi
        ax.set_xlim(freq_range)
        
        # Cari frekuensi dominan
        dominant_freqs = []
        for i in range(5):  # Cari 5 frekuensi dominan
            if len(fft_data) > 0:
                idx = np.argmax(fft_data)
                if freqs[idx] >= freq_range[0] and freqs[idx] <= freq_range[1]:
                    dominant_freqs.append((freqs[idx], fft_data[idx]))
                fft_data[max(0, idx-5):min(len(fft_data), idx+5)] = 0  # Hapus area sekitar puncak
        
        # Tampilkan frekuensi dominan
        if dominant_freqs:
            info_text = "Frekuensi dominan:\n"
            for i, (freq, mag) in enumerate(dominant_freqs[:5]):
                info_text += f"{i+1}. {freq:.1f} Hz (mag: {mag:.2f})\n"
                # Tandai di plot
                ax.plot(freq, mag, 'ro', markersize=5)
                ax.text(freq, mag, f" {freq:.1f} Hz", fontsize=8)
            
            ax.text(0.02, 0.95, info_text, transform=ax.transAxes, 
                    bbox=dict(facecolor='white', alpha=0.8), fontsize=8)
        
        figure.tight_layout()
    
    def plot_3d_spectrogram(self, audio_data, sample_rate, figure, colormap='viridis', freq_range=(0, 1000), resolution=1024):
        """
        Menggambar spektrogram 3D
        """
        figure.clear()
        ax = figure.add_subplot(111, projection='3d')
        
        # Buat spektrogram
        f, t, Sxx = signal.spectrogram(audio_data, fs=sample_rate, nperseg=resolution)
        
        # Filter frekuensi
        freq_mask = (f >= freq_range[0]) & (f <= freq_range[1])
        f_filtered = f[freq_mask]
        Sxx_filtered = Sxx[freq_mask, :]
        
        # Konversi ke dB
        Sxx_db = 10 * np.log10(Sxx_filtered + 1e-10)
        
        # Buat mesh grid untuk plot 3D
        T, F = np.meshgrid(t, f_filtered)
        
        # Plot 3D surface
        surf = ax.plot_surface(T, F, Sxx_db, cmap=colormap, linewidth=0, antialiased=True)
        
        ax.set_ylabel('Frekuensi (Hz)')
        ax.set_xlabel('Waktu (detik)')
        ax.set_zlabel('Intensitas (dB)')
        ax.set_title('Spektrogram 3D')
        
        # Tambahkan colorbar
        figure.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='Intensitas (dB)')
        
        # Atur sudut pandang
        ax.view_init(30, 45)
        
        figure.tight_layout()
    
    def plot_combined_analysis(self, audio_data, sample_rate, figure, colormap='viridis', freq_range=(0, 1000)):
        """
        Menggambar analisis gabungan (waveform dan spektrogram)
        """
        figure.clear()
        
        # Bagi plot menjadi 2 bagian
        gs = figure.add_gridspec(2, 1, height_ratios=[1, 2], hspace=0.3)
        
        # Subplot untuk waveform
        ax1 = figure.add_subplot(gs[0])
        time = np.arange(0, len(audio_data)) / sample_rate
        ax1.plot(time, audio_data, color='#3498db')
        ax1.set_ylabel('Amplitudo')
        ax1.set_title('Bentuk Gelombang Audio')
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.set_ylim(-1.1, 1.1)
        
        # Subplot untuk spektrogram
        ax2 = figure.add_subplot(gs[1])
        f, t, Sxx = signal.spectrogram(audio_data, fs=sample_rate, nperseg=1024)
        pcm = ax2.pcolormesh(t, f, 10 * np.log10(Sxx + 1e-10), shading='gouraud', cmap=colormap)
        ax2.set_ylabel('Frekuensi (Hz)')
        ax2.set_xlabel('Waktu (detik)')
        ax2.set_ylim(freq_range)
        
        # Tambahkan colorbar
        figure.colorbar(pcm, ax=ax2, label='Intensitas (dB)')
        
        # Sinkronkan sumbu x
        ax1.set_xlim(0, time[-1])
        ax2.set_xlim(0, t[-1])
        
        # Tambahkan info
        duration = len(audio_data) / sample_rate
        info_text = f"Durasi: {duration:.2f} detik | Sample rate: {sample_rate} Hz"
        figure.text(0.5, 0.01, info_text, ha='center', fontsize=8)
        
        figure.tight_layout()
