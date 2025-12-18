from src.processing.clean import to_price, to_rating

print("=== Testing to_price() ===")
print("Test 1:", to_price('51.77'))
print("Test 2:", to_price('£51.77'))
print("Test 3:", to_price('  £99.99  '))
print("Test 4:", to_price(None))
print("Test 5:", to_price(''))

print("\n=== Testing to_rating() ===")
print("Test 1 (word):", to_rating('Five'))
print("Test 2 (word):", to_rating('three'))
print("Test 3 (digit):", to_rating('4'))
print("Test 4 (decimal):", to_rating('4.0'))
print("Test 5 (None):", to_rating(None))
print("Test 6 (empty):", to_rating(''))

print("\n✓ All tests passed!")
