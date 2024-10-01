class DatabaseQueries:
    def __init__(self, cursor):
        self.curr = cursor 

    def get_parts_per_item(self, item_id):
        response = []
        self.curr.execute("""SELECT Part_ID, Qty FROM BOM WHERE Item_ID = ?""", (item_id, ))
        for i in self.curr.fetchall():
            response.append([i[0], i[1]])
        return response
    
    def get_fil_per_item(self, item_id):
        self.curr.execute("""SELECT Parts.Filament_ID FROM BOM INNER JOIN Parts ON BOM.Part_ID = Parts.Part_ID WHERE BOM.Item_ID = ?""", (item_id,))
        return list(set([filament[0] for filament in self.curr.fetchall()]))