class DatabaseSchema:
    def __init__(self, cursor):
        self.curr = cursor

    def create_tables(self):
        # Groups Table
        self.curr.execute(
            """
            CREATE TABLE IF NOT EXISTS Groups(
            Group_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Group_Name TEXT UNIQUE NOT NULL
            )
            """
        )

        # Filament Table
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
        
        # Items Table
        self.curr.execute(
            """
            CREATE TABLE IF NOT EXISTS Items(
            Item_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Item_Name TEXT UNIQUE NOT NULL,
            Group_ID INTEGER NOT NULL,
            Image_Path TEXT,
            FOREIGN KEY (Group_ID) REFERENCES Groups(Group_ID)
            )
            """
        )
        
        # Parts Table
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
        
        # BOM Table
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

        # Inventory Table
        self.curr.execute(
            """
            CREATE TABLE IF NOT EXISTS Inventory(
            Part_ID INTEGER PRIMARY KEY NOT NULL, 
            Qty INTEGER NOT NULL,
            FOREIGN KEY (Part_ID) REFERENCES Parts(Part_ID)
            )
            """
        )

        # Orders Table
        self.curr.execute(
            """
            CREATE TABLE IF NOT EXISTS Orders(
            Order_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Customer_ID INTEGER NOT NULL, 
            Start_Date DATE NOT NULL,
            End_Date DATE, 
            Status TEXT NOT NULL,
            FOREIGN KEY (Status) REFERENCES OrderStatus(Description)
            )
            """
        )

        # Order Items Table
        self.curr.execute(
            """
            CREATE TABLE IF NOT EXISTS OrderItems(
            Order_ID INTEGER NOT NULL, 
            Item_ID INTEGER NOT NULL,
            Qty INTEGER NOT NULL, 
            PRIMARY KEY (Order_ID, Item_ID)
            FOREIGN KEY (Item_ID) REFERENCES Items(Item_ID), 
            FOREIGN KEY (Order_ID) REFERENCES Orders(Order_ID)
            )
            """
        )

        # Order Financials Table
        self.curr.execute(
            """
            CREATE TABLE IF NOT EXISTS OrderFinancials(
            Order_ID INTEGER PRIMARY KEY NOT NULL,
            Subtotal REAL, 
            Discount REAL,
            Tax REAL, 
            Total REAL,
            FOREIGN KEY (Order_ID) REFERENCES Orders(Order_ID)
            )
            """
        )

        # Order Status Table
        self.curr.execute(
            """                    
            CREATE TABLE IF NOT EXISTS OrderStatus(
            Status_ID INTEGER PRIMARY KEY AUTOINCREMENT, 
            Description TEXT NOT NULL UNIQUE
            )
            """
        )