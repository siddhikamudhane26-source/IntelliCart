def segment_customers(total_orders, total_spend):
    if total_spend >= 10000: return 'VIP'
    if total_orders >= 3: return 'Loyal'
    if total_orders >= 1: return 'Active'
    return 'New Customer'
