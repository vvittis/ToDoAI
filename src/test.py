"""
Created by: vasilisvittis
Date: 5/12/23
Project Name: ToDoSystem
"""


# TODO: check if y is not zero

def test_divide(x, y):
    div = x / y
    print(div)
    return div


# TODO: change x and y variables into float. Add print statement for div variable.

def test_divide_str(x, y):
    div = x / y
    print(div)
    return div


if __name__ == '__main__':
    x = 5
    y = 4
    test_divide(x, y)

    x = '5'
    y = '4'
    test_divide_str(x, y)
