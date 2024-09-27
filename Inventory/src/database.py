import os
import sqlite3
import pandas as pd

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.database = None
        self.curr = None
        self.change_log = []

    def database_connect(self):
        try:
            self.database = sqlite3.connect(self.db_path)
            self.curr = self.database.cursor()
            
        except sqlite3.IntegrityError:
            pass

    def database_disconnect(self):
        if self.database and self.curr:
            self.curr.close()
            self.database = None
            self.curr = None
            
    def show_changelog(self):
        print(self.change_log)

    def create_tables(self):
        if self.database and self.curr:
            
            # Groups Table
            self.curr.execute(
                """
                CREATE TABLE IF NOT EXISTS Groups(
                Group_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Group_Name TEXT UNIQUE NOT NULL
                )
                """
            )
            
            # Items Table
            self.curr.execute(
                """
                CREATE TABLE IF NOT EXISTS Items(
                Item_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Item_Name TEXT UNIQUE NOT NULL,
                Group_Name TEXT NOT NULL,
                FOREIGN KEY (Group_Name) REFERENCES Groups(Group_Name)
                )
                """
            )
            # Create Filament Table
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
            
            # Create Parts Table
            self.curr.execute(
                """
                CREATE TABLE IF NOT EXISTS Parts(
                Part_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Part_Type TEXT NOT NULL,
                Part_Variant TEXT NOT NULL,
                Filament_ID INTEGER NOT NULL,
                UNIQUE (Part_Type, Part_Variant, Filament_ID),
                FOREIGN KEY (Filament_ID) REFERENCES Filament(Filament_ID)
                )
                """
            )
            
            # Create BOM Table
            self.curr.execute(
                """
                CREATE TABLE IF NOT EXISTS BOM(
                Item_ID INTEGER NOT NULL,
                Part_ID INTEGER NOT NULL, 
                Qty INTEGER NOT NULL,
                PRIMARY KEY (Item_ID, Part_ID),
                FOREIGN KEY (Item_ID) REFERENCES Items(Item_ID),
                FOREIGN KEY (Part_ID) REFERENCES Parts(Part_ID)
                )
                """
            )
            
            # Create Inventory Table
            self.curr.execute(
                """ 
                CREATE TABLE IF NOT EXISTS Inventory (
                Part_ID INTEGER PRIMARY KEY,
                Qty INTEGER DEFAULT 0, 
                FOREIGN KEY (Part_ID) REFERENCES Parts(Part_ID)
                )
                """
            )

    def _get_filament_id (self, color, fil_type, brand):
        self.curr.execute("""SELECT Filament_ID FROM Filament WHERE Filament_Color = ? AND Filament_Type = ? AND Filament_Brand = ?""", (color, fil_type, brand))
        return self.curr.fetchone()

    def _enter_filament_data(self, color, fil_type, brand):
        self.curr.execute("""INSERT INTO Filament (Filament_Color, Filament_Type, Filament_Brand) VALUES (?, ?, ?)""", (color, fil_type, brand))
        # try:
        #     self.curr.execute("""INSERT INTO Filament (Filament_Color, Filament_Type, Filament_Brand) VALUES (?, ?, ?)""", (color, fil_type, brand))
        # except sqlite3.IntegrityError:
        #     print(f"Filament ({color}, {fil_type}, {brand}) already exists.")
                    
    def _get_part_id(self, part_type, variant, filament_id):
        self.curr.execute("""SELECT Part_ID FROM Parts WHERE (Part_Type = ? AND Part_Variant = ? AND Filament_ID = ?)""", (part_type, variant, filament_id))
        return self.curr.fetchone()
        
    def _enter_part_data(self, part_type, variant, filament_id):
        self.curr.execute("""INSERT INTO Parts (Part_Type, Part_Variant, Filament_ID) VALUES (?, ?, ?)""", (part_type, variant, filament_id))
    
    def _get_item_id(self, item_name):
        self.curr.execute("""SELECT Item_ID FROM Items WHERE Item_Name = ?""", (item_name, ))
        return self.curr.fetchone()
        
    def _enter_item_data(self, item_name, item_group):
        self.curr.execute("""INSERT INTO Items (Item_Name, Group_Name) VALUES (?, ?)""", (item_name, item_group))    
    
    def _find_part_item_relationship(self, item_id, part_id):
        self.curr.execute("""SELECT * FROM BOM WHERE (Item_ID = ? AND Part_ID = ?)""", (item_id, part_id))
        return self.curr.fetchone()
    
    def load_filament_data(self):
        if self.database and self.curr:
            data_path = os.path.join(os.getcwd(), 'Inventory', 'data', 'references', 'filament_data.csv')
            df = pd.read_csv(data_path)
            
            for index, row in df.iterrows():
                color = row.get('Color')
                fil_type = row.get('Type')
                brand = row.get('Brand')

                fil_id = self._get_filament_id(color, fil_type, brand)
                
                if fil_id is None:
                    self._enter_filament_data(color, fil_type, brand)
                    print(f"Added Filament: {color}, {fil_type}, {brand}")
                    
            self.database.commit()    
    
    def load_bom_data(self):
        if self.database and self.curr:
            data_path = os.path.join(os.getcwd(), 'Inventory', 'data', 'references', 'master_bom.csv')
            df = pd.read_csv(data_path)
            
            for index, row in df.iterrows():
                group = row.loc['Group']
                item_name = row.loc['Item']
                part_type = row.loc['Part Type']
                variant = row.loc['Variant']
                color = row.loc['Filament Color']
                fil_type = row.loc['Filament Type']
                fil_brand = row.loc['Filament Brand']
                qty = row.loc['Qty']
                
                item_id = self._get_item_id(item_name)
                if item_id is None:
                    self._enter_item_data(item_name, group)
                    
                
                fil_id = self._get_filament_id(color, fil_type, fil_brand)
                
                if fil_id is not None:
                    part_id = self._get_part_id(part_type, variant, fil_id[0]) 
                    
                    if part_id is None:
                        self._enter_part_data(part_type, variant, fil_id[0])
                        print(f"Added Part: {part_type}, {variant}, {fil_id[0]}")
                else:
                    print(f"Filament not found: {color}, {fil_type}, {fil_brand}")

        self.database.commit()