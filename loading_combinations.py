import math

sec = lambda x: 1 / math.cos(x)
cosec = lambda x: 1 / math.sin(x)
cot = lambda x: 1 / math.tan(x)
inv_sinh = lambda x: 1 / math.sinh(x)
inv_cosh = lambda x: 1 / math.cosh(x)
inv_tanh = lambda x: 1 / math.tanh(x)
inv_asin = lambda x: 1/math.asin(x)
inv_acos = lambda x: 1/math.acos(x)
inv_atan = lambda x: 1/math.atan(x)
identity = lambda x: x

functions = [
    math.sin, math.cos, math.tan, sec, cosec, cot,
    math.asin, math.acos, math.atan, math.sinh, math.cosh, math.tanh,
    inv_sinh, inv_cosh, inv_asin, inv_acos, inv_atan,
    math.exp, math.exp2, math.expm1, math.sqrt, math.log, math.log10, math.cbrt, 
    math.gamma, identity
]
