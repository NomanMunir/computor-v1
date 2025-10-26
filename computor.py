#!/usr/bin/env python3
"""
Computor v1 - Polynomial equation solver
Solves polynomial equations of degree 2 or lower
"""

import sys
import re


def custom_sqrt(n):
    """
    Calculate square root using Newton's method (Babylonian method)
    No math library allowed!
    """
    if n < 0:
        return None
    if n == 0:
        return 0
    
    # Initial guess
    x = n
    # Newton's method: x_new = (x + n/x) / 2
    for _ in range(50):  # Sufficient iterations for convergence
        x_new = (x + n / x) / 2
        if abs(x_new - x) < 1e-10:  # Convergence threshold
            break
        x = x_new
    
    return x


def custom_abs(n):
    """Absolute value without using built-in abs"""
    return n if n >= 0 else -n


def gcd(a, b):
    """
    Calculate greatest common divisor using Euclidean algorithm
    """
    a, b = int(abs(a)), int(abs(b))
    while b:
        a, b = b, a % b
    return a


def simplify_fraction(numerator, denominator):
    """
    Simplify a fraction to lowest terms
    Returns: (num, denom) tuple
    """
    if denominator == 0:
        return (numerator, denominator)
    
    # Find GCD
    divisor = gcd(numerator, denominator)
    if divisor == 0:
        return (numerator, denominator)
    
    num = int(numerator / divisor)
    denom = int(denominator / divisor)
    
    # Make sure denominator is positive
    if denom < 0:
        num = -num
        denom = -denom
    
    return (num, denom)


def format_fraction(value, precision=1e-9):
    """
    Try to represent a decimal as a simple fraction
    Returns string representation
    """
    # Check if it's already close to an integer
    if abs(value - round(value)) < precision:
        return str(int(round(value)))
    
    # Try to find a simple fraction representation
    # Check denominators up to 100
    for denom in range(1, 101):
        num = value * denom
        if abs(num - round(num)) < precision:
            num, denom = simplify_fraction(round(num), denom)
            if denom == 1:
                return str(num)
            return f"{num}/{denom}"
    
    # Fall back to decimal
    return str(value)


class Term:
    """Represents a polynomial term: coefficient * X^power"""
    def __init__(self, coefficient, power):
        self.coefficient = float(coefficient)
        self.power = int(power)
    
    def __repr__(self):
        return f"Term({self.coefficient}, {self.power})"


def parse_equation(equation_str):
    """
    Parse equation string and extract terms from both sides
    Returns: (left_terms, right_terms)
    """
    # Split by '='
    if '=' not in equation_str:
        raise ValueError("Invalid equation: missing '='")
    
    parts = equation_str.split('=')
    if len(parts) != 2:
        raise ValueError("Invalid equation: multiple '=' signs")
    
    left_side = parts[0].strip()
    right_side = parts[1].strip()
    
    left_terms = parse_side(left_side)
    right_terms = parse_side(right_side)
    
    return left_terms, right_terms


def parse_side(side_str):
    """
    Parse one side of the equation and extract all terms
    Returns: list of Term objects
    """
    terms = []
    
    # Pattern to match terms like: [+/-] coefficient * X^power
    # Also handles free-form like: 5, 4*X, X^2, etc.
    pattern = r'([+-]?\s*\d+\.?\d*)\s*\*?\s*X\s*\^\s*(\d+)'
    
    # Find all matches
    matches = re.findall(pattern, side_str, re.IGNORECASE)
    
    for match in matches:
        coefficient = match[0].replace(' ', '')
        power = match[1]
        terms.append(Term(coefficient, power))
    
    return terms


def reduce_equation(left_terms, right_terms):
    """
    Move all terms to left side and combine like terms
    Returns: dict mapping power -> coefficient
    """
    # Dictionary to store combined coefficients by power
    coefficients = {}
    
    # Add left side terms
    for term in left_terms:
        if term.power in coefficients:
            coefficients[term.power] += term.coefficient
        else:
            coefficients[term.power] = term.coefficient
    
    # Subtract right side terms (move to left)
    for term in right_terms:
        if term.power in coefficients:
            coefficients[term.power] -= term.coefficient
        else:
            coefficients[term.power] = -term.coefficient
    
    return coefficients


