from sympy import *
from random import random
delta = 0.000001
small_delta = 0.000000000001


def correct_expr(s: str) -> Expr:
    t = ''
    p = ''
    for i in s:
        if i == 'x' and '0' <= p <= '9':
            t += '*'
        t += (p := i)
    return sympify(t)


def find_root(e: Expr, d: Expr, l: float, r: float):
    global delta, small_delta
    try:
        x = symbols('x')
        y = l + (r - l) * random()
        p = y + 1.0
        i = 0
        while abs(y - p) > small_delta and i < 64:
            p = y
            y -= float(e.evalf(subs={x: y})) / float(d.evalf(subs={x: y}))
            i += 1
        return None if i == 64 or abs(float(e.evalf(subs={x: y}))) > delta else y
    except:
        return None


def find_roots(e: Expr, l: float, r: float) -> list[float]:
    global delta
    try:
        s = sorted(filter(lambda y: abs(y.imag) <
                   delta, (complex(x.evalf()) for x in solve(e))))
    except:
        s = []
    i = 0
    while i < len(s):
        if s[i] < l - delta or s[i] > r + delta or i and abs(s[i] - s[i - 1]) < delta:
            s.pop(i)
        else:
            i += 1
    d = diff(e)
    for i in range(32):
        x = find_root(e, d, l + (r - l) * i / 32, l + (r - l) * (i + 1) / 32)
        if x is None or x < l - delta or x > r + delta:
            continue
        c = True
        for y in s:
            if abs(y - x) < delta:
                c = False
                break
        if c:
            s.append(x)
    return sorted(s)


def answer_roots(s: str, l: float, r: float) -> list[float]:
    return find_roots(correct_expr(s), l, r)


def answer_min(s: str, l: float, r: float) -> list[tuple[float]]:
    e = correct_expr(s)
    a = find_roots(diff(e), l, r)
    x = symbols('x')
    d = diff(e, x, 2)
    b = []
    for r in a:
        try:
            if float(d.evalf(subs={x: r})) > 0.0:
                b.append((r, float(e.evalf(subs={x: r}))))
        except:
            pass
    return b


def answer_max(s: str, l: float, r: float) -> list[tuple[float]]:
    e = correct_expr(s)
    a = find_roots(diff(e), l, r)
    x = symbols('x')
    d = diff(e, x, 2)
    b = []
    for r in a:
        try:
            if float(d.evalf(subs={x: r})) < 0.0:
                b.append((r, float(e.evalf(subs={x: r}))))
        except:
            pass
    return b
