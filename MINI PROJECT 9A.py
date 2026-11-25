import csv
import os

folder = os.path.dirname(os.path.abspath(__file__))
file_data = os.path.join(folder, "data-kualitas-air-sungai.csv")
file_akun = os.path.join(folder, "akun.csv")
file_pref = os.path.join(folder, "pengaturan.csv")

PARAM = {"1": ("ph", "pH"), "2": ("do", "DO (mg/L)"), "3": ("bod", "BOD (mg/L)"),
         "4": ("cod", "COD (mg/L)"), "5": ("ip", "Nilai IP")}
KRITERIA = {"1": "Tertinggi", "2": "Terendah", "3": "Rentang nilai"}

akun = {}  
pref = {}  

def ke_angka(teks):
    teks = teks.strip().replace("<", "").replace(",", ".")
    try:
        return float(teks)
    except ValueError:
        return None

def baca_csv(path):
    baris_semua = []
    if os.path.exists(path):
        f = open(path, newline="", encoding="utf-8")
        for baris in csv.reader(f, delimiter=";"):
            baris_semua.append(baris)
        f.close()
    return baris_semua

def tulis_csv(path, baris_semua):
    f = open(path, "w", newline="", encoding="utf-8")
    csv.writer(f, delimiter=";").writerows(baris_semua)
    f.close()

class Akun:
    def register():
        print("\n--- REGISTER ---")
        username = input("Username baru: ").strip()
        password = input("Password (min. 4 karakter): ")
        if username == "":
            print("Register gagal: username kosong.")
        elif username in akun:
            print("Register gagal: username sudah dipakai.")
        elif len(password) < 4:
            print("Register gagal: password terlalu pendek.")
        else:
            akun[username] = password
            tulis_csv(file_akun, [[u, akun[u]] for u in akun])
            print("Register berhasil! Silakan login.")

    def login():
        print("\n--- LOGIN ---")
        for i in range(3):
            username = input("Username: ").strip()
            password = input("Password: ")
            if username in akun and akun[username] == password:
                print("Login berhasil. Selamat datang,", username)
                return username
            print("Username/password salah. Sisa percobaan:", 2 - i)
        return None

class Pengaturan:
    def simpan(user, nama, nilai):
        pref[(user, nama)] = nilai
        tulis_csv(file_pref, [[k[0], k[1], pref[k]] for k in pref])

    def daerah_aktif(user, ganti=False):
        kata = pref.get((user, "daerah"))
        if kata is None or ganti:
            kata = input("Filter (contoh: Aceh Barat / Krueng Woyla, kosong = semua): ").strip()
            Pengaturan.simpan(user, "daerah", kata if kata != "" else "*")
            print("(Daerah disimpan)")
            return kata
        if kata == "*":
            kata = ""
        print("Daerah aktif:", kata if kata != "" else "(semua)")
        return kata

