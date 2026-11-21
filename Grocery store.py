"""
Smart Grocery Store Management System
-------------------------------------
Manages products, stock, customer sales and store reports
using lists and dictionaries as the main data structures.
"""

# ---------------------------------------------------------------
# Data storage
# ---------------------------------------------------------------
# List of dictionaries holding every product in the store
products = [
    {"id": 101, "name": "Milk", "category": "Dairy", "price": 250, "stock": 20},
    {"id": 102, "name": "Bread", "category": "Bakery", "price": 120, "stock": 15},
    {"id": 103, "name": "Eggs (Dozen)", "category": "Dairy", "price": 380, "stock": 4},
]

# Separate list of dictionaries holding completed sales
sales_records = []

LOW_STOCK_LIMIT = 5  # products below this quantity are flagged in the report


# ---------------------------------------------------------------
# Input helper functions (validation)
# ---------------------------------------------------------------
def get_int(prompt, minimum=0):
    """Keep asking until the user enters a whole number >= minimum."""
    while True:
        value = input(prompt).strip()
        try:
            number = int(value)
        except ValueError:
            print("  Invalid input. Please enter a whole number.")
            continue
        if number < minimum:
            print(f"  Value must be at least {minimum}.")
            continue
        return number


def get_float(prompt, minimum=0.0):
    """Keep asking until the user enters a number >= minimum."""
    while True:
        value = input(prompt).strip()
        try:
            number = float(value)
        except ValueError:
            print("  Invalid input. Please enter a number.")
            continue
        if number < minimum:
            print(f"  Value must be at least {minimum}.")
            continue
        return number


