#!/bin/bash
# Additional edge case tests for computor.py

echo "============================================"
echo "Edge Case Tests"
echo "============================================"
echo ""

echo "Test: Zero discriminant (one solution)"
echo "Input: 1 * X^0 - 2 * X^1 + 1 * X^2 = 0"
python3 computor.py "1 * X^0 - 2 * X^1 + 1 * X^2 = 0"
echo ""

echo "============================================"
echo "Test: Equation already in reduced form"
echo "Input: 0 * X^0 + 0 * X^1 + 1 * X^2 = 0"
python3 computor.py "0 * X^0 + 0 * X^1 + 1 * X^2 = 0"
echo ""

echo "============================================"
echo "Test: Negative coefficient in first term"
echo "Input: -5 * X^0 + 3 * X^1 = 0"
python3 computor.py "-5 * X^0 + 3 * X^1 = 0"
echo ""

echo "============================================"
echo "Test: Large coefficients"
echo "Input: 100 * X^0 + 50 * X^1 + 25 * X^2 = 0"
python3 computor.py "100 * X^0 + 50 * X^1 + 25 * X^2 = 0"
echo ""

echo "============================================"
echo "Edge case tests completed!"
echo "============================================"
