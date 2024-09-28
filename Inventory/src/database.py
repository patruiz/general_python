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
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def database_disconnect(self):
        if self.database:
            self.database.commit()
            self.curr.close()
            self.database.close()
            self.database = None
            self.curr = None
            
    def show_changelog(self):
        print(self.change_log)

    def create_tables(self):
        if self.database and self.curr:
            self.curr.execute(
                """
                CREATE TABLE IF NOT EXISTS Groups(
                Group_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Group_Name TEXT UNIQUE NOT NULL
                )
                """
            )
            
            self.curr.execute(
                """
                CREATE TABLE IF NOT EXISTS Items(
                Item_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Item_Name TEXT UNIQUE NOT NULL,
                Group_ID INTEGER NOT NULL,
                FOREIGN KEY (Group_ID) REFERENCES Groups(Group_ID)
                )
                """
            )
            
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

    def _get_filament_id(self, color, fil_type, brand):
        self.curr.execute("""SELECT Filament_ID FROM Filament WHERE Filament_Color = ? AND Filament_Type = ? AND Filament_Brand = ?""", (color, fil_type, brand))
        return self.curr.fetchone()

    def _get_group_id(self, group_name):
        self.curr.execute("""SELECT Group_ID FROM Groups WHERE Group_Name = ?""", (group_name,))
        return self.curr.fetchone()

    def _enter_group(self, group_name):
        try:
            self.curr.execute("""INSERT INTO Groups (Group_Name) VALUES (?)""", (group_name,))
            print(f"Added Group: {group_name}")
        except sqlite3.IntegrityError:
            print(f"Group '{group_name}' already exists.")

    def _enter_filament_data(self, color, fil_type, brand):
        try:
            self.curr.execute("""INSERT INTO Filament (Filament_Color, Filament_Type, Filament_Brand) VALUES (?, ?, ?)""", (color, fil_type, brand))
            print(f"Added Filament: {color}, {fil_type}, {brand}")
        except sqlite3.IntegrityError:
            print(f"Filament ({color}, {fil_type}, {brand}) already exists.")
                    
    def _get_part_id(self, part_type, variant, filament_id):
        self.curr.execute("""SELECT Part_ID FROM Parts WHERE (Part_Type = ? AND Part_Variant = ? AND Filament_ID = ?)""", (part_type, variant, filament_id))
        return self.curr.fetchone()
        
    def _enter_part(self, part_type, variant, filament_id):
        try:
            self.curr.execute("""INSERT INTO Parts (Part_Type, Part_Variant, Filament_ID) VALUES (?, ?, ?)""", (part_type, variant, filament_id))
            print(f"Added Part: {part_type}, {variant}, {filament_id}")
        except sqlite3.IntegrityError:
            print(f"Part ({part_type}, {variant}, {filament_id}) already exists.")

    def _get_item_id(self, item_name):
        self.curr.execute("""SELECT Item_ID FROM Items WHERE Item_Name = ?""", (item_name,))
        return self.curr.fetchone()
        
    def _enter_item(self, item_name, group_id):
        try:
            self.curr.execute("""INSERT INTO Items (Item_Name, Group_ID) VALUES (?, ?)""", (item_name, group_id))    
            print(f"Added Item: {item_name} to group ID {group_id}")
        except sqlite3.IntegrityError:
            print(f"Item '{item_name}' already exists.")

    def _get_item_part(self, item_id, part_id):
        self.curr.execute("""SELECT Item_ID, Part_ID FROM BOM WHERE Item_ID = ? AND Part_ID = ?""", (item_id, part_id))
        return self.curr.fetchone()
    
    def _enter_item_part(self, item_id, part_id, qty):
        self.curr.execute("""INSERT INTO BOM (Item_ID, Part_ID, Qty) VALUES (?, ?, ?)""", (item_id, part_id, qty))
        print(f"Added Item-Part: Item ID {item_id}, Part ID {part_id}, Qty {qty}")

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
                    
            self.database.commit()    

    def load_bom_data(self):
        if self.database and self.curr:
            data_path = os.path.join(os.getcwd(), 'Inventory', 'data', 'references', 'master_bom.csv')
            df = pd.read_csv(data_path)
            
            for index, row in df.iterrows():
                group_name = row['Group']
                item_name = row['Item']
                part_type = row['Part Type']
                variant = row['Variant']
                color = row['Filament Color']
                fil_type = row['Filament Type']
                fil_brand = row['Filament Brand']
                qty = row['Qty']

                fil_id = self._get_filament_id(color, fil_type, fil_brand)

                group_id = self._get_group_id(group_name)[0]
                if group_id is None:
                    self._enter_group(group_name)
                    group_id = self._get_group_id(group_name)[0]
                
                item_id = self._get_item_id(item_name)[0]
                if item_id is None:
                    self._enter_item(item_name, group_id)
                    item_id = self._get_item_id(item_name)[0]
                
                print(item_id)
                break
                part_id = self._get_part_id(part_type, variant, fil_id[0])
                if part_id is None:
                    self._enter_part(part_type, variant, fil_id[0])
                    part_id = self._get_part_id(part_type, variant, fil_id[0])[0]
                
                if self._get_item_part(item_id, part_id) is None:
                    self._enter_item_part(item_id, part_id, qty)
                
            self.database.commit()
