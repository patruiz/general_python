

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

    def check_inventory(self, parts_list):
        avail, notAvail = [], []

        for part in parts_list:
            print(part[0])
            self.db.curr.execute("""SELECT Qty FROM Inventory WHERE Part_ID = (?)""", (part[0], ))
            print(self.db.curr.fetchone()[0])


        #     new_parts = {}
        # except:
        #     pass

        # parts = parts.update(new_parts)




