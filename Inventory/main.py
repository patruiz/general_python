import os 
from src.database import Database
from src.inventory import Inventory

def main():
    os.system('cls')
    ass = Database(os.path.join(os.getcwd(), 'Inventory', 'data', 'swag.db'))

    ass.database_connect()
    ass.create_tables()
    ass.load_data()

    inv = Inventory(ass)
    needtobuyswag = inv.get_parts((1, 3))
    inv.check_inventory(needtobuyswag)
    # inv.get_parts((1, 3))


if __name__ == "__main__":
    main()