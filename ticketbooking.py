"""
Ticket Booking System - Simplified Version
For Information System Students

This app demonstrates:
- Unit Testing: Test individual calculations
- Integration Testing: Test single ticket booking
- System Testing: Test multiple tickets booking
"""


class BookingCart:
    """Booking cart to store tickets"""
    
    def __init__(self):
        self.tickets = []  # List to store tickets
    
    def add_ticket(self, event_name, price, quantity):
        """Add a ticket to cart"""
        if price < 0:
            raise ValueError("Price cannot be negative")
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        ticket = {
            'event': event_name,
            'price': price,
            'quantity': quantity
        }
        self.tickets.append(ticket)
    
    def get_tickets(self):
        """Get all tickets in cart"""
        return self.tickets


# ========================================
# PART 1: UNIT TESTABLE FUNCTIONS
# Test these functions one by one
# ========================================

def calculate_ticket_total(price, quantity):
    """
    Calculate total for one ticket type
    Example: price=500000, quantity=2 -> 1000000
    """
    if price < 0:
        raise ValueError("Price cannot be negative")
    if quantity <= 0:
        raise ValueError("Quantity must be positive")
    
    total = price * quantity
    return total


def calculate_subtotal(tickets):
    """
    Calculate subtotal of all tickets
    Example: 3 ticket types -> add all their totals
    """
    if not tickets:
        return 0
    
    subtotal = 0
    for ticket in tickets:
        ticket_total = ticket['price'] * ticket['quantity']
        subtotal = subtotal + ticket_total
    
    return subtotal


def apply_discount(subtotal, promo_code=None):
    """
    Apply discount to subtotal
    
    Promo Codes:
    - EARLY10 = 10% off
    - STUDENT20 = 20% off
    - VIP30 = 30% off
    
    Auto discount (no code):
    - >= 5,000,000 = 15% off (Group booking)
    - >= 2,500,000 = 10% off (Medium group)
    - >= 1,000,000 = 5% off (Small group)
    """
    if subtotal < 0:
        raise ValueError("Subtotal cannot be negative")
    
    discount_percent = 0
    
    # Check if user has promo code
    if promo_code:
        code = promo_code.upper()
        if code == "EARLY10":
            discount_percent = 10
        elif code == "STUDENT20":
            discount_percent = 20
        elif code == "VIP30":
            discount_percent = 30
    else:
        # Auto discount based on total
        if subtotal >= 5_000_000:
            discount_percent = 15
        elif subtotal >= 2_500_000:
            discount_percent = 10
        elif subtotal >= 1_000_000:
            discount_percent = 5
    
    discount_amount = subtotal * discount_percent / 100
    return discount_amount, discount_percent


def calculate_service_fee(subtotal_after_discount, payment_method="credit_card"):
    """
    Calculate service fee
    
    Rules:
    - FREE if total >= 3,000,000
    - Credit Card = 2% (min Rp 10,000)
    - E-Wallet = 1.5% (min Rp 5,000)
    - Bank Transfer = Rp 5,000 (flat)
    """
    if subtotal_after_discount < 0:
        raise ValueError("Subtotal cannot be negative")
    
    # Free service fee for big orders
    if subtotal_after_discount >= 3_000_000:
        return 0
    
    method = payment_method.lower()
    
    if method == "credit_card":
        fee = subtotal_after_discount * 0.02
        return max(fee, 10_000)  # Minimum Rp 10,000
    elif method == "e_wallet":
        fee = subtotal_after_discount * 0.015
        return max(fee, 5_000)  # Minimum Rp 5,000
    elif method == "bank_transfer":
        return 5_000  # Flat fee
    else:
        raise ValueError("Invalid payment method")


