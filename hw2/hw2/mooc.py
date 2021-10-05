"""Solutions of the traffic flow assignment."""


def hw2_answer1(val):
    ans, tol = 12.50, 1e-2
    return abs(val - ans) <= tol


def hw2_answer2(val):
    ans, tol = 21.6089, 1e-2
    return abs(val - ans) <= tol


def hw2_answer3(val):
    ans, tol = 17.3213, 1e-2
    return abs(val - ans) <= tol


def hw2_answer4(val):
    ans, tol = 30.7147, 1e-2
    return abs(val - ans) <= tol


def hw2_answer5(val):
    ans, tol = 18.0556, 1e-2
    return abs(val - ans) <= tol


def hw2_answer6(val):
    ans, tol = 27.9235, 1e-2
    return abs(val - ans) <= tol


def hw2_answer7(val):
    ans, tol = 23.4970, 1e-2
    return abs(val - ans) <= tol


def hw2_answer8(val):
    ans, tol = 22.6733, 1e-2
    return abs(val - ans) <= tol


dispatcher = {'hw2_answer1': hw2_answer1, 'hw2_answer2': hw2_answer2,
              'hw2_answer3': hw2_answer3, 'hw2_answer4': hw2_answer4,
              'hw2_answer5': hw2_answer5, 'hw2_answer6': hw2_answer6,
              'hw2_answer7': hw2_answer7, 'hw2_answer8': hw2_answer8}


def check(funcname, val,
          print_res=True, return_res=False):
    res = dispatcher[funcname](val)
    if print_res:
        res_str = 'Good job!' if res else 'Try again!'
        print('[{}] {}'.format(funcname, res_str))
    if return_res:
        return res
