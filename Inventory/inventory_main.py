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
        
        # Items Table
        self.curr.execute(
            """
            CREATE TABLE IF NOT EXISTS Items(
            Item_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Item_Name TEXT UNIQUE NOT NULL
            )
            """
        )

        # Filament Table
        self.curr.execute(
            """
            CREATE TABLE IF NOT EXISTS Filament(
            Filament_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Filament_Color TEXT NOT NULL,
            Filament_Type TEXT NOT NULL,
            Filament_Brand TEXT NOT NULL,
            UNIQUE (Filament_Color, Filament_Type, Filament_Brand)
            )
            """
        )

        # Components Table
        self.curr.execute(
            """
            CREATE TABLE IF NOT EXISTS Parts(
            Part_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            Part_Description TEXT NOT NULL,
            Filament INTEGER NOT NULL,
            FOREIGN KEY (Filament) REFERENCES Filament(Filament_ID)
            )
            """
        )
        
        # BOM Table
        self.curr.execute(
            """
            CREATE TABLE IF NOT EXISTS BOM(
            Item_ID INTEGER NOT NULL,
            Part_ID INTEGER NOT NULL, 
            Qty INTEGER NOT NULL,
            PRIMARY KEY (Item_ID, Part_ID),
            FOREIGN KEY (Item_ID) REFERENCES Items(Item_ID)
            FOREIGN KEY (Part_ID) REFERENCES Parts(Part_ID)
            )
            """
        )

    def load_data(self):
        data_files = ['Item_Data.csv', 'Filament_Data.csv']
        
        for file in data_files:
            if file == 'Item_Data.csv':
                path = os.path.join(os.getcwd(), 'Inventory', 'Data', file)
                df = pd.read_csv(path)
                for index, val in df.iterrows():
                    self.curr.execute("""INSERT INTO Items (Item_Name) VALUES (?)""", (val.iloc[0], ))
                    
            elif file == 'Filament_Data.csv':
                path = os.path.join(os.getcwd(), 'Inventory', 'Data', file)
                df = pd.read_csv(path)
                print(df)
                # for index, val in df.iterrows():
                    # print
                
                
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



