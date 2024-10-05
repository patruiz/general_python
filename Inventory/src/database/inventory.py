class DatabaseInventory:
    def __init__(self, curr):
        self.curr = curr

    def check_part(self, part_id):
        self.curr.execute("""SELECT Qty FROM Inventory WHERE Part_ID = ?""", (part_id,))
        result = self.curr.fetchone()
        return result[0] if result else 0

    def add_part(self, part_id, qty: int):
        stock = self.check_part(part_id)
        if stock == 0:
            self.curr.execute("""INSERT INTO Inventory (Part_ID, Qty) VALUES (?, ?)""", (part_id, qty))
        else: 
            new_qty = stock + qty
            self.curr.execute("""UPDATE Inventory SET Qty = ? WHERE Part_ID = ?""", (new_qty, part_id))

    def remove_part(self, part_id, qty: int):
        stock = self.check_part(part_id)
        if stock == 0:
            print(f"Part ID {part_id} not found in inventory.")
            return
        elif stock < qty:
            print(f"Not enough stock to remove {qty} units of part ID {part_id}.")
            return
        else:
            new_qty = stock - qty
            self.curr.execute("""UPDATE Inventory SET Qty = ? WHERE Part_ID = ?""", (new_qty, part_id))

    def check_item_availability(self, item_id):
        self.curr.execute("""SELECT BOM.Part_ID, BOM.Qty, Inventory.Qty FROM BOM LEFT JOIN Inventory ON BOM.Part_ID = Inventory.Part_ID WHERE BOM.Item_ID = ?""", (item_id,))
        parts = self.curr.fetchall()
        
        for part_id, qty_needed, qty_available in parts:
            qty_available = qty_available if qty_available else 0  
            if qty_needed > qty_available:
                return False  
        
        return True 
