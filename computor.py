#!/usr/bin/env python3
"""
Computor v1 - Polynomial equation solver
Solves polynomial equations of degree 2 or lower
"""

import sys
import re


def custom_sqrt(n: float) -> float | None:
    """Calculate square root using Newton's method (Babylonian method)."""
    if n < 0:
        return None
    if n == 0:
        return 0.0
    
    x = float(n)
    for _ in range(100):
        x_new = (x + n / x) / 2.0
        if custom_abs(x_new - x) < 1e-12:
            break
        x = x_new
    return x


def custom_abs(n: float) -> float:
    """Absolute value without using built-in abs."""
    return n if n >= 0 else -n


def gcd(a: int, b: int) -> int:
    """Calculate greatest common divisor using Euclidean algorithm."""
    a, b = int(custom_abs(a)), int(custom_abs(b))
    while b:
        a, b = b, a % b
    return a


def simplify_fraction(numerator: int, denominator: int) -> tuple[int, int]:
    """Simplify a fraction to lowest terms."""
    if denominator == 0:
        return (numerator, denominator)
    
    divisor = gcd(numerator, denominator)
    if divisor == 0:
        return (numerator, denominator)
    
    num = int(numerator / divisor)
    denom = int(denominator / divisor)
    if denom < 0:
        num = -num
        denom = -denom
    return (num, denom)


def format_number(val: float, max_decimals: int = 6) -> str:
    """
    Format a number cleanly:
    - If integer (e.g. 4.0, -5.0), display as '4', '-5'
    - Otherwise format with up to max_decimals without trailing zero noise.
    """
    if custom_abs(val) < 1e-12:
        return "0"
    if val.is_integer():
        return str(int(val))
    rounded = round(val, max_decimals)
    if rounded.is_integer():
        return str(int(rounded))
    # Format with precision and strip trailing zeros
    formatted = f"{rounded:.{max_decimals}f}".rstrip("0").rstrip(".")
    return formatted


def format_fraction(value: float, precision: float = 1e-9) -> str:
    """Try to represent a decimal as a simple fraction, fallback to formatted float."""
    if custom_abs(value - round(value)) < precision:
        return str(int(round(value)))
    
    for denom in range(1, 101):
        num = value * denom
        if custom_abs(num - round(num)) < precision:
            s_num, s_denom = simplify_fraction(int(round(num)), denom)
            if s_denom == 1:
                return str(s_num)
            return f"{s_num}/{s_denom}"
    
    return format_number(value)


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


def format_reduced_form(coefficients: dict[int, float]) -> str:
    """Format the reduced equation in the standard format (e.g. '4 * X^0 + 4 * X^1 - 9.3 * X^2 = 0')."""
    if not coefficients:
        return "0 * X^0 = 0"
    
    max_power = max(coefficients.keys()) if coefficients else 0
    all_zero = all(custom_abs(coefficients.get(i, 0.0)) < 1e-12 for i in range(max_power + 1))
    if all_zero:
        return "0 * X^0 = 0"
    
    terms = []
    for power in range(max_power + 1):
        coeff = coefficients.get(power, 0.0)
        if custom_abs(coeff) < 1e-12:
            coeff = 0.0
            
        coeff_str = format_number(custom_abs(coeff)) if terms else format_number(coeff)
        if not terms:
            terms.append(f"{coeff_str} * X^{power}")
        else:
            sign = "+" if coeff >= 0 else "-"
            terms.append(f"{sign} {coeff_str} * X^{power}")
    
    return " ".join(terms) + " = 0"


def get_degree(coefficients: dict[int, float]) -> int:
    """Get polynomial degree (highest power with non-zero coefficient)."""
    if not coefficients:
        return 0
    
    for power in sorted(coefficients.keys(), reverse=True):
        if custom_abs(coefficients[power]) > 1e-12:
            return power
    return 0


def solve_degree_0(coefficients: dict[int, float]) -> None:
    """Solve constant equation: c = 0."""
    c = coefficients.get(0, 0.0)
    if custom_abs(c) < 1e-12:
        print("Any real number is a solution.")
    else:
        print("No solution.")


def solve_degree_1(coefficients: dict[int, float]) -> None:
    """Solve linear equation: a + bX = 0 -> X = -a / b."""
    a = coefficients.get(0, 0.0)
    b = coefficients.get(1, 0.0)
    
    if custom_abs(b) < 1e-12:
        solve_degree_0(coefficients)
        return
    
    solution = -a / b
    print("The solution is:")
    print(format_number(solution))


def solve_degree_2(coefficients: dict[int, float]) -> None:
    """Solve quadratic equation: c + bX + aX^2 = 0 using discriminant Δ = b^2 - 4ac."""
    c_val = coefficients.get(0, 0.0)
    b_val = coefficients.get(1, 0.0)
    a_val = coefficients.get(2, 0.0)
    
    if custom_abs(a_val) < 1e-12:
        solve_degree_1(coefficients)
        return
    
    discriminant = b_val * b_val - 4.0 * a_val * c_val
    
    if discriminant > 1e-12:
        print("Discriminant is strictly positive, the two solutions are:")
        sqrt_disc = custom_sqrt(discriminant)
        sol1 = (-b_val + sqrt_disc) / (2.0 * a_val)
        sol2 = (-b_val - sqrt_disc) / (2.0 * a_val)
        first, second = (sol1, sol2) if sol1 > sol2 else (sol2, sol1)
        print(format_number(first))
        print(format_number(second))
    elif custom_abs(discriminant) <= 1e-12:
        print("Discriminant is zero, the solution is:")
        solution = -b_val / (2.0 * a_val)
        print(format_number(solution))
    else:
        print("Discriminant is strictly negative, the two complex solutions are:")
        sqrt_disc = custom_sqrt(-discriminant)
        real_part = -b_val / (2.0 * a_val)
        imag_part = sqrt_disc / (2.0 * a_val)
        
        real_str = format_fraction(real_part)
        imag_str = format_fraction(custom_abs(imag_part))
        
        print(f"{real_str} + {imag_str}i")
        print(f"{real_str} - {imag_str}i")


def solve_equation(coefficients: dict[int, float]) -> None:
    """Main solving logic - dispatches to appropriate solver based on degree."""
    degree = get_degree(coefficients)
    print(f"Polynomial degree: {degree}")
    
    if degree > 2:
        print("The polynomial degree is strictly greater than 2, I can't solve.")
    elif degree == 2:
        solve_degree_2(coefficients)
    elif degree == 1:
        solve_degree_1(coefficients)
    else:
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
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting...", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
