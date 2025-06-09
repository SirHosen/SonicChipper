#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SonicCipher - Aplikasi Kriptografi Teks ke Suara
Audio Processor - Logika enkripsi dan dekripsi audio
"""

import numpy as np
import scipy.io.wavfile as wav
import pygame
import json
import time
import os
from scipy import signal

class AudioProcessor:
    def __init__(self):
        pygame.mixer.init(frequency=44100, size=-16, channels=1)
        self.sample_rate = 44100  # Hz
    
    def encrypt_to_audio(self, text, key, base_freq=220, base_duration=0.1, algorithm="FSAE Standard"):
        """
        Enkripsi teks menjadi audio menggunakan algoritma FSAE
        
        Args:
            text (str): Teks yang akan dienkripsi
            key (int): Kunci enkripsi (1-25)
            base_freq (float): Frekuensi dasar dalam Hz
            base_duration (float): Durasi dasar dalam detik
            algorithm (str): Algoritma enkripsi yang digunakan
            
        Returns:
            dict: Data audio terenkripsi dan metadata
        """
        # Metadata untuk membantu dekripsi
        metadata = {
            'algorithm': algorithm,
            'base_freq': base_freq,
            'base_duration': base_duration,
            'freq_range': 660,  # Rentang frekuensi dari base_freq
            'char_count': len(text),
            'encryption_date': time.strftime("%Y-%m-%d %H:%M:%S"),
            'version': '1.0.0'
        }
        
        # Enkripsi teks menjadi frekuensi
        frequencies = []
        durations = []
        amplitudes = []
        
        for i, char in enumerate(text):
            # Dapatkan kode ASCII dan terapkan shift
            char_code = ord(char)
            shifted_code = (char_code + key) % 256
            
            # Petakan ke rentang frekuensi yang dapat didengar
            frequency = base_freq + (shifted_code / 256) * metadata['freq_range']
            
            # Variasikan durasi berdasarkan algoritma
            if algorithm == "FSAE Standard":
                # Durasi tetap
                duration = base_duration
            elif algorithm == "FSAE Enhanced":
                # Variasi durasi berdasarkan posisi
                duration = base_duration + (i % 5) * 0.05
            elif algorithm == "FSAE + AES":
                # Simulasi AES dengan variasi kompleks
                # Dalam implementasi nyata, ini akan menggunakan enkripsi AES sebenarnya
                duration = base_duration + (((i * key) % 10) / 100)
            else:
                # Default
                duration = base_duration
            
            # Variasikan amplitudo untuk algoritma enhanced
            if algorithm in ["FSAE Enhanced", "FSAE + AES"]:
                # Variasi amplitudo berdasarkan karakter
                amplitude = 0.4 + (shifted_code % 50) / 100  # Range 0.4-0.9
            else:
                amplitude = 0.5  # Default
            
            frequencies.append(frequency)
            durations.append(duration)
            amplitudes.append(amplitude)
        
        # Simpan karakter asli untuk verifikasi (khusus debugging)
        metadata['original_chars'] = [ord(c) for c in text]
        metadata['shifted_chars'] = [(ord(c) + key) % 256 for c in text]
        
        # Simpan frekuensi dan durasi dalam metadata
        metadata['frequencies'] = frequencies
        metadata['durations'] = durations
        metadata['amplitudes'] = amplitudes
        
        # Buat sinyal audio
        audio_data = self._generate_audio_signal(frequencies, durations, amplitudes)
        
        return {
            'audio': audio_data,
            'sample_rate': self.sample_rate,
            'metadata': metadata
        }
    
    def _generate_audio_signal(self, frequencies, durations, amplitudes=None):
        """
        Menghasilkan sinyal audio dari frekuensi dan durasi
        """
        if amplitudes is None:
            amplitudes = [0.5] * len(frequencies)
            
        total_samples = int(sum(durations) * self.sample_rate)
        audio_signal = np.zeros(total_samples)
        
        current_sample = 0
        for freq, duration, amplitude in zip(frequencies, durations, amplitudes):
            t = np.arange(0, duration, 1/self.sample_rate)
            samples = amplitude * np.sin(2 * np.pi * freq * t)
            
            # Tambahkan fade in/out untuk menghindari klik
            fade_samples = min(int(0.01 * self.sample_rate), len(samples) // 4)
            fade_in = np.linspace(0, 1, fade_samples)
            fade_out = np.linspace(1, 0, fade_samples)
            
            samples[:fade_samples] *= fade_in
            samples[-fade_samples:] *= fade_out
            
            # Tambahkan ke sinyal utama
            end_sample = current_sample + len(samples)
            if end_sample <= total_samples:
                audio_signal[current_sample:end_sample] = samples
            else:
                audio_signal[current_sample:] = samples[:total_samples-current_sample]
            
            current_sample = end_sample
        
        return audio_signal
    
    def play_audio(self, audio_data, sample_rate):
        """
        Memutar data audio
        """
        # Normalisasi audio ke range 16-bit
        audio_data = np.int16(audio_data * 32767)
        
        # Buat file sementara
        temp_file = "temp_audio.wav"
        wav.write(temp_file, sample_rate, audio_data)
        
        # Putar audio
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()
    
    def stop_audio(self):
        """
        Menghentikan pemutaran audio
        """
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
    
    def save_audio(self, file_path, audio_data, sample_rate, metadata):
        """
        Menyimpan audio terenkripsi dan metadata ke file
        """
        # Normalisasi audio ke range 16-bit
        audio_data = np.int16(audio_data * 32767)
        
        # Simpan audio
        wav.write(file_path, sample_rate, audio_data)
        
        # Simpan metadata dalam file terpisah
        metadata_file = file_path + ".metadata"
        try:
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            print(f"Metadata berhasil disimpan ke {metadata_file}")
        except Exception as e:
            print(f"Error saat menyimpan metadata: {str(e)}")
            
        # Simpan juga sebagai file teks biasa untuk backup
        text_file = file_path + ".info.txt"
        try:
            with open(text_file, 'w') as f:
                f.write(f"SonicCipher Encrypted Audio\n")
                f.write(f"Encrypted on: {metadata.get('encryption_date', 'Unknown')}\n")
                f.write(f"Algorithm: {metadata.get('algorithm', 'FSAE Standard')}\n")
                f.write(f"Base Frequency: {metadata.get('base_freq', 220)} Hz\n")
                f.write(f"Frequency Range: {metadata.get('freq_range', 660)} Hz\n")
                f.write(f"Character Count: {metadata.get('char_count', 0)}\n")
                
                if 'frequencies' in metadata:
                    f.write(f"Frequencies: {', '.join([f'{freq:.2f}' for freq in metadata['frequencies'][:10]])}")
                    if len(metadata['frequencies']) > 10:
                        f.write(f"... (and {len(metadata['frequencies']) - 10} more)")
                    f.write("\n")
        except Exception as e:
            print(f"Error saat menyimpan info file: {str(e)}")
    
    def load_audio(self, file_path):
        """
        Memuat file audio dan metadata
        """
        # Baca file audio
        sample_rate, audio_data = wav.read(file_path)
        
        # Normalisasi ke range -1.0 hingga 1.0
        audio_data = audio_data.astype(np.float32) / 32767.0
        
        # Coba baca metadata
        metadata = None
        metadata_file = file_path + ".metadata"
        if os.path.exists(metadata_file):
            try:
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                print(f"Metadata berhasil dimuat dari {metadata_file}")
            except Exception as e:
                print(f"Error saat memuat metadata: {str(e)}")
        else:
            print(f"File metadata tidak ditemukan: {metadata_file}")
        
        return audio_data, sample_rate, metadata
    
    def decrypt_from_audio(self, audio_data, sample_rate, key, tolerance=0.05, metadata=None):
        """
        Mendekripsi audio kembali menjadi teks
        
        Args:
            audio_data (numpy.array): Data audio
            sample_rate (int): Sample rate audio
            key (int): Kunci dekripsi
            tolerance (float): Toleransi frekuensi (dalam persen)
            metadata (dict): Metadata dari enkripsi (opsional)
            
        Returns:
            str: Teks terdekripsi
        """
        if metadata is None:
            # Jika tidak ada metadata, kita harus menganalisis audio
            return self._decrypt_without_metadata(audio_data, sample_rate, key, base_freq=220, freq_range=660, tolerance=tolerance)
        else:
            # Jika ada metadata, gunakan untuk dekripsi yang lebih akurat
            return self._decrypt_with_metadata(key, metadata)
    
    def _decrypt_with_metadata(self, key, metadata):
        """
        Mendekripsi menggunakan metadata yang tersedia
        """
        base_freq = metadata.get('base_freq', 220)
        freq_range = metadata.get('freq_range', 660)
        frequencies = metadata.get('frequencies', [])
        
        # Dekripsi frekuensi menjadi teks
        text = ''
        for freq in frequencies:
            # Konversi kembali dari frekuensi ke kode karakter
            normalized_freq = (freq - base_freq) / freq_range
            char_code = int(round(normalized_freq * 256))
            
            # Terapkan shift balik
            original_code = (char_code - key) % 256
            
            # Konversi ke karakter
            text += chr(original_code)
        
        return text
    
    def _decrypt_without_metadata(self, audio_data, sample_rate, key, base_freq=220, freq_range=660, tolerance=0.05):
        """
        Mendekripsi tanpa metadata menggunakan analisis frekuensi
        Metode ini lebih kompleks dan kurang akurat
        """
        # Deteksi segmen audio yang berisi nada
        segments = self._improved_tone_detection(audio_data, sample_rate)
        
        # Analisis frekuensi dominan di setiap segmen
        frequencies = []
        for start, end in segments:
            if end - start > 10:  # Pastikan segmen cukup panjang
                segment_data = audio_data[start:end]
                freq = self._get_dominant_frequency(segment_data, sample_rate)
                if freq > 0:  # Pastikan frekuensi valid
                    frequencies.append(freq)
        
        # Dekripsi frekuensi menjadi teks
        text = ''
        for freq in frequencies:
            # Konversi kembali dari frekuensi ke kode karakter dengan toleransi
            normalized_freq = (freq - base_freq) / freq_range
            
            # Terapkan toleransi - coba beberapa nilai dalam rentang toleransi
            possible_values = []
            for t in [-tolerance, 0, tolerance]:
                adjusted_freq = normalized_freq * (1 + t)
                if 0 <= adjusted_freq <= 1:  # Pastikan dalam rentang valid
                    char_code = int(round(adjusted_freq * 256))
                    original_code = (char_code - key) % 256
                    possible_values.append((original_code, abs(t)))  # Simpan nilai dan seberapa jauh dari asli
            
            # Pilih nilai dengan toleransi terkecil
            if possible_values:
                possible_values.sort(key=lambda x: x[1])  # Urutkan berdasarkan toleransi
                best_char_code = possible_values[0][0]
                text += chr(best_char_code)
            else:
                text += '?'  # Karakter tidak dapat didekripsi
        
        return text
    
    def _improved_tone_detection(self, audio_data, sample_rate):
        """
        Metode yang lebih baik untuk mendeteksi segmen nada dalam audio
        """
        # Hitung energi sinyal
        frame_length = int(0.02 * sample_rate)  # 20ms frame
        hop_length = int(0.01 * sample_rate)    # 10ms hop
        
        frames = []
        for i in range(0, len(audio_data) - frame_length, hop_length):
            frames.append(audio_data[i:i+frame_length])
        
        # Hitung energi untuk setiap frame
        energy = np.array([np.sum(frame**2) for frame in frames])
        
        # Normalisasi energi
        if np.max(energy) > 0:
            energy = energy / np.max(energy)
        
        # Tentukan threshold energi
        threshold = 0.1
        
        # Temukan frame di atas threshold
        active_frames = energy > threshold
        
        # Temukan transisi (awal dan akhir segmen)
        transitions = np.diff(active_frames.astype(int))
        segment_starts = np.where(transitions == 1)[0]
        segment_ends = np.where(transitions == -1)[0]
        
        # Pastikan jumlah start dan end sama
        if len(segment_starts) > len(segment_ends):
            segment_ends = np.append(segment_ends, len(active_frames) - 1)
        elif len(segment_starts) < len(segment_ends):
            segment_starts = np.insert(segment_starts, 0, 0)
        
        # Konversi indeks frame ke indeks sampel
        segments = []
        for start, end in zip(segment_starts, segment_ends):
            sample_start = start * hop_length
            sample_end = (end + 1) * hop_length + frame_length
            if sample_end > len(audio_data):
                sample_end = len(audio_data)
            segments.append((sample_start, sample_end))
        
        # Gabungkan segmen yang berdekatan
        if segments:
            merged_segments = [segments[0]]
            for current_start, current_end in segments[1:]:
                prev_start, prev_end = merged_segments[-1]
                
                # Jika segmen saat ini berdekatan dengan segmen sebelumnya
                if current_start - prev_end < frame_length:
                    # Gabungkan segmen
                    merged_segments[-1] = (prev_start, current_end)
                else:
                    # Tambahkan segmen baru
                    merged_segments.append((current_start, current_end))
            
            return merged_segments
        
        return segments
    
    def _get_dominant_frequency(self, audio_segment, sample_rate):
        """
        Mendapatkan frekuensi dominan dari segmen audio menggunakan STFT
        """
        if len(audio_segment) < 100:  # Terlalu pendek untuk analisis yang akurat
            return 0
        
        # Gunakan STFT untuk analisis frekuensi yang lebih baik
        nperseg = min(1024, len(audio_segment))
        f, t, Zxx = signal.stft(audio_segment, fs=sample_rate, nperseg=nperseg)
        
        # Ambil rata-rata magnitude spektrum
        magnitude = np.mean(np.abs(Zxx), axis=1)
        
        # Temukan frekuensi dengan magnitude tertinggi
        # Batasi pencarian ke rentang frekuensi yang diharapkan (200-1000 Hz)
        freq_mask = (f >= 200) & (f <= 1000)
        if np.sum(freq_mask) > 0:
            filtered_magnitude = magnitude[freq_mask]
            filtered_freqs = f[freq_mask]
            
            if len(filtered_magnitude) > 0:
                max_idx = np.argmax(filtered_magnitude)
                return filtered_freqs[max_idx]
        
        # Fallback ke metode FFT sederhana jika STFT tidak berhasil
        n = len(audio_segment)
        freqs = np.fft.rfftfreq(n, d=1/sample_rate)
        fft_data = np.abs(np.fft.rfft(audio_segment))
        
        # Filter ke rentang frekuensi yang diharapkan
        freq_mask = (freqs >= 200) & (freqs <= 1000)
        if np.sum(freq_mask) > 0:
            filtered_fft = fft_data[freq_mask]
            filtered_freqs = freqs[freq_mask]
            
            if len(filtered_fft) > 0:
                max_idx = np.argmax(filtered_fft)
                return filtered_freqs[max_idx]
        
        return 0
    
    def test_encryption_decryption(self, text, key=7):
        """
        Fungsi pengujian untuk memverifikasi enkripsi dan dekripsi
        """
        print(f"Teks asli: '{text}'")
        print(f"Kunci: {key}")
        
        # Enkripsi
        encrypted_data = self.encrypt_to_audio(text, key)
        print(f"Frekuensi: {encrypted_data['metadata']['frequencies'][:5]}...")
        
        # Dekripsi langsung dari metadata
        decrypted_text = self._decrypt_with_metadata(key, encrypted_data['metadata'])
        print(f"Teks terdekripsi: '{decrypted_text}'")
        
        # Verifikasi
        if text == decrypted_text:
            print("Sukses: Teks asli dan teks terdekripsi sama!")
        else:
            print("Gagal: Teks asli dan teks terdekripsi berbeda!")
            # Analisis karakter yang berbeda
            print("Analisis perbedaan:")
            for i, (orig, decrypted) in enumerate(zip(text, decrypted_text)):
                if orig != decrypted:
                    print(f"  Indeks {i}: Asli='{orig}' ({ord(orig)}) vs Dekripsi='{decrypted}' ({ord(decrypted)})")
        
        return text == decrypted_text
