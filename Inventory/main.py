import os 
# from src.database import DatabaseConnection, DatabaseSchema, DataLoader, DatabaseQueries

from src.database import Database
# from src.inventory import Inventory

def main():
    os.system('cls')
    # os.system('clear')

    ass = Database(os.path.join(os.getcwd(), 'Inventory', 'data', 'swag.db'))

    ass.database_connect()
    ass.create_tables()

    ass.load_filament_data()
    ass.load_bom_data()
    ass.load_item_images()

    ass.view_image("1")

    # ass.show_changelog()

# def main():
#     os.system('cls')

#     db_path = os.path.join(os.getcwd(), 'Inventory', 'data', 'swag.db')
#     db_connection = DatabaseConnection(db_path)
#     db_connection.connect()

#     db_schema = DatabaseSchema(db_connection.cursor)
#     db_schema.create_tables()

#     db_loader = DataLoader(db_connection.cursor, db_connection)
#     db_loader.load_filament_data()

#     db_queries = DatabaseQueries(db_connection.cursor)
#     db_queries._get_group_id('Swag')

#     db_connection.disconnect()
    

if __name__ == "__main__":
    main()