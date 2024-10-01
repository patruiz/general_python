class DatabaseOrders:
    def __init__(self, curr):
        self.curr = curr

    def create_order(self, customer_id, start_date, status):
        self.curr.execute("""INSERT INTO Orders (Start_Date, Customer_ID, Status) VALUES (?, ?, ?)""", (start_date, customer_id, status))
        return self.curr.lastrowid
    
    def add_item_to_order(self, order_id, item_id, quantity):
        self.curr.execute("""INSERT INTO OrderItems (Order_ID, Item_ID, Qty) VALUES (?, ?, ?)""", (order_id, item_id, quantity))

    def update_order_status(self, order_id, status_name):
        
        pass

    def calc_order_total(self):
        pass

    def get_order_details(self):
        pass

