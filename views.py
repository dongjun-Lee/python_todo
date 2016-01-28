from Tkinter import *
from ttk import *
import tkSimpleDialog
from controllers import *
from models import *
import operator
import tkMessageBox


list_view = None


class InputDialog(tkSimpleDialog.Dialog):
    def body(self, master):
        Label(master, text="Date (YYYY-MM-DD) : ").grid(row=0)
        Label(master, text="Start time (HH:MM) : ").grid(row=1)
        Label(master, text="End time (HH:MM) : ").grid(row=2)
        Label(master, text="Content : ").grid(row=3)
        Label(master, text="Priority : ").grid(row=4)

        self.date_edit = Entry(master)
        self.start_time_edit = Entry(master)
        self.end_time_edit = Entry(master)
        self.content_edit = Entry(master)
        self.priority_edit = Entry(master)

        self.date_edit.grid(row=0, column=1)
        self.start_time_edit.grid(row=1, column=1)
        self.end_time_edit.grid(row=2, column=1)
        self.content_edit.grid(row=3, column=1)
        self.priority_edit.grid(row=4, column=1)

        return self.date_edit

    def apply(self):
        date = str(self.date_edit.get())
        start_time = str(self.start_time_edit.get())
        end_time = str(self.end_time_edit.get())
        content = str(self.content_edit.get())
        priority = str(self.priority_edit.get())

        new_todo = Todo(date=date, start_time=start_time, end_time=end_time, content=content, priority=priority)
        FileHandler.save_todo(new_todo)
        global list_view
        list_view.load_list()


class App(Frame):
    def __init__(self, master):
        # create a frame with the title and size
        self.master = master
        master.title("TODO Application")
        frame = Frame(master)
        frame.pack()

        # create a pulldown menu, and add it to the menu bar
        menu_bar = Menu(master)
        menu = Menu(menu_bar, tearoff=0)
        menu.add_command(label="List View", command=self.open_list_view)
        menu.add_command(label="Calendar View", command=self.open_calendar_view)
        menu_bar.add_cascade(label="Menu", menu=menu)

        # display the menu
        master.config(menu=menu_bar)

        # Add TODO button
        Button(master, text="Add TODO", command=self.add_todo_callback).pack(side=TOP)

        self.is_list_view = False
        self.open_list_view()

    def open_list_view(self):
        if not self.is_list_view:
            global list_view
            list_view = ListView(self.master)
            self.is_list_view = True

    def open_calendar_view(self):
        # TODO
        pass

    def add_todo_callback(self):
        InputDialog(self.master)


class ListView(Frame):
    def __init__(self, master):
        self.treeview = Treeview(master)
        self.master = master
        self.create_gui()
        self.load_list()

    def create_gui(self):
        self.treeview['columns'] = ("date", 'start_time', 'end_time', 'content', 'priority')
        self.treeview['show'] = 'headings'

        self.treeview.column("date", anchor='center', width=80)
        self.treeview.heading("date", text='Date', command=lambda: self.sort_list('date'))
        self.treeview.column('start_time', anchor='center', width=80)
        self.treeview.heading('start_time', text='Start Time')
        self.treeview.column('end_time', anchor='center', width=80)
        self.treeview.heading('end_time', text='End Time')
        self.treeview.column('content', anchor='center', width=200)
        self.treeview.heading('content', text='Content')
        self.treeview.column('priority', anchor='center', width=50)
        self.treeview.heading('priority', text='Priority', command=lambda: self.sort_list('priority'))
        self.treeview.pack()

        self.treeview.bind("<Double-1>", self.on_double_clicked)

    def draw_list(self):
        self.treeview.delete(*self.treeview.get_children())
        for todo in self.todo_list:
            self.treeview.insert('', 'end',
                                 values=(todo.date, todo.start_time, todo.end_time, todo.content, todo.priority))

    def load_list(self):
        self.todo_list = FileHandler.load_todo_list()
        self.draw_list()

    def sort_list(self, column_name):
        self.todo_list.sort(key=operator.attrgetter(column_name))
        self.draw_list()

    def on_double_clicked(self, event):
        clicked_item = self.treeview.focus()
        clicked_values = self.treeview.item(clicked_item).get('values')
        clicked_list = map(lambda x: str(x), clicked_values)

        if tkMessageBox.askyesno("Delete", "Delete this TODO item?"):
            for todo in self.todo_list:
                if clicked_list == todo.to_list():
                    self.todo_list.remove(todo)
            FileHandler.save_todo_list(self.todo_list)
            self.draw_list()
        else:
            pass