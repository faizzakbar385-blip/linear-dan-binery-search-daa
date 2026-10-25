import csv
import time
from dataclasses import dataclass

@dataclass
class Buku:
    judul: str
    penulis: str
    kategori: str

@dataclass
class HasilPencarian:
    buku: Buku | None
    perbandingan: int
    waktu_detik: float

def ambil_kolom(baris, pilihan):
    for nama, isi in baris.items():
        if nama and nama.strip().lower().replace(' ', '_') in pilihan:
            return (isi or '').strip()
    return ''

def baca_dataset(nama_file):
    data = []
    with open(nama_file, encoding='utf-8-sig', newline='') as file:
        pembaca = csv.DictReader(file)
        for baris in pembaca:
            judul = ambil_kolom(baris, {'title', 'book_title', 'book_name', 'judul'})
            penulis = ambil_kolom(baris, {'author', 'authors', 'author_name', 'penulis'})
            kategori = ambil_kolom(baris, {'category', 'categories', 'genre', 'kategori'})
            if judul:
                data.append(Buku(judul, penulis, kategori))
    if not data:
        raise ValueError('Tidak ada judul buku. Periksa nama kolom pada CSV.')
    return data

def linear_search(data, kata_kunci):
    awal = time.perf_counter()
    jumlah = 0
    for buku in data:
        jumlah += 1
        if buku.judul.casefold() == kata_kunci.casefold():
            return HasilPencarian(buku, jumlah, time.perf_counter() - awal)
    return HasilPencarian(None, jumlah, time.perf_counter() - awal)

def binary_search(data_urut, kata_kunci):
    awal = time.perf_counter()
    kiri, kanan, jumlah = 0, len(data_urut) - 1, 0
    kunci = kata_kunci.casefold()
    while kiri <= kanan:
        tengah = (kiri + kanan) // 2
        judul = data_urut[tengah].judul.casefold()
        jumlah += 1  # satu perbandingan tiga-arah antara judul dan kunci
        if judul == kunci:
            return HasilPencarian(data_urut[tengah], jumlah, time.perf_counter() - awal)
        elif judul < kunci:
            kiri = tengah + 1
        else:
            kanan = tengah - 1
    return HasilPencarian(None, jumlah, time.perf_counter() - awal)

def tampilkan(hasil):
    if hasil.buku is None:
        print('Buku tidak ditemukan.')
    else:
        print('Judul:', hasil.buku.judul)
        print('Penulis:', hasil.buku.penulis)
        print('Kategori:', hasil.buku.kategori)
    print('Perbandingan:', hasil.perbandingan)
    print(f'Waktu: {hasil.waktu_detik:.9f} detik')

def uji(data):
    print('\nPENGUJIAN (waktu hanya proses pencarian, tidak termasuk pengurutan)')
    print(f"{'n':>7} | {'Algoritma':<14} | {'Skenario':<13} | {'Operasi':>8} | {'Detik':>12}")
    for n in (100, 1000, 10000):
        if len(data) < n:
            print(f'Lewati n={n}: dataset hanya memiliki {len(data)} baris.')
            continue
        bagian = data[:n]
        urut = sorted(bagian, key=lambda b: b.judul.casefold())
        for nama, fungsi, kumpulan in [('Linear', linear_search, bagian), ('Binary', binary_search, urut)]:
            for posisi, kunci in [('Awal', kumpulan[0].judul), ('Tengah', kumpulan[n//2].judul), ('Akhir', kumpulan[-1].judul), ('Tidak ada', '\uffffBUKU_TIDAK_ADA_123')]:
                hasil = fungsi(kumpulan, kunci)
                print(f'{n:7} | {nama:<14} | {posisi:<13} | {hasil.perbandingan:8} | {hasil.waktu_detik:12.9f}')

if __name__ == '__main__':
    lokasi = input('Masukkan lokasi file CSV dataset: ').strip().strip('"')
    try:
        buku = baca_dataset(lokasi)
        print(f'Data berhasil dibaca: {len(buku)} buku')
        kata = input('Masukkan judul buku yang dicari (persis): ').strip()
        print('\nLINEAR SEARCH')
        tampilkan(linear_search(buku, kata))
        print('\nBINARY SEARCH')
        buku_urut = sorted(buku, key=lambda b: b.judul.casefold())
        tampilkan(binary_search(buku_urut, kata))
        uji(buku)
    except (OSError, ValueError) as error:
        print('Gagal membaca dataset:', error)
