from models import *


class FileHandler:
    FILE_NAME = "todo.txt"

    @classmethod
    def save_todo(cls, todo):
        todo_file = open(cls.FILE_NAME, 'a')
        todo_file.write(todo.to_string() + "\n")
        todo_file.close()

    @classmethod
    def save_todo_list(cls, todo_list):
        todo_file = open(cls.FILE_NAME, 'w')
        for todo in todo_list:
            todo_file.write(todo.to_string() + "\n")
        todo_file.close()

    @classmethod
    def load_todo_list(cls):
        todo_file = open(cls.FILE_NAME, 'r')
        todo_list = []

        line = todo_file.readline()
        while line:
            date = line.split(Todo.DIVIDER)[0]
            start_time = line.split(Todo.DIVIDER)[1]
            end_time = line.split(Todo.DIVIDER)[2]
            content = line.split(Todo.DIVIDER)[3]
            priority = line.split(Todo.DIVIDER)[4]

            todo = Todo(date=date, start_time=start_time, end_time=end_time, content=content, priority=priority)
            todo_list.append(todo)
            line = todo_file.readline()

        return todo_list
