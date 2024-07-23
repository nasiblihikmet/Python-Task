def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
        #  print(f"i={i}, result={result}") 
    return result

print(factorial(5))  # Expected output: 120
