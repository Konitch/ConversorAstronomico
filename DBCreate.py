import sqlite3

class ConvDB():
    def __init__(self):
        self.conectar = sqlite3.connect('banco.db')
        self.createTable()

    def createTable(self):
        c = self.conectar.cursor()
        
        c.execute("""create table if not exists info_Conversao (
                     idusuario integer primary key autoincrement,
                     descricao text,
                     valorObtido float,
                     medida_De string,
                     medida_Para string,
                     resultado float)""")
        self.conectar.commit()
        c.close()