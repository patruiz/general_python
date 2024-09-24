import os 
import sqlite3
import keyboard
import pandas as pd 

class Database:
    def __init__(self, db_path):
        self.db_path = db_path 
        self.database = None
        self.curr = None

    def database_connect(self):
        os.system('cls')
        # print(f'Connecting to {self.db_path} . . .')
        try:
            self.database = sqlite3.connect(self.db_path)
            self.curr = self.database.cursor()
            # print('\nConnection Successful . . .')
            # print('Press Enter to Continue . . .')
            # keyboard.wait('enter')
            # print("")
        except sqlite3.IntegrityError as e:
            # print(f'Item {val.iloc[0]} already exists in the database.')
            pass

    def database_disconnect(self):
        if self.database and self.curr != None:
            self.curr.close()

    def create_tables(self):
        if self.database and self.curr != None:
    
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

            # Part Table
            self.curr.execute(
                """
                CREATE TABLE IF NOT EXISTS Parts(
                Part_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                Part_Type TEXT NOT NULL,
                Part_Variant TEXT(1) NOT NULL,
                Filament_ID INTEGER NOT NULL,
                UNIQUE (Part_Type, Part_Variant, Filament_ID),
                FOREIGN KEY (Filament_ID) REFERENCES Filament(Filament_ID)
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
            
            # Inventory Table
            self.curr.execute(
                """ 
                CREATE TABLE IF NOT EXISTS Inventory (
                Part_ID INTEGER PRIMARY KEY,
                Qty INTEGER DEFAULT 0, 
                FOREIGN KEY (Part_ID) REFERENCES Parts (Part_ID)
                )
                """
            )

            

    def load_data(self):
        if self.database and self.curr != None:
        
            data_files = ['item_data.csv', 'filament_data.csv', 'part_data.csv', 'bom_data.csv']

            # Item Data - Load
            for file in data_files:
                path = os.path.join(os.getcwd(), 'Inventory', 'data', 'references', file)
                df = pd.read_csv(path)

                if file == data_files[0]:
                    for index, val in df.iterrows():
                        item = val.loc['Item']
                        try:
                            self.curr.execute("""INSERT INTO Items (Item_Name) VALUES (?)""", (item, ))
                        except sqlite3.IntegrityError as e:
                            # print(f'Item {val.iloc[0]} already exists in the database.')
                            pass

                # Filament Data - Load                    
                elif file == data_files[1]:
                    for index, val in df.iterrows():
                        color = val.loc['Color']
                        fil_type = val.loc['Type']
                        brand = val.loc['Brand']
                        try:
                            self.curr.execute("""INSERT INTO Filament (Filament_Color, Filament_Type, Filament_Brand) VALUES (?, ?, ?)""", (color, fil_type, brand))
                        except sqlite3.IntegrityError as e:
                            # print(f'Item {val.iloc[0]} already exists in the database.')
                            pass

                # Parts Data - Load                         
                elif file == data_files[2]:
                    self.curr.execute("""SELECT Filament_ID FROM Filament""")
                    filament_list = [i[0] for i in self.curr.fetchall()]
                    for index, val in df.iterrows():
                        part_type, part_variant = val.loc['Part Type'], val.loc['Variant']
                        for filament in filament_list:
                            try:
                                self.curr.execute("""INSERT INTO Parts (Part_Type, Part_Variant, Filament_ID) VALUES (?, ?, ?)""", (part_type, part_variant, filament))
                            except sqlite3.IntegrityError as e:
                                # print(f'Item {val.iloc[0]} already exists in the database.')
                                pass
                        
                # BOM Data - Load
                elif file == data_files[3]:
                    for index, val in df.iterrows():
                        # print(val)
                        self.curr.execute("""SELECT Item_ID FROM Items WHERE Item_Name = ?""", (val.loc['Item'], ))
                        item_id = self.curr.fetchone()[0]

                        self.curr.execute("""SELECT Filament_ID FROM Filament WHERE (Filament_Color = ? AND Filament_Type = ? AND Filament_Brand = ?)""", (val.loc['Color'], val.loc['Filament Type'], val.loc['Filament Brand']) )
                        filament_id = self.curr.fetchone()[0]

                        self.curr.execute("""SELECT Part_ID FROM Parts WHERE (Part_Type = ? AND Part_Variant = ? AND Filament_ID = ?)""", (val.loc['Part Type'], val.loc['Variant'], filament_id))
                        part_id = self.curr.fetchone()[0]

                        # print(f"Item ID: {item_id}, Filament ID: {filament_id}, Part ID: {part_id}")

                        try:
                            self.curr.execute("""INSERT INTO BOM (Item_ID, Part_ID, Qty) VALUES (?, ?, ?)""", (item_id, part_id, int(val.loc['Qty'])))
                        except sqlite3.IntegrityError as e:
                            # print(f'Item {val.iloc[0]} already exists in the database.')
                            pass


            self.database.commit()




