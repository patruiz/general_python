import os 
from src.database import DatabaseConnection, DatabaseSchema, DataLoader, DatabaseQueries, DatabaseOrders

def main():
    os.system('cls')

    db_path = os.path.join(os.getcwd(), 'Inventory', 'data', 'swag.db')
    db_connection = DatabaseConnection(db_path)
    db_connection.connect()

    db_schema = DatabaseSchema(db_connection.cursor)
    db_schema.create_tables()

    db_loader = DataLoader(db_connection.cursor, db_connection)
    db_loader.load_filament_data()
    db_loader.load_bom_data()
    # db_loader.load_inventory_data()
    db_loader.load_order_status_data()

    db_queries = DatabaseQueries(db_connection.cursor)
    # butthole = db_queries.get_parts_per_item(2)
    # print(butthole)

    db_orders = DatabaseOrders(db_connection.cursor)
    # db_orders.create_order(1, '01-Oct-24')
    db_orders.add_item_to_order(1, 1, 3)
    




    db_connection.disconnect()
    

if __name__ == "__main__":
    main()