def format_reduced_form(coefficients):
    """
    Format the reduced equation in the required output format
    """
    if not coefficients:
        return "0 * X^0 = 0"
    
    # Get max power to determine range
    max_power = max(coefficients.keys()) if coefficients else 0
    
    # Check if all coefficients are zero
    all_zero = all(coefficients.get(i, 0) == 0 for i in range(max_power + 1))
    if all_zero:
        return "0 * X^0 = 0"
    
    terms = []
    for power in range(max_power + 1):
        coeff = coefficients.get(power, 0)
        
        if not terms:
            # First term - no leading sign if positive
            terms.append(f"{coeff} * X^{power}")
        else:
            # Subsequent terms with explicit sign
            if coeff >= 0:
                terms.append(f"+ {coeff} * X^{power}")
            else:
                terms.append(f"- {-coeff} * X^{power}")
    
    return " ".join(terms) + " = 0"


def get_degree(coefficients):
    """
    Get the degree of the polynomial (highest power with non-zero coefficient)
    """
    if not coefficients:
        return 0
    
    # Find highest power with non-zero coefficient
    for power in sorted(coefficients.keys(), reverse=True):
        if coefficients[power] != 0:
            return power
    
    return 0


def solve_degree_0(coefficients):
    """
    Solve constant equation: a = 0
    """
    a = coefficients.get(0, 0)
    
    if a == 0:
        print("Any real number is a solution.")
    else:
        print("No solution.")


def solve_degree_1(coefficients):
    """
    Solve linear equation: a + bX = 0
    Solution: X = -a/b
    """
    a = coefficients.get(0, 0)
    b = coefficients.get(1, 0)
    
    if b == 0:
        solve_degree_0(coefficients)
        return
    
    solution = -a / b
    print("The solution is:")
    print(solution)


def solve_degree_2(coefficients):
    """
    Solve quadratic equation: a + bX + cX^2 = 0
    Using discriminant: Δ = b^2 - 4ac
    """
    a = coefficients.get(0, 0)
    b = coefficients.get(1, 0)
    c = coefficients.get(2, 0)
    
    if c == 0:
        solve_degree_1(coefficients)
        return
    
    # Calculate discriminant
    discriminant = b * b - 4 * a * c
    
    if discriminant > 0:
        print("Discriminant is strictly positive, the two solutions are:")
        sqrt_disc = custom_sqrt(discriminant)
        sol1 = (-b + sqrt_disc) / (2 * c)
        sol2 = (-b - sqrt_disc) / (2 * c)
        # Print in descending order
        if sol1 > sol2:
            print(sol1)
            print(sol2)
        else:
            print(sol2)
            print(sol1)
    elif discriminant == 0:
        print("Discriminant is zero, the solution is:")
        solution = -b / (2 * c)
        print(solution)
    else:  # discriminant < 0
        print("Discriminant is strictly negative, the two complex solutions are:")
        sqrt_disc = custom_sqrt(-discriminant)
        real_part = -b / (2 * c)
        imag_part = sqrt_disc / (2 * c)
        
        # Try to format as fractions for cleaner output
        real_str = format_fraction(real_part)
        imag_str = format_fraction(imag_part)
        
        # Format with proper signs
        if imag_str.startswith('-'):
            print(f"{real_str} - {imag_str[1:]}i")
            print(f"{real_str} + {imag_str[1:]}i")
        else:
            print(f"{real_str} + {imag_str}i")
            print(f"{real_str} - {imag_str}i")


def solve_equation(coefficients):
    """
    Main solving logic - dispatches to appropriate solver based on degree
    """
    degree = get_degree(coefficients)
    
    print(f"Polynomial degree: {degree}")
    
    if degree > 2:
        print("The polynomial degree is strictly greater than 2, I can't solve.")
    elif degree == 2:
        solve_degree_2(coefficients)
    elif degree == 1:
        solve_degree_1(coefficients)
    else:  # degree 0
        solve_degree_0(coefficients)


def main():
    """Main program entry point"""
    # Get equation from command line or stdin
    if len(sys.argv) > 1:
        equation_str = sys.argv[1]
    else:
        print("Enter equation:")
        equation_str = input().strip()
    
    try:
        # Parse equation
        left_terms, right_terms = parse_equation(equation_str)
        
        # Reduce to standard form
        coefficients = reduce_equation(left_terms, right_terms)
        
        # Display reduced form
        reduced_form = format_reduced_form(coefficients)
        print(f"Reduced form: {reduced_form}")
        
        # Solve
        solve_equation(coefficients)
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
