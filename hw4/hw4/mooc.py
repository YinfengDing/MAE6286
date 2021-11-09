"""Solutions of the assignment to compare with student answers."""

import numpy


def hw4_u_sample(val):
    ans, tol = [0.7264, 0.4681, 0.4272, 0.7899, 0.7133], 1e-2
    return numpy.allclose(val, ans, atol=tol, rtol=0.0)


def hw4_u_min(val):
    ans, tol = 0.2602, 1e-2
    return abs(val - ans) <= tol


def hw4_row_col(vals):
    ans = (76, 182)
    return all(v == a for v, a in zip(vals, ans))


def hw4_v_max(val):
    ans, tol = 0.3599, 1e-2
    return abs(val - ans) <= tol


prefix = 'hw4'
suffixes = ['u_sample', 'u_min', 'row_col', 'v_max']
dispatcher = {}
for suffix in suffixes:
    funcname = prefix + '_' + suffix
    dispatcher[funcname] = eval(funcname)


def check(funcname, val,
          print_res=True, return_res=False):
    res = dispatcher[funcname](val)
    if print_res:
        res_str = 'Good job!' if res else 'Try again!'
        print('[{}] {}'.format(funcname, res_str))
    if return_res:
        return res
