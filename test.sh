#!/bin/bash
# Test script for computor.py with all examples from the PDF

# Detect Python command
if command -v uv &> /dev/null; then
    PY_CMD="uv run python"
elif command -v python3 &> /dev/null; then
    PY_CMD="python3"
else
    PY_CMD="python"
fi

echo "============================================"
echo "Computor v1 - Test Suite"
echo "============================================"
echo ""

echo "Test 1: Quadratic with positive discriminant"
echo "Input: 5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"
$PY_CMD computor.py "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"
echo ""

echo "============================================"
echo "Test 2: Linear equation"
echo "Input: 5 * X^0 + 4 * X^1 = 4 * X^0"
$PY_CMD computor.py "5 * X^0 + 4 * X^1 = 4 * X^0"
echo ""

echo "============================================"
echo "Test 3: Degree > 2 (unsolvable)"
echo "Input: 8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0"
$PY_CMD computor.py "8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0"
echo ""

echo "============================================"
echo "Test 4: Infinite solutions"
echo "Input: 6 * X^0 = 6 * X^0"
$PY_CMD computor.py "6 * X^0 = 6 * X^0"
echo ""

echo "============================================"
echo "Test 5: No solution"
echo "Input: 10 * X^0 = 15 * X^0"
$PY_CMD computor.py "10 * X^0 = 15 * X^0"
echo ""

echo "============================================"
echo "Test 6: Complex solutions"
echo "Input: 1 * X^0 + 2 * X^1 + 5 * X^2 = 0"
$PY_CMD computor.py "1 * X^0 + 2 * X^1 + 5 * X^2 = 0"
echo ""

echo "============================================"
echo "All tests completed!"
echo "============================================"
