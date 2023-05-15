import os
from itertools import groupby
from itertools import groupby
from operator import itemgetter
from transformers import pipeline
import openai
from collections import defaultdict
from scan import scan, progress_bar

GUARANTEE = 0.9


def print_hi(name):
    openai.api_key = open("../plugin/key.txt", "r").read().strip('\n')

    todo_assignments = scan()  # finds all the to-dos in the .py files under the /src/ folder
    todo_history = []
    print("\nProducing Code Suggestions...")
    progress_bar(0, (len(todo_assignments)))
    for index, todo in enumerate(todo_assignments):
        progress_bar(index + 1, len(todo_assignments) + 1)

        message_history = []
        guarantee = 0
        while True:
            if guarantee > GUARANTEE:
                break
            user_input = " I want to " + todo['todo_statement'] + " to this function \n" + todo['function'] + \
                         " I want only the code so it ready to be executed and with no descriptions."
            # print("User's input was >: \n", user_input)
            message_history.append({"role": "user", "content": user_input})

            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=message_history
            )

            # print(completion)
            reply_content_code = completion.choices[0].message.content

            message_history.append({"role": "assistant", "content": reply_content_code})
            # print(reply_content_code)
            # code = reply_content.split('```')

            user_input = 'Give one sentence description of the changes you made.'
            message_history.append({"role": "user", "content": user_input})
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=message_history
            )
            reply_content_description = completion.choices[0].message.content
            # print(reply_content_description)
            message_history.append({"role": "assistant", "content": reply_content_description})
            reply = {"file": todo['file'], "todo_code": reply_content_code, "todo_description": reply_content_description}
            todo_history.append(reply)
            guarantee = evaluate_answer(reply)
    print("\n")
    files = sorted(todo_history, key=itemgetter('file'))
    directory = os.getcwd() + "/temp/"
    target_directory = os.path.dirname(os.getcwd()) + '/src/'
    # Display data grouped by grade
    for key, value in groupby(files, key=itemgetter('file')):
        file_name = str(key) + '.py'
        ai_filename = directory + "ai_" + file_name
        for k in value:
            os.makedirs(os.path.dirname(ai_filename), exist_ok=True)
            with open(ai_filename, "a+") as f:
                f.write("\n # TODO_RESOLVED:" + k['todo_description'] + "\n")
                f.write(k['todo_code'].replace("```", "").replace("python", "") + "\n")
        statement = "./pycharm merge " + target_directory + file_name + " " + ai_filename + " " + target_directory + file_name
        # print(statement)
        os.chdir("/Users/vasilisvittis/Library/Application Support/JetBrains/Toolbox/apps/PyCharm-P/ch-0/231.8770.66/PyCharm.app/Contents/MacOS")
        os.system(statement)
        os.remove(ai_filename)
    os.rmdir(directory)

    # printing result


def evaluate_answer(reply):
    guarantee = 1

    """
    logic
    """

    return guarantee


if __name__ == '__main__':
    print_hi('PyCharm')
