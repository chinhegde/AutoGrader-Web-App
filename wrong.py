binary_str = ""
temp = k

# Convert integer to binary string manually
while temp > 0:
    binary_str = str(temp % 2)
    temp //= 2

# Check if binary string is equal to its reverse
return binary_str == binary_str[::-1]