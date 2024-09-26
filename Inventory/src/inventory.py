

class Inventory:
    def __init__(self, db):
        self.db = db

    # def add_inventory(self, val):
    #      self.db.curr.execute("""UPDATE Inventory SET Qty = (?) WHERE Part_ID = (?)""", (val, ) )

    def get_parts(self, order: tuple):
        try: 
            item, qty = int(order[0]), int(order[1])
            self.db.curr.execute("""SELECT Part_ID, Qty FROM BOM WHERE Item_ID = (?)""", (item, ))
            parts = [[i[0], i[1]*qty] for i in self.db.curr.fetchall()]
        except:
                pass
        
        print(f"from get_parts: {parts}")
        return parts
    
    def new_item(self):
         pass
    
    





