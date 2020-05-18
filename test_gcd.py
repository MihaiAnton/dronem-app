import pytest
from computeGCD import computeGCD

def test_gcd_valid():
    assert computeGCD(60, 48) == 12

def test_gcd_invalid():
    assert computeGCD(60, 48) == 13, "Test failed!"

