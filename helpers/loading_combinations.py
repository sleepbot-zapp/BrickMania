from math import (
    sin,
    cos,
    tan,
    sinh,
    cosh,
    tanh,
    asin,
    acos,
    atan,
    asinh,
    exp,
    exp2,
    expm1,
)


def sec(x):
    return 1 / cos(x)


def cosec(x):
    return 1 / sin(x)


def cot(x):
    return 1 / tan(x)


def inv_sinh(x):
    return 1 / sinh(x)


def inv_cosh(x):
    return 1 / cosh(x)


def inv_tanh(x):
    return 1 / tanh(x)


def inv_asin(x):
    return 1 / asin(x)


def inv_acos(x):
    return 1 / acos(x)


def inv_atan(x):
    return 1 / atan(x)


def identity(x):
    return x


combs = [
    (sin, cos),
    (sin, tan),
    (sin, sinh),
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
    ((cos, sinh)),
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
]
