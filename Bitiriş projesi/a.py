from config import *
import sqlite3
from config import Database 
from discord import ui,ButtonStyle

class DB_Manager:
    def __init__(self,database):
        self.database=database
    def create_tables(self):
        conn=sqlite3.connect(self.database)
        with conn:
            conn.execute("""CREATE TABLE Student( 
                         Student_id INTEGER PRIMARY KEY,
                         Adi INTEGER,
                         Numarasi INTEGER,
                         Sinif INTEGER,
                         FOREIGN KEY(Sinif) REFERENCES Lesson(Sinif)  
                         )""")



            conn.execute("""CREATE TABLE Lesson(
                         Program_id INTEGER PRIMARY KEY,
                         Sinif INTEGER,
                         Ders TEXT,
                         Saat INTEGER
                         ) """)
            
        
            return "Tablo oluştutuldu"

siniflar=(5,6,7,8,9,10,11,12)
def gen_buttons(self):
        buttons = []
        for option in siniflar:
            buttons.append(ui.Button(label=option, style=ButtonStyle.primary))
        return buttons



if __name__=="__main__":
    start=DB_Manager(database=Database) 
    print(start.create_tables())
   