def calculate_platform_fee(total_tickets):
    """
    Calculate platform/admin fee per ticket
    
    Rules:
    - 1-5 tickets: Rp 10,000 per ticket
    - 6-10 tickets: Rp 7,500 per ticket
    - 11+ tickets: Rp 5,000 per ticket
    """
    if total_tickets <= 0:
        raise ValueError("Total tickets must be positive")
    
    if total_tickets <= 5:
        fee_per_ticket = 10_000
    elif total_tickets <= 10:
        fee_per_ticket = 7_500
    else:
        fee_per_ticket = 5_000
    
    return total_tickets * fee_per_ticket


# ========================================
# PART 2: INTEGRATION FUNCTION
# Book ONE ticket type (single event)
# ========================================

def book_single_ticket(event_name, price, quantity, promo_code=None):
    """
    Book tickets for ONE event
    
    Steps:
    1. Calculate ticket total
    2. Apply discount
    3. Calculate platform fee
    
    This is INTEGRATION testing - combines multiple unit functions
    """
    # Validate
    if price < 0:
        raise ValueError("Price cannot be negative")
    if quantity <= 0:
        raise ValueError("Quantity must be positive")
    
    # Calculate total
    ticket_total = calculate_ticket_total(price, quantity)
    
    # Apply discount
    discount_amount, discount_percent = apply_discount(ticket_total, promo_code)
    after_discount = ticket_total - discount_amount
    
    # Calculate platform fee
    platform_fee = calculate_platform_fee(quantity)
    
    # Final total
    final_total = after_discount + platform_fee
    
    result = {
        "event": event_name,
        "quantity": quantity,
        "ticket_price": price,
        "ticket_total": ticket_total,
        "discount_amount": discount_amount,
        "discount_percent": discount_percent,
        "after_discount": after_discount,
        "platform_fee": platform_fee,
        "final_total": final_total
    }
    
    return result


# ========================================
# PART 3: SYSTEM FUNCTION
# Complete booking for MULTIPLE tickets/events
# ========================================

def process_booking(cart, promo_code=None, payment_method="credit_card"):
    """
    Process complete booking with MULTIPLE ticket types
    
    This is the MAIN SYSTEM function that does everything:
    1. Check cart is not empty
    2. Calculate subtotal for all tickets
    3. Apply discount
    4. Calculate platform fee
    5. Calculate service fee
    6. Create booking summary
    """
    # Check cart has tickets
    if not cart.tickets:
        raise ValueError("Cart is empty")
    
    # Calculate subtotal
    subtotal = calculate_subtotal(cart.tickets)
    
    # Apply discount
    discount_amount, discount_percent = apply_discount(subtotal, promo_code)
    after_discount = subtotal - discount_amount
    
    # Calculate total tickets count
    total_tickets = sum(ticket['quantity'] for ticket in cart.tickets)
    
    # Calculate fees
    platform_fee = calculate_platform_fee(total_tickets)
    service_fee = calculate_service_fee(after_discount, payment_method)
    
    # Final total
    final_total = after_discount + platform_fee + service_fee
    
    # Create summary
    summary = {
        "tickets": cart.tickets,
        "total_tickets": total_tickets,
        "subtotal": subtotal,
        "discount": discount_amount,
        "discount_percent": discount_percent,
        "after_discount": after_discount,
        "platform_fee": platform_fee,
        "service_fee": service_fee,
        "payment_method": payment_method,
        "total": final_total,
        "status": "Success"
    }
    
    return summary


def print_booking_summary(summary):
    """Print booking summary nicely"""
    print("\n" + "=" * 60)
    print("BOOKING SUMMARY")
    print("=" * 60)
    
    print("\nTICKETS:")
    for ticket in summary['tickets']:
        total = ticket['price'] * ticket['quantity']
        print(f"  {ticket['event']}: Rp {ticket['price']:,} x {ticket['quantity']} = Rp {total:,}")
    
    print(f"\nTotal Tickets: {summary['total_tickets']}")
    print(f"Subtotal: Rp {summary['subtotal']:,}")
    
    if summary['discount'] > 0:
        print(f"Discount ({summary['discount_percent']}%): -Rp {summary['discount']:,}")
    
    print(f"After Discount: Rp {summary['after_discount']:,}")
    print(f"Platform Fee: Rp {summary['platform_fee']:,}")
    print(f"Service Fee ({summary['payment_method']}): Rp {summary['service_fee']:,}")
    print("-" * 60)
    print(f"TOTAL PAYMENT: Rp {summary['total']:,}")
    print(f"Status: {summary['status']}")
    print("=" * 60 + "\n")


