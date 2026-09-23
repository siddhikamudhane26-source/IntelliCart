# Normalization
**UNF:** A single order record with repeating Product1, Qty1, Product2, Qty2 creates repeating groups.
**1NF:** Each field is atomic and every order item becomes a separate row.
**2NF:** Product attributes depend on ProductID, so product details are separated into PRODUCTS; line attributes stay in ORDER_ITEMS.
**3NF:** Customer attributes are in USERS, order attributes in ORDERS, and product attributes in PRODUCTS, removing transitive dependencies.
Final 3NF relations: USERS, PRODUCTS, ORDERS, ORDER_ITEMS.
