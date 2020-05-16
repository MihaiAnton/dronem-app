def computeGCD(x, y):
    """
    Function for computing the gcd of two numbers
    :param x: integer
    :param y: integer
    :return: gcd of x and y
    """
    while (y):
        x, y = y, x % y

    return x