class Program:
    def saring(data, kata):
        hasil = []
        for d in data:
            teks = d["kabupaten"] + " " + d["sungai"] + " " + d["lokasi"]
            if kata.lower() in teks.lower():
                hasil.append(d)
        return hasil

    def urutkan(data, kunci, besar_dulu):
        hasil = data[:]
        n = len(hasil)
        for i in range(n):
            for j in range(n - 1 - i):
                if besar_dulu:
                    tukar = hasil[j][kunci] < hasil[j + 1][kunci]
                else:
                    tukar = hasil[j][kunci] > hasil[j + 1][kunci]
                if tukar:
                    hasil[j], hasil[j + 1] = hasil[j + 1], hasil[j]
        return hasil

    def pilih_jumlah(satuan):
        print("Tampilkan berapa", satuan + "?")
        print("  1. 5 " + satuan)
        print("  2. 10 " + satuan)
        print("  3. Semua " + satuan)
        pilih = input("Pilih (1-3): ").strip()
        if pilih == "1":
            return "5"
        elif pilih == "2":
            return "10"
        elif pilih == "3":
            return "semua"
        print("Pilihan tidak valid.")
        return None

    def muat_data():
        data = []
        dibuang = 0
        f = open(file_data, newline="", encoding="cp1252")
        baca = csv.reader(f, delimiter=";")
        next(baca)
        for baris in baca:
            if len(baris) < 34 or baris[4].strip() != "2020":
                dibuang += 1
                continue
            d = {}
            d["kabupaten"] = baris[3].strip()
            d["sungai"] = baris[5].strip()
            d["lokasi"] = baris[7].strip()
            d["ph"] = ke_angka(baris[10])
            d["do"] = ke_angka(baris[14])
            d["bod"] = ke_angka(baris[17])
            d["cod"] = ke_angka(baris[18])
            d["ip"] = ke_angka(baris[32])
            d["status"] = baris[33].strip()
            if None in (d["ph"], d["do"], d["bod"], d["cod"], d["ip"]):
                dibuang += 1
                continue
            data.append(d)
        f.close()
        return data, dibuang

    def cetak_tabel(hasil, kunci, label):
        if len(hasil) == 0:
            print("Data tidak ditemukan.")
            return
        print("\nParameter:", label)
        print("{:<3} {:<22} {:<20} {:<34} {:>7}  {}".format(
            "No", "Kabupaten/Kota", "Sungai", "Lokasi", "Nilai", "Status"))
        print("-" * 103)
        no = 1
        for d in hasil:
            print("{:<3} {:<22} {:<20} {:<34} {:>7.2f}  {}".format(
                no, d["kabupaten"][:22], d["sungai"][:20],
                d["lokasi"][:34], d[kunci], d["status"]))
            no += 1
        print("Total:", len(hasil), "data")

    def menu_rata_rata(data, user):
        print("\n--- RATA-RATA PER LOKASI ---")
        terfilter = Program.saring(data, Pengaturan.daerah_aktif(user))

        kelompok = {}
        for d in terfilter:
            kunci = (d["sungai"], d["lokasi"])
            if kunci not in kelompok:
                kelompok[kunci] = []
            kelompok[kunci].append(d)

        if len(kelompok) == 0:
            print("Data tidak ditemukan.")
            return

        print("\n{:<20} {:<40} {:>6} {:>6} {:>7} {:>8}".format(
            "Sungai", "Lokasi", "pH", "DO", "BOD", "COD"))
        print("-" * 92)
        for kunci in kelompok:
            daftar = kelompok[kunci]
            n = len(daftar)
            rata = []
            for p in ["ph", "do", "bod", "cod"]:
                total = 0
                for x in daftar:
                    total += x[p]
                rata.append(total / n)
            print("{:<20} {:<40} {:>6.2f} {:>6.2f} {:>7.2f} {:>8.2f}".format(
                kunci[0][:20], kunci[1][:40], rata[0], rata[1], rata[2], rata[3]))
        print("Total:", len(kelompok), "lokasi")

    def menu_cari(data, user):
        print("\n--- CARI DATA ---")
        terfilter = Program.saring(data, Pengaturan.daerah_aktif(user))
        param = pref.get((user, "param"))
        kriteria = pref.get((user, "kriteria"))
        pakai = False
        if param is not None and kriteria is not None:
            print("Pengaturan terakhir -> Parameter:", PARAM[param][1],
                  "| Kriteria:", KRITERIA[kriteria])
            pakai = input("Gunakan pengaturan terakhir ini? (y/n): ").strip().lower() == "y"

        if not pakai:
            print("  1. pH\n  2. DO (mg/L)\n  3. BOD (mg/L)\n  4. COD (mg/L)\n  5. Nilai IP")
            param = input("Pilih parameter (1-5): ").strip()
            if param not in PARAM:
                print("Pilihan tidak valid.")
                return
            print("Kriteria: 1. Tertinggi  2. Terendah  3. Rentang nilai")
            kriteria = input("Pilih kriteria (1-3): ").strip()
            if kriteria == "3":
                bawah = input("Nilai minimum (contoh: 6.5): ")
                atas = input("Nilai maksimum (contoh: 8.5): ")
                if ke_angka(bawah) is None or ke_angka(atas) is None:
                    print("Nilai harus berupa angka.")
                    return
                Pengaturan.simpan(user, "bawah", bawah)
                Pengaturan.simpan(user, "atas", atas)
            elif kriteria == "1" or kriteria == "2":
                jumlah = Program.pilih_jumlah("data")
                if jumlah is None:
                    return
                Pengaturan.simpan(user, "jumlah", jumlah)
            else:
                print("Kriteria tidak valid.")
                return
            Pengaturan.simpan(user, "param", param)
            Pengaturan.simpan(user, "kriteria", kriteria)
            print("(Pengaturan disimpan)")

        kunci, label = PARAM[param]

        if kriteria == "3":
            bawah = ke_angka(pref[(user, "bawah")])
            atas = ke_angka(pref[(user, "atas")])
            hasil = []
            for d in terfilter:
                if d[kunci] >= bawah and d[kunci] <= atas:
                    hasil.append(d)
        else:
            kode = pref[(user, "jumlah")]
            jumlah = len(terfilter) if kode == "semua" else int(kode)
            hasil = Program.urutkan(terfilter, kunci, kriteria == "1")[:jumlah]

        Program.cetak_tabel(hasil, kunci, label)

    def menu_prioritas(data, user):
        print("\n--- PRIORITAS PEMANTAUAN (Nilai IP) ---")
        print("Lokasi diurutkan dari Nilai IP terbesar (paling tercemar) ke terkecil.")
        terfilter = Program.saring(data, Pengaturan.daerah_aktif(user))
        kode = pref.get((user, "jml_prioritas"))
        pakai = False
        if kode is not None:
            print("Pengaturan terakhir -> Jumlah lokasi teratas:", kode)
            pakai = input("Gunakan pengaturan terakhir ini? (y/n): ").strip().lower() == "y"
        if not pakai:
            kode = Program.pilih_jumlah("lokasi")
            if kode is None:
                return
            Pengaturan.simpan(user, "jml_prioritas", kode)
            print("(Pengaturan disimpan)")

        jumlah = len(terfilter) if kode == "semua" else int(kode)
        urut = Program.urutkan(terfilter, "ip", True)
        Program.cetak_tabel(urut[:jumlah], "ip", "Nilai IP")

        hitung = {}
        for d in terfilter:
            hitung[d["status"]] = hitung.get(d["status"], 0) + 1
        print("\nRingkasan status mutu air:")
        for status in hitung:
            print("  -", status + ":", hitung[status], "titik")

    def main():
        if not os.path.exists(file_data):
            print("File data tidak ditemukan:", file_data)
            return

        data, dibuang = Program.muat_data()
        print("Data dimuat:", len(data), "baris valid,", dibuang, "baris dibuang.")

        for b in baca_csv(file_akun):
            if len(b) >= 2:
                akun[b[0]] = b[1]
        for b in baca_csv(file_pref):
            if len(b) >= 3:
                pref[(b[0], b[1])] = b[2]

        while True:
            print("\n=== KUALITAS AIR SUNGAI & DANAU ACEH 2020 ===")
            print(" 1. Register\n 2. Login\n 3. Keluar")
            pilih = input("Pilih (1-3): ").strip()

            if pilih == "1":
                Akun.register()
            elif pilih == "2":
                user = Akun.login()
                while user is not None:
                    print("\n=== MENU UTAMA (user:", user + ") ===")
                    print(" 1. Rata-rata pH, DO, BOD, COD per lokasi")
                    print(" 2. Cari data (tertinggi / terendah / rentang)")
                    print(" 3. Prioritas pemantauan (Nilai IP & status)")
                    print(" 4. Ganti daerah")
                    print(" 5. Logout")
                    menu = input("Pilih menu (1-5): ").strip()

                    if menu == "1":
                        Program.menu_rata_rata(data, user)
                    elif menu == "2":
                        Program.menu_cari(data, user)
                    elif menu == "3":
                        Program.menu_prioritas(data, user)
                    elif menu == "4":
                        print("\n--- GANTI DAERAH ---")
                        Pengaturan.daerah_aktif(user, ganti=True)
                    elif menu == "5":
                        print("Anda telah logout.")
                        user = None
                    else:
                        print("Pilihan tidak valid.")
            elif pilih == "3":
                print("Terima kasih.")
                break
            else:
                print("Pilihan tidak valid.")

Program.main()