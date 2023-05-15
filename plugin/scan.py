"""
Created by: vasilisvittis
Date: 5/12/23scan
Project Name: ToDoSystem
"""
import glob
import inspect
import os
from datetime import datetime
import importlib


def scan():
    directory = os.path.dirname(os.getcwd()) + '/src/'

    # print(directory)

    path = r'' + directory + '*.py'
    files = []
    files = glob.glob(directory + '/**/*.py', recursive=True)

    # print(files)
    to_dos = []
    todo_word = '# TODO:'
    def_word = 'def'
    print("\nScanning Files...")
    progress_bar(0, (len(files)))
    for index, file in enumerate(files):
        progress_bar(index + 1, len(files))

        find = False
        sub_file = file.rfind("/")
        file_name = file[sub_file + 1:-3]
        mymodule = importlib.import_module(file_name)
        with open(r'' + file, 'r') as fp:

            # reosad all lines in a list
            lines = fp.readlines()
            for line in lines:
                # check if string present on a current line
                if line.find(todo_word) != -1:
                    find = True
                    # print(todo_word, 'string exists in file ' + file)
                    # print('Line Number:', lines.index(line))
                    # print('Line:', line)
                    todo_statement = line[8:].strip('\n')
                if find:
                    if line.find(def_word) != -1:
                        find = False
                        # print('Line:', line)
                        function_line = line.strip('\n')
                        # print(function_line[4:])
                        end_point = function_line.find("(")
                        function_name = function_line[4:end_point]
                        bar = getattr(mymodule, function_name)
                        i = inspect.getsource(bar).index('\n')
                        j = inspect.getsource(bar).rindex(':', 0, i)
                        # print(inspect.getsource(bar)[j + 1:])
                        function_descr = function_line + inspect.getsource(bar)[j + 1:]
                        to_dos.append({'file': file_name, 'todo_statement': todo_statement, 'function': function_descr})
    # print(to_dos)
    return to_dos


if __name__ == '__main__':
    scan()
    # i = inspect.getsource(hello_world).index('\n')
    # j = inspect.getsource(hello_world).rindex(':', 0, i)
    #
    # print(inspect.getsource(hello_world)[j + 1:])


# # TODO: change now variable into string
# def test_date():
#     now = datetime.datetime.now()
#     print(now)
#     return now


# # TODO check if y is not zero
# def test_divide(x, y):
#     div = x / y
#     print(div)
#     return div


# # TODO change x and y variables into float. Add print statement for div variable.
# def test_divide_str(x, y):
#     div = x / y
#     print(div)
#     return div

def progress_bar(progress, total):
    percent = 100 * (progress / float(total))
    bar = '█' * int(percent) + '-' * (100 - int(percent))
    print(f"\r|{bar}| {percent:.2f}%", end="\r")
