import os 
import pandas as pd 

class DataLoader:
    def __init__(self, cursor, db):
        self.curr = cursor
        self.database = db

    def ensure_filament(self, color, fil_type, brand):
        self.curr.execute("""SELECT Filament_ID FROM Filament WHERE Filament_Color = ? AND Filament_Type = ? AND Filament_Brand = ?""", (color, fil_type, brand))
        result = self.curr.fetchone()
        if result:
            return result[0]
        else:
            self.curr.execute("""INSERT INTO Filament (Filament_Color, Filament_Type, Filament_Brand) VALUES (?, ?, ?)""", (color, fil_type, brand))
            return self.curr.lastrowid
        
    def ensure_group(self, group_name):
        self.curr.execute("""SELECT Group_ID FROM Groups WHERE GROUP_NAME = ?""", (group_name, ))
        result = self.curr.fetchone()
        if result:
            return result[0]
        else:
            self.curr.execute("""INSERT INTO Groups (Group_Name) VALUES (?)""", (group_name, ))
            print(f"Added Group: {group_name}")
            return self.curr.lastrowid
        
    def ensure_part(self, part_type, variant, filament_id):
        self.curr.execute("""SELECT Part_ID FROM Parts WHERE (Part_Type = ? AND Part_Variant = ? AND Filament_ID = ?)""", (part_type, variant, filament_id))
        result = self.curr.fetchone()
        if result:
            return result[0]
        else:
            self.curr.execute("""INSERT INTO Parts (Part_Type, Part_Variant, Filament_ID) VALUES (?, ?, ?)""", (part_type, variant, filament_id))
            print(f"Added Part: {part_type}, {variant}, {filament_id}")
            return self.curr.lastrowid
        
    def ensure_item(self, item_name, group_id):
        self.curr.execute("""SELECT Item_ID FROM Items WHERE Item_Name = ?""", (item_name,))
        result = self.curr.fetchone()
        if result:
            return result[0]
        else:
            self.curr.execute("""INSERT INTO Items (Item_Name, Group_ID) VALUES (?, ?)""", (item_name, group_id))  
            print(f"Added Item: {item_name}")
            return self.curr.lastrowid
        
    def ensure_item_part(self, item_id, part_id, qty):
        self.curr.execute("""SELECT Item_ID, Part_ID FROM BOM WHERE Item_ID = ? AND Part_ID = ?""", (item_id, part_id))
        result = self.curr.fetchone()
        if result:
            return result[0]
        else:
            self.curr.execute("""INSERT INTO BOM (Item_ID, Part_ID, Qty) VALUES (?, ?, ?)""", (item_id, part_id, qty))
            print(f"Added Item-Part: Item ID {item_id}, Part ID {part_id}, Qty {qty}")
            return self.curr.fetchone()

    def ensure_order_status(self, order_status):
        self.curr.execute("""SELECT Status_ID FROM OrderStatus WHERE Description = ?""", (order_status, ))
        result = self.curr.fetchone()
        if result:
            return result[0]
        else:
            self.curr.execute("""INSERT INTO OrderStatus (Description) VALUES (?)""", (order_status, ))
            return self.curr.lastrowid
    
    def load_filament_data(self):
        if self.database and self.curr:
            data_path = os.path.join(os.getcwd(), 'Inventory', 'data', 'references', 'filament_data.csv')
            df = pd.read_csv(data_path)
            
            for index, row in df.iterrows():
                color = row.get('Color')
                fil_type = row.get('Type')
                brand = row.get('Brand')

                fil_id = self.ensure_filament(color, fil_type, brand)
                    
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

                fil_id = self.ensure_filament(color, fil_type, fil_brand)
                group_id = self.ensure_group(group_name)
                item_id = self.ensure_item(item_name, group_id)
                part_id = self.ensure_part(part_type, variant, fil_id)
                part_item = self.ensure_item_part(item_id, part_id, qty)

    def load_inventory_data(self):
        if self.database and self.curr:
            data_path = os.path.join(os.getcwd(), 'Inventory', 'data', 'references', 'inventory.csv')
            df = pd.read_csv(data_path)

            for index, row in df.iterrows():
                part_id = int(row.loc['Part_ID'])
                qty = int(row.loc['Qty'])

                self.curr.execute("""INSERT INTO Inventory (Part_ID, Qty) VALUES (?, ?)""", (part_id, qty))
    
    def load_order_status_data(self):
        if self.database and self.curr:
            data_path = os.path.join(os.getcwd(), 'Inventory', 'data', 'references', 'order_status_data.csv')
            df = pd.read_csv(data_path)

            for index, row in df.iterrows():
                desc = row.loc['Order_Description']

                order_status_id = self.ensure_order_status(desc)

                

    # def load_item_images(self):
    #     self.curr.execute("""SELECT Item_ID FROM Items""")
    #     item_ids = [item_id[0] for item_id in self.curr.fetchall()]
    #     for item_id in item_ids:
    #         name_format = f"I{item_id}.png"
    #         img_path = os.path.join(self.image_path, name_format)
    #         print(img_path)

    #         self.curr.execute("""UPDATE Items SET Image_Path = ? WHERE Item_ID = ?""", (img_path, item_id))

    #     self.database.commit()