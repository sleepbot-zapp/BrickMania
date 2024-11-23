from math import (
    acos,
    asin,
    asinh,
    atan,
    cos,
    cosh,
    exp,
    exp2,
    expm1,
    sin,
    sinh,
    tan,
    tanh,
)


# Trigonometric and Hyperbolic Functions
def sec(x):
    """Secant of x."""
    return 1 / cos(x)


def cosec(x):
    """Cosecant of x."""
    return 1 / sin(x)


def cot(x):
    """Cotangent of x."""
    return 1 / tan(x)


# Inverse Hyperbolic Functions
def inv_sinh(x):
    """Inverse hyperbolic sine of x."""
    return 1 / sinh(x)


def inv_cosh(x):
    """Inverse hyperbolic cosine of x."""
    return 1 / cosh(x)


def inv_tanh(x):
    """Inverse hyperbolic tangent of x."""
    return 1 / tanh(x)


# Inverse Trigonometric Functions
def inv_asin(x):
    """Inverse sine of x."""
    return 1 / asin(x)


def inv_acos(x):
    """Inverse cosine of x."""
    return 1 / acos(x)


def inv_atan(x):
    """Inverse tangent of x."""
    return 1 / atan(x)


# Combinations of functions
combs = (
    (sin, cos),
    (sin, tan),
    (sin, sinh),
    (sin, tanh),
    (sin, exp),
    (sin, exp2),
    (sin, asin),
    (sin, acos),
    (sin, atan),
    (sin, asinh),
    (cos, sin),
    (cos, tan),
    (cos, sinh),
    (cos, tanh),
    (cos, expm1),
    (cos, asin),
    (cos, atan),
    (tan, sin),
    (tan, cos),
    (tan, sec),
    (tan, sinh),
    (tan, cosh),
    (tan, tanh),
    (tan, inv_cosh),
    (tan, exp),
    (tan, exp2),
    (tan, expm1),
    (sec, sin),
    (sec, tan),
    (sec, sinh),
    (sec, tanh),
    (sec, expm1),
    (sinh, sin),
    (sinh, cos),
    (sinh, tan),
    (sinh, sec),
    (sinh, sinh),
    (sinh, cosh),
    (sinh, tanh),
    (sinh, exp),
    (sinh, exp2),
    (sinh, expm1),
    (cosh, sin),
    (cosh, tan),
    (cosh, sinh),
    (cosh, tanh),
    (cosh, expm1),
    (tanh, sin),
    (tanh, cos),
    (tanh, tan),
    (tanh, sec),
    (tanh, sinh),
    (tanh, cosh),
    (tanh, tanh),
    (tanh, inv_cosh),
    (tanh, exp),
    (tanh, exp2),
    (tanh, expm1),
    (inv_cosh, sin),
    (inv_cosh, tan),
    (inv_cosh, sinh),
    (inv_cosh, tanh),
    (inv_cosh, expm1),
)