def get_text(prompt):
    """Keep asking until the user enters non-empty text."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  This field cannot be empty.")


# ---------------------------------------------------------------
# Product helper functions
# ---------------------------------------------------------------
def find_product_by_id(product_id):
    """Return the product dictionary with the given ID, or None."""
    for product in products:
        if product["id"] == product_id:
            return product
    return None


def print_product(product):
    """Print the complete details of one product."""
    print(f"  ID       : {product['id']}")
    print(f"  Name     : {product['name']}")
    print(f"  Category : {product['category']}")
    print(f"  Price    : {product['price']:.2f}")
    print(f"  Stock    : {product['stock']}")


# ---------------------------------------------------------------
# 1. Add New Product
# ---------------------------------------------------------------
def add_product():
    print("\n--- Add New Product ---")
    product_id = get_int("Enter Product ID: ", minimum=1)

    # Prevent duplicate product IDs
    if find_product_by_id(product_id) is not None:
        print("  Error: A product with this ID already exists.")
        return

    name = get_text("Enter Product Name: ")
    category = get_text("Enter Category: ")
    price = get_float("Enter Price: ", minimum=0.01)
    stock = get_int("Enter Available Stock: ", minimum=0)

    # Store the product as a dictionary and append it to the list
    new_product = {
        "id": product_id,
        "name": name,
        "category": category,
        "price": price,
        "stock": stock,
    }
    products.append(new_product)
    print(f"  Product '{name}' added successfully.")


# ---------------------------------------------------------------
# 2. View All Products
# ---------------------------------------------------------------
def view_products():
    print("\n--- All Products ---")
    if not products:
        print("  No products available.")
        return

    print(f"{'ID':<8}{'Name':<22}{'Category':<15}{'Price':>10}{'Stock':>8}")
    print("-" * 63)
    for product in products:  # loop through every product record
        print(
            f"{product['id']:<8}{product['name']:<22}{product['category']:<15}"
            f"{product['price']:>10.2f}{product['stock']:>8}"
        )


# ---------------------------------------------------------------
# 3. Search Product
# ---------------------------------------------------------------
def search_product():
    print("\n--- Search Product ---")
    query = get_text("Enter Product ID or Name: ")
    matches = []

    for product in products:
        # Match by ID if the query is numeric, otherwise by name
        if query.isdigit() and product["id"] == int(query):
            matches.append(product)
        elif query.lower() in product["name"].lower():
            matches.append(product)

    if not matches:
        print("  Product not found.")
        return

    print(f"  {len(matches)} product(s) found:")
    for product in matches:
        print("  " + "-" * 25)
        print_product(product)


# ---------------------------------------------------------------
# 4. Update Product Stock
# ---------------------------------------------------------------
def update_stock():
    print("\n--- Update Product Stock ---")
    product_id = get_int("Enter Product ID: ", minimum=1)
    product = find_product_by_id(product_id)

    if product is None:
        print("  Product not found.")
        return

    print(f"  Current stock of {product['name']}: {product['stock']}")
    print("  1. Add stock")
    print("  2. Set new quantity")
    option = input("  Choose option (1/2): ").strip()

    if option == "1":
        quantity = get_int("  Enter quantity to add: ", minimum=1)
        product["stock"] += quantity
    elif option == "2":
        product["stock"] = get_int("  Enter new stock quantity: ", minimum=0)
    else:
        print("  Invalid option. No changes made.")
        return

    print(f"  Updated stock of {product['name']}: {product['stock']}")


# ---------------------------------------------------------------
# 5. Process Customer Sale
# ---------------------------------------------------------------
def process_sale():
    print("\n--- Process Customer Sale ---")
    product_id = get_int("Enter Product ID: ", minimum=1)
    product = find_product_by_id(product_id)

    if product is None:
        print("  Product not found.")
        return

    if product["stock"] == 0:
        print(f"  Sorry, {product['name']} is out of stock.")
        return

    quantity = get_int(f"Enter quantity (available: {product['stock']}): ", minimum=1)

    # Do not allow a sale larger than the available stock
    if quantity > product["stock"]:
        print(f"  Sale denied. Only {product['stock']} unit(s) in stock.")
        return

    total = quantity * product["price"]
    product["stock"] -= quantity  # deduct purchased quantity

    # Record the completed sale in the separate sales list
    sales_records.append(
        {
            "id": product["id"],
            "name": product["name"],
            "quantity": quantity,
            "total": total,
        }
    )

    print("\n  ===== PURCHASE SUMMARY =====")
    print(f"  Product        : {product['name']}")
    print(f"  Unit Price     : {product['price']:.2f}")
    print(f"  Quantity       : {quantity}")
    print(f"  Total Amount   : {total:.2f}")
    print(f"  Remaining Stock: {product['stock']}")


# ---------------------------------------------------------------
# 6. View Sales Records
# ---------------------------------------------------------------
def view_sales():
    print("\n--- Sales Records ---")
    if not sales_records:
        print("  No sales recorded yet.")
        return

    print(f"{'ID':<8}{'Name':<22}{'Qty Sold':>10}{'Total Amount':>16}")
    print("-" * 56)
    for sale in sales_records:
        print(
            f"{sale['id']:<8}{sale['name']:<22}{sale['quantity']:>10}"
            f"{sale['total']:>16.2f}"
        )


# ---------------------------------------------------------------
# 7. Generate Store Report
# ---------------------------------------------------------------
def generate_report():
    print("\n==================================")
    print("          STORE REPORT")
    print("==================================")

    # Totals calculated with loops over the lists
    total_stock = 0
    for product in products:
        total_stock += product["stock"]

    total_revenue = 0
    for sale in sales_records:
        total_revenue += sale["total"]

    print(f"Total number of products   : {len(products)}")
    print(f"Total available stock      : {total_stock}")
    print(f"Total sales transactions   : {len(sales_records)}")
    print(f"Total revenue generated    : {total_revenue:.2f}")

    # Products with stock below the low-stock limit
    print(f"\nProducts with stock below {LOW_STOCK_LIMIT} units:")
    low_stock_found = False
    for product in products:
        if product["stock"] < LOW_STOCK_LIMIT:
            print(f"  - {product['name']} (ID {product['id']}): {product['stock']} left")
            low_stock_found = True
    if not low_stock_found:
        print("  None")

    # Highest and lowest priced products
    if products:
        highest = products[0]
        lowest = products[0]
        for product in products:
            if product["price"] > highest["price"]:
                highest = product
            if product["price"] < lowest["price"]:
                lowest = product
        print(f"\nHighest priced product: {highest['name']} ({highest['price']:.2f})")
        print(f"Lowest priced product : {lowest['name']} ({lowest['price']:.2f})")
    else:
        print("\nNo products available for price comparison.")


# ---------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------
def show_menu():
    print("\n====================================")
    print("SMART GROCERY STORE SYSTEM")
    print("====================================\n")
    print("1. Add New Product")
    print("2. View All Products")
    print("3. Search Product")
    print("4. Update Product Stock")
    print("5. Process Customer Sale")
    print("6. View Sales Records")
    print("7. Generate Store Report")
    print("8. Exit\n")


def main():
    # Map menu choices to their functions
    actions = {
        "1": add_product,
        "2": view_products,
        "3": search_product,
        "4": update_stock,
        "5": process_sale,
        "6": view_sales,
        "7": generate_report,
    }

    while True:  # runs until the user chooses Exit
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "8":
            print("\nThank you for using the Smart Grocery Store System. Goodbye!")
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("  Invalid choice. Please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()