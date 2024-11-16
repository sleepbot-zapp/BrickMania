import math

sec = lambda x : 1/math.cos(x)
cosec = lambda x : 1/math.sin(x)
cot = lambda x : 1/math.tan(x)
inv_sinh = lambda x : 1/math.sinh(x)
inv_cosh = lambda x : 1/math.cosh(x)
inv_tanh = lambda x : 1/math.tanh(x)

combs = [
        (math.sin, math.cos), (math.sin, math.tan), (math.sin, math.sinh), (math.sin, math.sinh), (math.sin, math.tanh), (math.sin, math.exp), (math.sin, math.exp2), (math.sin, math.asin), (math.sin, math.acos), (math.sin, math.atan), (math.sin, math.asinh), 
        (math.cos, math.sin), (math.cos, math.tan), ((math.cos, math.sinh)), (math.cos, math.tanh), (math.cos, math.expm1), (math.cos, math.asin), (math.cos, math.atan),
        (math.tan, math.sin), (math.tan, math.cos), (math.tan, sec), (math.tan, math.sinh), (math.tan, math.cosh), (math.tan, math.tanh), (math.tan, inv_cosh), (math.tan, math.exp), (math.tan, math.exp2), (math.tan, math.expm1),
        (sec, math.sin), (sec, math.tan), (sec, math.sinh), (sec, math.tanh), (sec, math.expm1),
        (math.sinh, math.sin), (math.sinh, math.cos), (math.sinh, math.tan), (math.sinh, sec), (math.sinh, math.sinh), (math.sinh, math.cosh), (math.sinh, math.tanh), (math.sinh, math.exp), (math.sinh, math.exp2), (math.sinh, math.expm1),
        (math.cosh, math.sin), (math.cosh, math.tan), (math.cosh, math.sinh), (math.cosh, math.tanh), (math.cosh, math.expm1),
        (math.tanh, math.sin), (math.tanh, math.cos), (math.tanh, math.tan), (math.tanh, sec), (math.tanh, math.sinh), (math.tanh, math.cosh), (math.tanh, math.tanh), (math.tanh, inv_cosh), (math.tanh, math.exp), (math.tanh, math.exp2), (math.tanh, math.expm1),
        (inv_cosh, math.sin), (inv_cosh, math.tan), (inv_cosh, math.sinh), (inv_cosh, math.tanh), (inv_cosh, math.expm1),

    ]