def print_single_ticket_summary(ticket_data):
    """Print single ticket booking nicely"""
    print("\n" + "=" * 50)
    print(f"EVENT: {ticket_data['event']}")
    print("=" * 50)
    print(f"Ticket Price: Rp {ticket_data['ticket_price']:,}")
    print(f"Quantity: {ticket_data['quantity']}")
    print(f"Ticket Total: Rp {ticket_data['ticket_total']:,}")
    
    if ticket_data['discount_amount'] > 0:
        print(f"Discount ({ticket_data['discount_percent']}%): -Rp {ticket_data['discount_amount']:,}")
    
    print(f"After Discount: Rp {ticket_data['after_discount']:,}")
    print(f"Platform Fee: Rp {ticket_data['platform_fee']:,}")
    print("-" * 50)
    print(f"Total: Rp {ticket_data['final_total']:,}")
    print("=" * 50 + "\n")


# ========================================
# DEMO - How to use the app
# ========================================

def main():
    """Demo of the ticket booking system"""
    print("=== TICKET BOOKING SYSTEM DEMO ===\n")
    
    # ============================================
    # INTEGRATION TEST DEMO: Book single ticket type
    # ============================================
    print("=" * 60)
    print("INTEGRATION TEST: Single Event Booking")
    print("=" * 60)
    
    print("\n--- Event 1: Concert with STUDENT20 code ---")
    concert = book_single_ticket("Rock Concert", 750_000, 2, "STUDENT20")
    print_single_ticket_summary(concert)
    
    print("--- Event 2: Theater without promo ---")
    theater = book_single_ticket("Theater Show", 400_000, 4, None)
    print_single_ticket_summary(theater)
    
    print("--- Event 3: Sports Event with VIP30 ---")
    sports = book_single_ticket("Football Match", 1_200_000, 3, "VIP30")
    print_single_ticket_summary(sports)
    
    # ============================================
    # SYSTEM TEST DEMO: Complete booking with multiple tickets
    # ============================================
    print("\n" + "=" * 60)
    print("SYSTEM TEST: Multiple Events - Complete Booking")
    print("=" * 60)
    
    # Scenario 1: Multiple events with promo code
    print("\n--- SCENARIO 1: Family Outing (with EARLY10 promo) ---")
    cart1 = BookingCart()
    cart1.add_ticket("Movie Premier", 150_000, 4)
    cart1.add_ticket("Museum Tour", 75_000, 4)
    cart1.add_ticket("Food Festival", 200_000, 4)
    result1 = process_booking(cart1, "EARLY10", "credit_card")
    print_booking_summary(result1)
    
    # Scenario 2: Large group booking with auto discount
    print("--- SCENARIO 2: Corporate Event (Auto discount) ---")
    cart2 = BookingCart()
    cart2.add_ticket("Conference", 2_500_000, 1)
    cart2.add_ticket("Workshop", 1_500_000, 2)
    result2 = process_booking(cart2, None, "bank_transfer")
    print_booking_summary(result2)
    
    # Scenario 3: Small booking
    print("--- SCENARIO 3: Date Night (Small booking) ---")
    cart3 = BookingCart()
    cart3.add_ticket("Dinner Show", 500_000, 2)
    result3 = process_booking(cart3, None, "e_wallet")
    print_booking_summary(result3)
    
    # Scenario 4: Large group with student discount
    print("--- SCENARIO 4: Student Group (STUDENT20) ---")
    cart4 = BookingCart()
    cart4.add_ticket("Educational Tour", 300_000, 15)
    result4 = process_booking(cart4, "STUDENT20", "bank_transfer")
    print_booking_summary(result4)


if __name__ == "__main__":
    main()
