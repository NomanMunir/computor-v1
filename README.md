# Computor v1

A polynomial equation solver for equations of degree 2 or lower.

## Description

This project implements a simple equation solver that:

- Parses polynomial equations in the format `a * X^n`
- Reduces equations to standard form (all terms on left side)
- Solves equations of degree 0, 1, and 2
- Handles real and complex solutions
- Uses custom implementations (no math libraries for sqrt, etc.)

## Features

- ✅ Degree 0 equations (constants): Determines if equation has no solution, one solution, or infinite solutions
- ✅ Degree 1 equations (linear): Solves for single real solution
- ✅ Degree 2 equations (quadratic): Uses discriminant method
  - Positive discriminant: Two real solutions
  - Zero discriminant: One real solution
  - Negative discriminant: Two complex solutions
- ✅ Detects equations of degree > 2 (reports as unsolvable)
- ✅ Custom square root implementation (Newton's method)
- ✅ Fraction simplification for cleaner output

## Usage

```bash
# Run with command-line argument
./computor.py "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"

# Or run without arguments to enter equation interactively
./computor.py
```

## Examples

```bash
# Quadratic with two real solutions
$ ./computor.py "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"
Reduced form: 4.0 * X^0 + 4.0 * X^1 - 9.3 * X^2 = 0
Polynomial degree: 2
Discriminant is strictly positive, the two solutions are:
0.905239
-0.475131

# Linear equation
$ ./computor.py "5 * X^0 + 4 * X^1 = 4 * X^0"
Reduced form: 1.0 * X^0 + 4.0 * X^1 = 0
Polynomial degree: 1
The solution is:
-0.25

# Complex solutions
$ ./computor.py "1 * X^0 + 2 * X^1 + 5 * X^2 = 0"
Reduced form: 1.0 * X^0 + 2.0 * X^1 + 5.0 * X^2 = 0
Polynomial degree: 2
Discriminant is strictly negative, the two complex solutions are:
-1/5 + 2/5i
-1/5 - 2/5i
```

## Testing

Run the test suite with all examples from the project specification:

```bash
chmod +x test.sh
./test.sh
```

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Implementation Details

- **Custom sqrt function**: Implemented using Newton's method (Babylonian algorithm)
- **Fraction simplification**: GCD-based reduction for cleaner complex number output
- **No math libraries**: All mathematical operations implemented from scratch using only basic arithmetic

## Project Structure

```text
.
├── computor.py        # Main solver program
├── test.sh           # Test script with all examples
├── README.md         # This file
└── computor-v1.pdf   # Project specification
```

## Author

42 School Project - Computor v1
