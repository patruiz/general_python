import os 
from src.database import Database
from src.inventory import Inventory

def main():
    os.system('cls')
    # os.system('clear')

    ass = Database(os.path.join(os.getcwd(), 'Inventory', 'data', 'swag.db'))

    ass.database_connect()
    ass.create_tables()

    # ass.load_filament_data()
    # ass.load_bom_data()
    # ass.load_item_images()

    # ass.view_image("1")

    # ass.show_changelog()
    
    

if __name__ == "__main__":
    main()