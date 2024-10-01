class DatabaseOrders:
    def __init__(self, curr):
        self.curr = curr

    def create_order(self, customer_id, start_date, status = 1):
        self.curr.execute("""INSERT INTO Orders (Start_Date, Customer_ID, Status) VALUES (?, ?, ?)""", (start_date, customer_id, status))
        return self.curr.lastrowid
    
    def add_item_to_order(self, order_id, item_id, quantity):
        self.curr.execute("""INSERT INTO OrderItems (Order_ID, Item_ID, Qty) VALUES (?, ?, ?)""", (order_id, item_id, quantity))

    def update_order_status(self, order_id, status = None):
        if status:
            self.curr.execute("""SELECT Status_ID FROM OrderStatus WHERE Description = ?""", (status, ))
            response = self.curr.fetchone()[0]
            if response is None:
                raise ValueError
            else:
                self.curr.execute("""UPDATE Orders SET Status = ? WHERE Order_ID = ?""", (response, order_id))
        else:
            self.curr.execute("""SELECT Status FROM Orders WHERE Order_ID = ?""", (order_id, ))
            status_id = int(self.curr.fetchone()[0]) + 1
            self.curr.execute("""UPDATE Orders SET Status = ? WHERE Order_ID = ?""", (status_id, order_id))


    def calc_order_total(self):
        pass

    def get_order_details(self):
        pass

