from fractions import gcd
from copy import deepcopy, copy

def rid_gcd(a):
    """a is an array of two entries. return the simpliefied number."""
    assert a[1] != 0
    g = gcd(a[0], a[1])
    if g != 0:
        return [a[0]/g, a[1]/g]
    return a

def subtract_mul(a, b, m):
    """a and b are 2 entry arrays, treat entries as numerator and denominator. 
    want, a - b*m, where m is also a tuple."""
    assert a[1] != 0 and b[1] != 0
    b[0], b[1] = (m[0] * b[0], m[1]* b[1])
    a, b = (a[0] * b[1], a[1]*b[1]), (b[0]*a[1], b[1]*a[1])
    c = [0,0]
    c[0] = a[0] - b[0]
    c[1] = a[1]
    return rid_gcd(c)

def lin_solver(m):
    """expects matrix entries to be tuples, numerator and denominator"""
    for r in range(1, len(m)+1):
        mul = copy(m[-r][-r])
        for c in range(0, len(m[-r])):
            if mul[0] != 0 and mul[1] != 0:
                m[-r][c]= ( m[-r][c][0] * mul[1], m[-r][c][1] * mul[0])
            elif mul[1] == 0:
                raise Exception("Yo, not possible to have only numerator or only denominator zero.")
            m[-r][c] = rid_gcd(m[-r][c])
            
        for r_l in range(0, len(m) - r):
            # skips the state i am currently in
            if r_l == len(m) - r:
                continue
            mul = m[r_l][-r][:]
            for c in range(0, len(m[-r])):
                m[r_l][c] = subtract_mul(m[r_l][c][:], m[-r][c][:], mul)
    return m
def sub_diag(m):
    """subtracts one from each entry in the diagonal """
    m = m[:]
    for i in range(0, len(m)):
        m[i][i] = subtract_mul(m[i][i], [1,1], [1,1])
    return m
    
def convert_to_tuples(m):
    """Converts the array to tuples, where every entry corresponds to a numerator denominator pair.
    Denominator is the sum of the entries of a row. Necessary to find probability to go into a state
    from a given state."""
    work_with = []
    for state in m:
        denom = sum(state)
        if denom == 0:
            denom = 1
        new_state = []
        for i in state:
            new_state.append((i, denom))
        work_with.append(new_state)
    return work_with

def lcm_of_array(a, should_negate=True):
    """Array of tuples. We want to return an array where all numbers are put under a common denominator
    and the denominator is in the last position of a. For example. a = [[1,2], [3,4]] as input gives
    [2, 3, 4] as an answer.
    If should_negate is true, we negate the numerators. Necessary for this specific problem."""
    print(a)
    lcm = a[0][1]
    for i in range(1, len(a)):
        lcm = lcm*a[i][1]/gcd(lcm,a[i][1])
    result = [-elem[0]*(lcm/elem[1]) for elem in a]
    result.append(lcm)
    return result

def compute(m):
"""m is the matrix for which to find the probabilities. As specified in the summary"""
    work_with = convert_to_tuples(m)
    answers = []
    for i in range(0, len(m)):
        if sum(m[i][:i]) + sum(m[i][i+1:]) == 0:
            m[i][i] = 0
        if sum(m[i]) == 0:
            temp_m = deepcopy(work_with)
            temp_m[i][i] = (1, 1) # to indicate that this state is the terminal state we are looking for
            temp_m = sub_diag(temp_m) # to solve for a b = [0, 0, ...]
            t = lin_solver(temp_m)
            answers.append(t[0][i])
    final_answer = lcm_of_array(answers)
    
    return final_answer
            