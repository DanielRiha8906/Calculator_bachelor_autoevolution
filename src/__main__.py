from .calculator import Calculator

def main():
    calc = Calculator()
    print("Addition:", calc.add(10, 5))
    print("Subtraction:", calc.subtract(10, 5))
    print("Multiplication:", calc.multiply(10, 5))
    print("Division:", calc.divide(10, 5))
    print("Factorial:", calc.factorial(5))
    print("Square:", calc.square(4))
    print("Cube:", calc.cube(3))
    print("Square Root:", calc.square_root(9))
    print("Cube Root:", calc.cube_root(27))
    print("Power:", calc.power(2, 10))
    print("Log (base 10):", calc.log(100))
    print("Ln (natural log):", calc.ln(1))

if __name__ == "__main__":
    main()
