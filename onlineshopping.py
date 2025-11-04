"""
Online Shopping Application - Simplified Version
For Information System Students

This app demonstrates:
- Unit Testing: Test one function at a time
- Integration Testing: Test functions working together
- System Testing: Test complete shopping process
"""


class ShoppingCart:
    """Shopping cart to store items"""
    
    def __init__(self):
        self.items = []  # List to store items
    
    def add_item(self, name, price, quantity):
        """Add an item to cart"""
        if price < 0:
            raise ValueError("Price cannot be negative")
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        item = {
            'name': name,
            'price': price,
            'quantity': quantity
        }
        self.items.append(item)
    
    def get_items(self):
        """Get all items in cart"""
        return self.items


# ========================================
# PART 1: UNIT TESTABLE FUNCTIONS
# Test these functions one by one
# ========================================

def calculate_item_total(price, quantity):
    """
    Calculate total for one item
    Example: price=100000, quantity=2 -> 200000
    """
    if price < 0:
        raise ValueError("Price cannot be negative")
    if quantity <= 0:
        raise ValueError("Quantity must be positive")
    
    total = price * quantity
    return total


def calculate_subtotal(items):
    """
    Calculate subtotal of all items
    Example: 3 items -> add all their totals
    """
    if not items:
        return 0
    
    subtotal = 0
    for item in items:
        item_total = item['price'] * item['quantity']
        subtotal = subtotal + item_total
    
    return subtotal


def apply_discount(subtotal, discount_code=None):
    """
    Apply discount to subtotal
    
    Discount Codes:
    - SAVE10 = 10% off
    - SAVE20 = 20% off
    - SAVE30 = 30% off
    
    Auto discount (no code):
    - >= 15,000,000 = 15% off
    - >= 7,500,000 = 10% off
    - >= 3,000,000 = 5% off
    """
    if subtotal < 0:
        raise ValueError("Subtotal cannot be negative")
    
    discount_percent = 0
    
    # Check if user has discount code
    if discount_code:
        code = discount_code.upper()
        if code == "SAVE10":
            discount_percent = 10
        elif code == "SAVE20":
            discount_percent = 20
        elif code == "SAVE30":
            discount_percent = 30
    else:
        # Auto discount based on total
        if subtotal >= 15_000_000:
            discount_percent = 15
        elif subtotal >= 7_500_000:
            discount_percent = 10
        elif subtotal >= 3_000_000:
            discount_percent = 5
    
    discount_amount = subtotal * discount_percent / 100
    return discount_amount, discount_percent


def calculate_shipping(subtotal_after_discount, location="local"):
    """
    Calculate shipping cost
    
    Rules:
    - FREE if total >= 7,500,000
    - Local = 75,000
    - National = 225,000
    - International = 750,000
    """
    if subtotal_after_discount < 0:
        raise ValueError("Subtotal cannot be negative")
    
    # Free shipping for big orders
    if subtotal_after_discount >= 7_500_000:
        return 0
    
    location = location.lower()
    
    if location == "local":
        return 75_000
    elif location == "national":
        return 225_000
    elif location == "international":
        return 750_000
    else:
        raise ValueError("Invalid location")


def calculate_tax(subtotal_after_discount, tax_rate=0.10):
    """
    Calculate tax (default 10%)
    Example: 1,000,000 x 10% = 100,000
    """
    if subtotal_after_discount < 0:
        raise ValueError("Subtotal cannot be negative")
    if tax_rate < 0 or tax_rate > 1:
        raise ValueError("Tax rate must be between 0 and 1")
    
    tax = subtotal_after_discount * tax_rate
    return tax


# ========================================
# PART 2: INTEGRATION FUNCTION
# This combines multiple functions together
# ========================================

