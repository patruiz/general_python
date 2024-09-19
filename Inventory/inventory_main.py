import os 
import sqlite3
import pandas as pd 

class shop_db:
    def __init__(self, db_path):
        self.database = sqlite3.connect(db_path)
        self.curr = self.database.cursor()

    def database_connect(self):
        pass

    def create_tables(self):
        
        self.curr.execute(
            """
            CREATE TABLE IF NOT EXISTS Items(
            Name TEXT PRIMARY KEY NOT NULL
            )
            """
        )

        self.curr.execute(
            """
            CREATE TABLE IF NOT EXISTS Filament(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Color TEXT NOT NULL,
            Type TEXT NOT NULL,
            Brand TEXT NOT NULL,
            UNIQUE (Color, Type, Brand),
            FOREIGN KEY (Item) REFERENCES Items(Name)
            )
            """
        )

        self.curr.execute(
            """
            CREATE TABLE IF NOT EXISTS Components(
            ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            DESCRIPTION TEXT NOT NULL,
            Item TEXT NOT NULL,
            Filament INTEGER NOT NULL,
            FOREIGN KEY (Item) REFERENCES Items(Name),
            FOREIGN KEY (Filament) REFERENCES Filament(ID)
            )
            """
        )

    def load_data(self):
        path = os.path.join(os.getcwd(), 'Inventory', 'Data', 'Items.csv')
        print(path)
        df = pd.read_csv(path)
        for index, val in df.iterrows():
            self.curr.execute(
                """INSERT INTO Items VALUES (?)""", (val)
            )
        self.database.commit()

        
    
    def enter_values(self, color, type, brand, item):
        self.curr.execute(
            """INSERT INTO Filament (color, type, brand, item) VALUES (?, ?, ?, ?)""", (color, type, brand, item)
        )

        self.database.commit()


ass = shop_db('swag.db')
ass.create_tables()
ass.load_data()
# ass.enter_values('Charcoal', 'PLA Matte', 'Bambu', 'Pokeball')



