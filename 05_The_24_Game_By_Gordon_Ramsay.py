# Prog-05: The Fucking 24 Game
# 645645645646456555655645645654564312156415619489189456 Name Gordon Ramsay

from itertools import permutations, product
# import ทำไมวะงง ไม่เห็นต้องใช้
import math


def generate_all_combinations(num_list, operators):
    all_combi = []
    for n, o in product(sorted(set(permutations(num_list))),
                        product(operators, repeat=3)):
        x = [None] * (len(n) + len(o))
        x[::2] = n
        x[1::2] = o
        all_combi.append(x)
    return all_combi


# เป็นเหี้ยไรกับขีด

# Possible parentheses form
# ( ( 1 + 2 ) + 3 ) + 4
# ( 1 + ( 2 + 3 ) ) + 4
# ( 1 + 2 ) + ( 3 + 4 )
# 1 + ( ( 2 + 3 ) + 4 )
# 1 + ( 2 + ( 3 + 4 ) )

def calculate_parentheses(cases):
    """Calculate all cases in parameter 'cases'
    return : case that calculate and it's 24 else return 'No Solutions'

    Example and Doctest :
    >>> nums = [5, 5, 9, 5]
    >>> cases = generate_all_combinations(nums, '+-*/')
    >>> calculate_parentheses(cases)
    '( ( 5 + 5 ) + 5 ) + 9 = 24'
    >>> nums = [13, 2, 13, 13]
    >>> cases = generate_all_combinations(nums, '+-*/')
    >>> calculate_parentheses(cases)
    '2 * ( 13 - ( 13 / 13 ) ) = 24'
    >>> nums = [1, 1, 2, 7]
    >>> cases = generate_all_combinations(nums, '+-*/')
    >>> calculate_parentheses(cases)
    '( 1 + 2 ) * ( 1 + 7 ) = 24'
    >>> nums = [200, -120, 10, 3]
    >>> cases = generate_all_combinations(nums, '+-*/')
    >>> calculate_parentheses(cases)
    '( ( -120 + 200 ) * 3 ) / 10 = 24'
    >>> nums = [1, 1, 1, 9]
    >>> cases = generate_all_combinations(nums, '+-*/')
    >>> calculate_parentheses(cases)
    'No Solutions'
    >>> # Check case that can occured 'divided by zero' problem
    >>> nums = [13, 13, 13, 13]
    >>> cases = generate_all_combinations(nums, '+-*/')
    >>> calculate_parentheses(cases)
    'No Solutions'
    """
    # Use try except because some combination are error because 'divided by zero'
    for i in cases:
        case_to_calculate = i
        num1 = case_to_calculate[0]
        operation1 = case_to_calculate[1]
        num2 = case_to_calculate[2]
        operation2 = case_to_calculate[3]
        num3 = case_to_calculate[4]
        operation3 = case_to_calculate[5]
        num4 = case_to_calculate[6]

        # I use different variable name to make you read a program easier

        # Case 1 : ( ( num1 'operation1' num2 ) 'operation2' num3 ) 'operation3' num4
        case1 = f"( ( {num1} {operation1} {num2} ) {operation2} {num3} ) {operation3} {num4} = 24"
        try :
            calc1 = calc(num1, operation1, num2)
            calc1 = calc(calc1, operation2, num3)
            calc1 = calc(calc1, operation3, num4)
        except ZeroDivisionError:
            calc1 = 0
        if calc1 == 24:
            return case1

        # Case 2 : ( num1 'operation1' ( num2 'operation2' num3 ) ) 'operation3' num4
        case2 = f"( {num1} {operation1} ( {num2}  {operation2} {num3} ) ){operation3} {num4} = 24"
        try :
            calc2 = calc(num2, operation2, num3)
            calc2 = calc(num1, operation1, calc2)
            calc2 = calc(calc2, operation3, num4)
        except ZeroDivisionError:
            calc2 = 0
        if calc2 == 24:
            return case2

        # Case 3 : ( num1 'operation1' num2 ) 'operation2' ( num3 'operation3' num4 )
        case3 = f"( {num1} {operation1} {num2} ) {operation2} ( {num3} {operation3} {num4} ) = 24"
        try:
            calc31 = calc(num1, operation1, num2)
            calc32 = calc(num3, operation3, num4)
            calc3 = calc(calc31, operation2, calc32)
        except ZeroDivisionError:
            calc3 = 0
        if calc3 == 24:
            return case3

        # Case 4 : num1 'operation1' ( ( num2 'operation2' num3 ) 'operation3' num4 )
        case4 = f"{num1} {operation1} ( ( {num2} {operation2} {num3} ) {operation3} {num4} ) = 24"
        try:
            calc4 = calc(num2, operation2, num3)
            calc4 = calc(calc4, operation3, num4)
            calc4 = calc(num1, operation1, calc4)
        except ZeroDivisionError:
            calc4 = 0
        if calc4 == 24:
            return case4

        # Case 5 : num1 'operation1' ( num2 'operation2' ( num3 'operation3' num4 ) )
        case5 = f"{num1} {operation1} ( {num2} {operation2} ( {num3} {operation3} {num4} ) ) = 24"
        try :
            calc5 = calc(num3, operation3, num4)
            calc5 = calc(num2, operation2, calc5)
            calc5 = calc(num1, operation1, calc5)
        except ZeroDivisionError:
            calc5 = 0
        if calc5 == 24:
            return case5

    return 'No Solutions'



# calc function for you with doctest
def calc(num1, op, num2):
    """Return a result for operation between num1 and num2

    Examples and Doctest :
    >>> calc(2, "+", 3)
    5
    >>> calc(2, "-", 3)
    -1
    >>> calc(2, "*", 3)
    6
    >>> calc(2, "/", 2)
    1.0

    """
    if op == "+":
        return num1 + num2
    elif op == "-":
        return num1 - num2
    elif op == "*":
        return num1 * num2
    elif op == "/":
        return num1 / num2


# เป็นเหี้ยไรกับขีด

# I write to support error when some idiot not write 4 numbers
nums = input('Enter 4 integers: ').split()
if len(nums) != 4:
    print(f"Hey, an idiot sandwich! How dare you write {len(nums)} numbers instead of 4 numbers! Fuck off!")
else :
    for i in range(len(nums)):
        nums[i] = int(nums[i])
    cases = generate_all_combinations(nums, '+-*/')
    print(calculate_parentheses(cases))

