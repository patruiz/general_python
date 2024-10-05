import os
from src.database import DatabaseConnection, DatabaseSchema, DataLoader, DatabaseQueries, DatabaseOrders, DatabaseInventory

def main():
    os.system('cls' if os.name == 'nt' else 'clear') 

    db_path = os.path.join(os.getcwd(), 'Inventory', 'data', 'swag.db')
    db_connection = DatabaseConnection(db_path)
    db_connection.connect()

    db_schema = DatabaseSchema(db_connection.cursor)
    db_loader = DataLoader(db_connection.cursor, db_connection)
    db_queries = DatabaseQueries(db_connection.cursor)
    db_orders = DatabaseOrders(db_connection.cursor)
    db_inventory = DatabaseInventory(db_connection.cursor)

    # Uncomment this line to (re)create tables - only do this when necessary!
    # db_schema.create_tables()

    # Uncomment the following lines to load data if required
    # db_loader.load_filament_data()
    # db_loader.load_bom_data()
    # db_loader.load_inventory_data()
    # db_loader.load_order_status_data()

    # Interactive Menu
    while True:
        print("\n--- Database Test Menu ---")
        print("1. Create Order")
        print("2. Add Item to Order")
        print("3. Update Order Status")
        print("4. Get Order Details")
        print("5. Add Part to Inventory")
        print("6. Remove Part from Inventory")
        print("7. Check Item Availability")
        print("8. Exit")
        
        choice = input("Select an option (1-8): ").strip()

        try:
            if choice == '1':
                customer_id = int(input("Enter Customer ID: "))
                start_date = input("Enter Start Date (e.g., 01-Oct-24): ")
                order_id = db_orders.create_order(customer_id, start_date)
                print(f"Order created with ID: {order_id}")

            elif choice == '2':
                order_id = int(input("Enter Order ID: "))
                item_id = int(input("Enter Item ID: "))
                quantity = int(input("Enter Quantity: "))
                db_orders.add_item_to_order(order_id, item_id, quantity)
                print(f"Added Item {item_id} to Order {order_id} with Quantity {quantity}")

            elif choice == '3':
                order_id = int(input("Enter Order ID: "))
                status = input("Enter Status (ID or Description): ")
                try:
                    if status.isdigit():
                        db_orders.update_order_status(order_id, int(status))
                    else:
                        db_orders.update_order_status(order_id, status)
                    print(f"Order {order_id} status updated.")
                except ValueError as e:
                    print(f"Error: {e}")

            elif choice == '4':
                order_id = int(input("Enter Order ID: "))
                order_details = db_orders.get_order_details(order_id)
                print(f"Order Details for Order ID {order_id}: {order_details}")

            elif choice == '5':
                part_id = int(input("Enter Part ID: "))
                quantity = int(input("Enter Quantity to Add: "))
                db_inventory.add_part(part_id, quantity)
                print(f"Added {quantity} units of Part ID {part_id} to inventory.")

            elif choice == '6':
                part_id = int(input("Enter Part ID: "))
                quantity = int(input("Enter Quantity to Remove: "))
                db_inventory.remove_part(part_id, quantity)
                print(f"Removed {quantity} units of Part ID {part_id} from inventory.")

            elif choice == '7':
                item_id = int(input("Enter Item ID: "))
                available = db_inventory.check_item_availability(item_id)
                if available:
                    print(f"Item ID {item_id} is available in inventory.")
                else:
                    print(f"Item ID {item_id} is NOT available in inventory.")

            elif choice == '8':
                print("Exiting the database test program.")
                break

            else:
                print("Invalid option. Please choose a number between 1 and 8.")

        except Exception as e:
            print(f"An error occurred: {e}")

    # Close database connection
    db_connection.disconnect()

if __name__ == "__main__":
    main()
