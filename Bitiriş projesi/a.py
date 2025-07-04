from config import *
import sqlite3
from config import Database 
from discord import ui,ButtonStyle
import os


    


class DB_Manager:
    def __init__(self,database):
        self.database=database
        if not os.path.exists(self.database):
            self.create_tables()
    def create_tables(self):
        conn=sqlite3.connect(self.database)
        with conn:
            conn.execute("""CREATE TABLE Student( 
                         Student_id INTEGER PRIMARY KEY,
                         Ad TEXT,
                         Soyad TEXT,
                         Numara INTEGER,
                         Sinif INTEGER
                         )""")


            conn.execute("""CREATE TABLE Lesson(
                         Program_id INTEGER PRIMARY KEY,
                         Sinif INTEGER,
                         Ders TEXT,
                         Saat INTEGER
                         ) """)
            
        
            return "Tablo oluştutuldu"
    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()

    def __select_data(self, sql, data = tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()

        
    def ogrencikayit(self,id,ad,soyad,numara,sinif):
        try:
            sql="INSERT INTO Student (Student_id,Ad,Soyad,Numara,Sinif) VALUES (?,?,?,?,?)"
            self.__executemany(sql,[(id,ad,soyad,numara,sinif)])
            return f"Başarılı Kayıt"
        except Exception as a:
            return f"Kayıt Yapılamadı.{a}"
    

    def get_ogrenciler(self,data):
        try:
            sql="SELECT * FROM Student WHERE Student_id = ?"
            sonuc=self.__select_data(sql,(data,))
            return sonuc
        except Exception as a:
            return f"Öğrenci bulunamadı.{a}"
        
        



siniflar=(9,10,11,12)
def gen_buttons(self):
        buttons = []
        for option in siniflar:
            buttons.append(ui.Button(label=option, style=ButtonStyle.primary))
        return buttons


if __name__=="__main__":
    start=DB_Manager(database=Database) 
    print(start.create_tables())
   
