from math import sin, cos, tan, sinh, cosh, tanh, asin, acos, atan, asinh, exp, exp2, expm1

sec = lambda x: 1 / cos(x)
cosec = lambda x: 1 / sin(x)
cot = lambda x: 1 / tan(x)
inv_sinh = lambda x: 1 / sinh(x)
inv_cosh = lambda x: 1 / cosh(x)
inv_tanh = lambda x: 1 / tanh(x)
inv_asin = lambda x: 1/asin(x)
inv_acos = lambda x: 1/acos(x)
inv_atan = lambda x: 1/atan(x)
identity = lambda x: x

combs = [
        (sin, cos), (sin, tan), (sin, sinh), (sin, sinh), (sin, tanh), (sin, exp), (sin, exp2), (sin, asin), (sin, acos), (sin, atan), (sin, asinh), 
        (cos, sin), (cos, tan), ((cos, sinh)), (cos, tanh), (cos, expm1), (cos, asin), (cos, atan),
        (tan, sin), (tan, cos), (tan, sec), (tan, sinh), (tan, cosh), (tan, tanh), (tan, inv_cosh), (tan, exp), (tan, exp2), (tan, expm1),
        (sec, sin), (sec, tan), (sec, sinh), (sec, tanh), (sec, expm1),
        (sinh, sin), (sinh, cos), (sinh, tan), (sinh, sec), (sinh, sinh), (sinh, cosh), (sinh, tanh), (sinh, exp), (sinh, exp2), (sinh, expm1),
        (cosh, sin), (cosh, tan), (cosh, sinh), (cosh, tanh), (cosh, expm1),
        (tanh, sin), (tanh, cos), (tanh, tan), (tanh, sec), (tanh, sinh), (tanh, cosh), (tanh, tanh), (tanh, inv_cosh), (tanh, exp), (tanh, exp2), (tanh, expm1),
        (inv_cosh, sin), (inv_cosh, tan), (inv_cosh, sinh), (inv_cosh, tanh), (inv_cosh, expm1),
    ]