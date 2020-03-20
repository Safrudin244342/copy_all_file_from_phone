"""
program ini dubuat untuk mengcopy file dengan ektensi khusu dari flashdisk

by bening / 6 maret 2020
"""
import os
import threading

# deklarasi semua variable yang akan digunakan
class variable:
    pusat_dir = '/run/user/0/gvfs'
    list_file = []
    ektensi = {
        "image": ['jpg', 'jpeg', 'png', 'JPG', 'JPEG', 'PNG'],
        "aplikasi": ['apk', 'APK'],
        "kompres": ['zip', 'ZIP', 'rar', 'RAR', '7z'],
        "musik": ['mp3', 'MP3'],
        "video": ['mp4', 'MP4', '3gp', '3GP']
    }
    ektensi_search = ""
    size_transfer = []
    maks_transfer = 10
    folder_tujuan = "/usr/project/python/copy_all_flashdisk/copy/"

# membaca semua folder dan file yang ada
def read_file_and_dir(path):
    list_path = os.listdir(path)
    for dir in list_path:
        if os.path.isdir(path + "/" + dir):
            t = threading.Thread(target=read_file_and_dir, args=(path + "/" + dir, ))
            t.start()
            t.join()
        else:
            ektensi_file = dir.split(".")
            ektensi_file = ektensi_file[len(ektensi_file) - 1]
            if ektensi_file in variable.ektensi_search:
                print(path + "/" + dir)
                variable.size_transfer.append(os.path.getsize(path + "/" + dir))
                variable.list_file.append(path + "/" + dir)

# membagi tugas untuk mengirimkan semua file lebih cepat
def copy_all_file():
    jml_file = len(variable.list_file)

    if jml_file >= variable.maks_transfer:
        split = int(jml_file / variable.maks_transfer)
        awal = 0
        akhir = split
        t = []
        for i in range(variable.maks_transfer):
            t.append(threading.Thread(target=copy_file, args=(variable.list_file[awal:akhir], )))
            awal += split
            akhir += split

        for thread in t:
            thread.start()
            thread.join()
    else:
        copy_file(variable.list_file)

# mengcopy file
def copy_file(list_file):
    for file in list_file:
        print("Copy : " + file)
        os.system("cp '" + file + "' '" + variable.folder_tujuan + "'")

# membaca semua folder dari flashdisk
# /run/user/0/gvfs/
# tempat dimana folder flashdisk disimpan

daftar_mtp = os.listdir(variable.pusat_dir)
for i in range(len(daftar_mtp)):
    print(str(i + 1) + ". " + daftar_mtp[i])

flashdisk = daftar_mtp[int(input("Pilih flashdisk mana yang akan diambail datanya : ")) - 1]
ektensi = input("File ektensi yang akan diambil : ")

if ektensi in variable.ektensi:
    variable.ektensi_search = variable.ektensi[ektensi]
else:
    variable.ektensi_search = [ektensi]

# membaca semua file dan folder
read_file_and_dir(variable.pusat_dir + "/" + flashdisk)

# menghitung jumlah byte yang akan dikirim
transfer = 0
for size in variable.size_transfer:
    transfer += size

transfer /= 1000000

print("Jumlah yang akan ditrensfer: " + str(int(transfer)) + " MB")
conf = input("Lanjutkan Pengiriman [yes/no] : ")
if conf == "yes":
    print("Mengirim file!")
    copy_all_file()

print("------------------------------Tugas selesai----------------------------------")