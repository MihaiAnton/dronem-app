import pytest
import math


@pytest.mark.parametrize(
    "a,b,expected_output",
    [
        (6, 3, 3),
        (17, 23, 1),
        (4, 4, 2)
    ]
)
def test_gcd(a, b, expected_output):
    assert math.gcd(a, b) == expected_output