def calculate_order(items, discount_code=None, location="local", tax_rate=0.10):
    """
    Calculate complete order total
    
    Steps:
    1. Calculate subtotal
    2. Apply discount
    3. Calculate shipping
    4. Calculate tax
    5. Get final total
    """
    # Step 1: Subtotal
    subtotal = calculate_subtotal(items)
    
    # Step 2: Discount
    discount_amount, discount_percent = apply_discount(subtotal, discount_code)
    subtotal_after_discount = subtotal - discount_amount
    
    # Step 3: Shipping
    shipping = calculate_shipping(subtotal_after_discount, location)
    
    # Step 4: Tax
    tax = calculate_tax(subtotal_after_discount, tax_rate)
    
    # Step 5: Final total
    final_total = subtotal_after_discount + shipping + tax
    
    # Return all details
    result = {
        "subtotal": subtotal,
        "discount_amount": discount_amount,
        "discount_percent": discount_percent,
        "subtotal_after_discount": subtotal_after_discount,
        "shipping": shipping,
        "tax": tax,
        "final_total": final_total
    }
    
    return result


# ========================================
# PART 3: SYSTEM FUNCTION
# Complete purchase from start to finish
# ========================================

def complete_purchase(cart, discount_code=None, location="local", tax_rate=0.10):
    """
    Complete the entire purchase process
    
    This is the MAIN function that does everything:
    1. Check cart is not empty
    2. Calculate order totals
    3. Create payment summary
    """
    # Check cart has items
    if not cart.items:
        raise ValueError("Cart is empty")
    
    # Calculate order
    order = calculate_order(cart.items, discount_code, location, tax_rate)
    
    # Create summary
    summary = {
        "items": cart.items,
        "subtotal": order["subtotal"],
        "discount": order["discount_amount"],
        "shipping": order["shipping"],
        "tax": order["tax"],
        "total": order["final_total"],
        "status": "Success"
    }
    
    return summary


def print_summary(summary):
    """Print payment summary nicely"""
    print("\n" + "=" * 50)
    print("PAYMENT SUMMARY")
    print("=" * 50)
    
    print("\nITEMS:")
    for item in summary['items']:
        total = item['price'] * item['quantity']
        print(f"  {item['name']}: Rp {item['price']:,} x {item['quantity']} = Rp {total:,}")
    
    print(f"\nSubtotal: Rp {summary['subtotal']:,}")
    
    if summary['discount'] > 0:
        print(f"Discount: -Rp {summary['discount']:,}")
    
    print(f"Shipping: Rp {summary['shipping']:,}")
    print(f"Tax: Rp {summary['tax']:,}")
    print("-" * 50)
    print(f"TOTAL: Rp {summary['total']:,}")
    print(f"Status: {summary['status']}")
    print("=" * 50 + "\n")


# ========================================
# DEMO - How to use the app
# ========================================

def main():
    """Demo of the shopping app"""
    print("=== ONLINE SHOPPING DEMO ===\n")
    
    # Create cart
    cart = ShoppingCart()
    
    # Add items
    cart.add_item("Laptop", 15_000_000, 1)
    cart.add_item("Mouse", 500_000, 2)
    cart.add_item("Keyboard", 1_000_000, 1)
    
    print("Cart items:")
    for item in cart.items:
        print(f"  - {item['name']}: Rp {item['price']:,} x {item['quantity']}")
    
    # Scenario 1: With discount code
    print("\n--- SCENARIO 1: With SAVE20 code ---")
    result1 = complete_purchase(cart, discount_code="SAVE20", location="local")
    print_summary(result1)
    
    # Scenario 2: Auto discount
    print("--- SCENARIO 2: Auto discount ---")
    result2 = complete_purchase(cart, location="national")
    print_summary(result2)
    
    # Scenario 3: Small order
    print("--- SCENARIO 3: Small order ---")
    small_cart = ShoppingCart()
    small_cart.add_item("Book", 200_000, 2)
    small_cart.add_item("Pen", 50_000, 3)
    result3 = complete_purchase(small_cart, location="local")
    print_summary(result3)


if __name__ == "__main__":
    main()
