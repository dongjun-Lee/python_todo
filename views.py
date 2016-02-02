from tkinter import *
from tkinter.ttk import *
import tkinter.simpledialog
from controllers import *
from models import *
import operator
import tkinter.messagebox
import calendar
from datetime import datetime


list_view = None
calendar_view = None


class App(Frame):
    def __init__(self, master):
        # create a frame with the title and size
        self.master = master
        master.title("TODO Application")
        frame = Frame(master)
        frame.pack()

        global list_view, calendar_view
        list_view = ListView(self.master)
        calendar_view = CalendarView(self.master)

        # create a pulldown menu, and add it to the menu bar
        menu_bar = Menu(master)
        menu = Menu(menu_bar, tearoff=0)
        menu.add_command(label="List View", command=self.open_list_view)
        menu.add_command(label="Calendar View", command=self.open_calendar_view)
        menu_bar.add_cascade(label="Menu", menu=menu)

        # display the menu
        master.config(menu=menu_bar)

        # Add TODO button
        Button(master, text="Add TODO", command=self.add_todo_callback).pack(side=BOTTOM)

        self.is_list_view = False
        self.open_list_view()

    def open_list_view(self):
        global list_view, calendar_view
        list_view.show_list_view()
        calendar_view.hide_calendar_view()

    def open_calendar_view(self):
        global list_view, calendar_view
        list_view.hide_list_view()
        calendar_view.show_calendar_view()

    def add_todo_callback(self):
        InputDialog(self.master)


class InputDialog(tkinter.simpledialog.Dialog):
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
        calendar_view.load_list()


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

        if tkinter.messagebox.askyesno("Delete", "Delete this TODO item?"):
            for todo in self.todo_list:
                if clicked_list == todo.to_list():
                    self.todo_list.remove(todo)
            FileHandler.save_todo_list(self.todo_list)
            self.draw_list()
        else:
            pass

    def hide_list_view(self):
        self.treeview.pack_forget()

    def show_list_view(self):
        self.treeview.pack()


class CalendarView(Frame):
    def __init__(self, master):
        self.treeview = Treeview(master, padding=6)
        self.master = master
        self.year = datetime.now().year
        self.month = datetime.now().month

        self.prev_button = Button(self.master, text="prev", command=self.prev_callback)
        title = str(self.year) + "-" + str(self.month)
        self.title_label = Label(self.master, text=title)
        self.next_button = Button(self.master, text="next", command=self.next_callback)

        self.create_gui()
        self.load_list()

    def create_gui(self):
        self.treeview['columns'] = ("mon", 'tue', 'wed', 'thur', 'fri', 'sat', 'sun')
        self.treeview['show'] = 'headings'

        self.treeview.column("mon", anchor='center', width=70)
        self.treeview.heading("mon", text='Mon')
        self.treeview.column("tue", anchor='center', width=70)
        self.treeview.heading("tue", text='Tue')
        self.treeview.column("wed", anchor='center', width=70)
        self.treeview.heading("wed", text='Wed')
        self.treeview.column("thur", anchor='center', width=70)
        self.treeview.heading("thur", text='Thur')
        self.treeview.column("fri", anchor='center', width=70)
        self.treeview.heading("fri", text='Fri')
        self.treeview.column("sat", anchor='center', width=70)
        self.treeview.heading("sat", text='Sat')
        self.treeview.column("sun", anchor='center', width=70)
        self.treeview.heading("sun", text='Sun')

        self.treeview.bind("<Double-1>", self.on_double_clicked)

    def prev_callback(self):
        self.month -= 1
        if self.month == 0:
            self.month = 12
            self.year -=1
        self.draw_calendar(self.year, self.month)
        self.title_label.config(text=str(self.year) + "-" + str(self.month))

    def next_callback(self):
        self.month += 1
        if self.month == 13:
            self.month = 1
            self.year += 1
        self.draw_calendar(self.year, self.month)
        self.title_label.config(text=str(self.year) + "-" + str(self.month))

    def load_list(self):
        self.todo_list = FileHandler.load_todo_list()
        self.draw_calendar(self.year, self.month)

    def get_calendar(self, year, month):
        (first_day, last_date) = calendar.monthrange(year, month)

        calendar_matrix = []
        count = -first_day
        for i in range(6):
            calendar_matrix.append([""] * 7)

        for i in range(6):
            for j in range(7):
                count += 1
                if 0 < count <= last_date:
                    calendar_matrix[i][j] = str(count)

        for todo in self.todo_list:
            [todo_year, todo_month, todo_day] = todo.date.split("-")
            if int(todo_year) == year and int(todo_month) == month:
                # TODO : Add * at date
                i = int((int(todo_day) + first_day - 1) / 7)
                j = (int(todo_day) + first_day - 1) % 7
                calendar_matrix[i][j] += "*"

        return calendar_matrix

    def draw_calendar(self, year, month):
        calendar_matrix = self.get_calendar(year, month)
        self.treeview.delete(*self.treeview.get_children())
        for week in calendar_matrix:
            self.treeview.insert('', 'end', values=week)

    def on_double_clicked(self, event):
        clicked_item = self.treeview.focus()
        clicked_values = self.treeview.item(clicked_item).get('values')

        week_todo_str = ""
        for value in clicked_values:
            value = str(value)
            for todo in self.todo_list:
                [todo_year, todo_month, todo_day] = todo.date.split("-")
                if int(todo_year) == self.year and int(todo_month) == self.month \
                        and int(todo_day) == int(value.replace("*", "")):
                    week_todo_str += todo.to_string() + "\n"

        tkinter.messagebox.showinfo("This week's TODO", week_todo_str)

    def hide_calendar_view(self):
        self.treeview.pack_forget()

    def show_calendar_view(self):
        self.prev_button.pack(side=TOP)
        self.title_label.pack(side=TOP)
        self.next_button.pack(side=TOP)
        self.treeview.pack(side=BOTTOM)





