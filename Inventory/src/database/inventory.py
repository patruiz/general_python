
class DatabaseInventory:
    def __init__(self, curr):
        self.curr = curr

    def check_part(self, part_id):
        self.curr.execute("""SELECT (Qty) FROM Inventory WHERE Part_ID = ?""", (part_id, ))
        return self.curr.fetchone()[0]

    def add_part(self, part_id, qty: int):
        stock = self.check_part(part_id)
        print(f"checking: {stock}")
        if stock is None:
            self.curr.execute("""INSERT INTO Inventory (Part_ID, Qty) VALUES (?, ?)""", (part_id, qty))
        else:
            new_qty = stock + qty
            self.curr.execute("""UPDATE Inventory SET Qty = ? WHERE Part_ID = ?""", (new_qty, part_id))

        print(f"final: {self.check_part(part_id)}")

    def remove_part(self, part_id, qty: int):
        stock = self.check_part(part_id)
        print(f"remove checking: {stock}") 
        if (stock is None):
            pass
        elif stock is not None:
            diff = stock - qty
            if diff < 0:
                raise ValueError
            elif (diff == 0) or (diff > 0):
                new_qty = diff 
                self.curr.execute("""UPDATE Inventory SET Qty = ? WHERE Part_ID = ?""", (new_qty, part_id))
                print(f"removing final qty: {new_qty}")


    def remove_item(self):
        pass
    # use get_parts_per_item function from queries to get the list of all the parts that feed into an item to determine if you have enough inventory to create an item 
    