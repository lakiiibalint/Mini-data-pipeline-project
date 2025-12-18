from src.processing.clean import to_availability

print("=== Testing to_availability() ===")
print("Test 1 (numeric in parentheses):", to_availability("In stock (22 available)"))
print("Test 2 (numeric inline):", to_availability("15 in stock"))
print("Test 3 (no number, in stock):", to_availability("In stock"))
print("Test 4 (out of stock):", to_availability("Out of Stock"))
print("Test 5 (None):", to_availability(None))
print("Test 6 (unknown text):", to_availability("Availability: TBD"))
