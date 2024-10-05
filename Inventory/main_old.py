import os 
from src.database import DatabaseConnection, DatabaseSchema, DataLoader, DatabaseQueries, DatabaseOrders, DatabaseInventory, DatabaseOperations

def main():
    os.system('cls')

    db_path = os.path.join(os.getcwd(), 'Inventory', 'data', 'swag.db')
    db_connection = DatabaseConnection(db_path)
    db_connection.connect()

    db_schema = DatabaseSchema(db_connection.cursor)
    # db_schema.create_tables()

    db_loader = DataLoader(db_connection.cursor, db_connection)
    # db_loader.load_filament_data()
    # db_loader.load_bom_data()
    # db_loader.load_inventory_data()
    # db_loader.load_order_status_data()

    db_queries = DatabaseQueries(db_connection.cursor)
    # butthole = db_queries.get_parts_per_item(2)
    # print(butthole)

    db_orders = DatabaseOrders(db_connection.cursor)
    # db_orders.create_order(1, '01-Oct-24')
    # db_orders.add_item_to_order(1, 2, 1)

    db_orders.update_order_status(1, 1)
    print(db_orders.get_order_details(1))

    db_inventory = DatabaseInventory(db_connection.cursor)
    # db_inventory.add_part_to_inventory(1, 5)
    # db_inventory.remove_part_from_inventory(1, 1)
    # db_inventory.check_item_availability(1)




    db_connection.disconnect()

    

if __name__ == "__main__":
    main()