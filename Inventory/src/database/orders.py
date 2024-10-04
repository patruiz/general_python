class DatabaseOrders:
    def __init__(self, curr):
        self.curr = curr

    def create_order(self, customer_id, start_date, status = 1):
        self.curr.execute("""INSERT INTO Orders (Start_Date, Customer_ID, Status) VALUES (?, ?, ?)""", (start_date, customer_id, status))
        return self.curr.lastrowid
    
    def add_item_to_order(self, order_id, item_id, quantity):
        try:
            self.curr.execute("""INSERT INTO OrderItems (Order_ID, Item_ID, Qty) VALUES (?, ?, ?)""", (order_id, item_id, quantity))
        except:
            raise ValueError 

    def update_order_status(self, order_id, status = None):
        if status:
            print(status)
            if not isinstance(status, int):
                print(status)
                self.curr.execute("""SELECT Status_ID FROM OrderStatus WHERE Description = ?""", (status, ))
                status_id = self.curr.fetchone()[0]
            else:
                status_id = status
        else:
            self.curr.execute("""SELECT Status FROM Orders WHERE Order_ID = ?""", (order_id, ))
            status_id = self.curr.fetchone()[0]
            status_id = int(status_id) + 1

        self.curr.execute("""UPDATE Orders SET Status = ? WHERE Order_ID = ?""", (status_id, order_id))

    def get_order_details(self, order_id):
        self.curr.execute("""SELECT * FROM Orders""")
        order_list = [orders[0] for orders in self.curr.fetchall()]
        if order_id in order_list:
            self.curr.execute("""SELECT Orders.Order_ID, Orders.Start_Date, Orders.Status, OrderItems.Item_ID, OrderItems.Qty FROM Orders LEFT JOIN OrderItems ON Orders.Order_ID = OrderItems.Order_ID WHERE Orders.Order_ID = ?""", (order_id, ))
            for response in self.curr.fetchall():
                print(f"OrderID: {response[0]} - StartDate: {response[1]} - Status: {response[2]} - ItemID: {response[3]} - Qty: {response[4]}")
        else:
            pass


    def calc_order_total(self):
        pass