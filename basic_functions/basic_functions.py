import os # added so that Github actions can run the script with test values 

# Check if running in Github Actions
is_ci = os.getenv("CI") == "true"
is_test = any(key.startswith("PYTEST_") for key in os.environ)  # ✅ Better way to detect pytest
print(f"Is Test: {is_test}")
print(f"Is CI: {is_ci}")



# Task 1: Create a function add(a, b) that returns a + b

def add(num1, num2):
    return num1 + num2

if not (is_ci or is_test):
    num1 = int(input("Enter First Number: "))
    num2 = int(input("Enter Second Number: "))
else:
    num1, num2 = 5, 8

result = add(num1, num2)
print(f"Sum of {num1} and {num2} is {result}")


# Task 2: Create a function subtract(a, b) that returns a - b

def subtract(num1, num2):
    return num1 - num2

if not (is_ci or is_test):
    num1 = int(input("Enter First Number: "))
    num2 = int(input("Enter Second Number: "))
else:
    num1, num2 = 5, 8

result = subtract(num1,num2)

print(f"Subtract of {num1} and {num2} is {result}")



# Task 32: Create a function multiply(a, b) that returns a * b


def multiply(num1, num2):
    return num1 * num2

if not (is_ci or is_test):
    num1 = int(input("Enter First Number: "))
    num2 = int(input("Enter Second Number: "))
else:
    num1, num2 = 5, 8

result = multiply(num1,num2)

print(f"multiplication of {num1} and {num2} is {result}")