import os
import os.path
import pickle
import tkinter as tk
import ttkbootstrap as ttk
from custom_widgets import CustomDateEntry
from tkinter.font import Font
from datetime import date


class ToDoApp(ttk.Window):
    app_file_path = os.path.dirname(__file__)
    main_path = os.path.dirname(app_file_path)
    icon_path = os.path.join(main_path, 'data', 'blank_icon.png')
    theme_path = os.path.join(main_path, 'data', 'app_theme.json')

    def __init__(self):
        super().__init__()
        self.geometry('600x530')
        self.title('TO-DO LIST')
        self.resizable(False, False)
        if os.path.isfile(ToDoApp.icon_path):
            icon = tk.PhotoImage(file=ToDoApp.icon_path)
            self.iconphoto(False, icon)
            self.iconphoto(True, icon)

        # set app style
        self.main_font = Font(family='Verdana', size=12)
        self.app_style = ttk.Style()
        try:
            self.app_style.load_user_themes(ToDoApp.theme_path)
            self.app_style.theme_use(themename='todo_theme')
            self.theme_file_check = True
        except FileNotFoundError:
            self.app_style.theme_use(themename='flatly')
            self.theme_file_check = False
        self.app_style.configure(style='TButton', font=self.main_font)

        # set tasks variables
        self.data_dict_var = {}
        self.data_dict_items_list = []
        self.data_task_list = []
        self.task_index = None

        # set task entry variable
        self.task_string_var = ttk.StringVar()
        self.date_var = date.today().strftime('%Y-%m-%d')

        # load tasks and set task list variable
        self.load_task_from_file()
        self.task_list_var = tk.Variable(value=self.data_task_list)

        # create layout
        self.frame_date_selection()
        self.frame_new_task()
        self.frame_task_list()
        self.frame_task_options()

        # configure title bar's X button action
        self.protocol('WM_DELETE_WINDOW', self.exit_by_x)

        # bind ESCAPE key press
        self.bind('<KeyPress-Escape>', lambda event: self.widgets_reset())

        # run app
        self.mainloop()

    def frame_date_selection(self):
        frame = ttk.Frame(self)

        self.date_label = ttk.Label(frame, text='Select date:', font=self.main_font, anchor='center')
        self.date_label.pack(side='left', padx=3)

        self.calendar_button = CustomDateEntry(frame, width=10, bootstyle='secondary', firstweekday=0)
        self.calendar_button.button_focus_disable()
        if self.theme_file_check:
            self.calendar_button.entry_configure('primary', self.main_font)
        else:
            self.calendar_button.entry_configure('secondary', self.main_font)
        self.calendar_button.pack(side='left', expand=True, padx=5)

        self.select_date_button = ttk.Button(
            frame,
            text='Show tasks',
            bootstyle='secondary-TButton',
            takefocus=False,
            command=self.load_task_for_date
        )
        self.select_date_button.pack(side='right')

        frame.pack(side='top', padx=15, pady=15, fill='x')

    def frame_new_task(self):
        frame = ttk.Frame(self)

        self.add_label = ttk.Label(frame, text='New:', font=self.main_font)
        self.add_label.pack(side='left', padx=3)

        self.new_task_field = ttk.Entry(frame, font=self.main_font, textvariable=self.task_string_var)
        self.new_task_field.pack(side='left', padx=10, fill='x', expand=True)
        self.new_task_field.bind('<Return>', lambda event: self.add_new_task())

        self.add_task_button = ttk.Button(
            frame,
            text='Add',
            bootstyle='secondary-TButton',
            takefocus=False,
            command=self.add_new_task
        )
        self.add_task_button.pack(side='right')

        frame.pack(side='top', padx=15, fill='x')

    def frame_task_list(self):
        frame = ttk.Frame(self)

        self.date_label = ttk.Label(frame, text=f'Tasks for day {self.date_var}', font=self.main_font)
        self.date_label.pack(side='top', fill='x')

        self.task_list = tk.Listbox(
            frame,
            listvariable=self.task_list_var,
            selectmode=tk.SINGLE,
            height=11,
            font=self.main_font,
        )
        self.load_completed_task()

        self.task_list_scrollbar = tk.Scrollbar(self.task_list, orient='vertical', command=self.task_list.yview)
        self.task_list.configure(yscrollcommand=self.task_list_scrollbar.set)
        self.task_list_scrollbar_update()
        self.task_list.pack(side='top', fill='x')

        self.task_list.bind('<<ListboxSelect>>', self.task_completion_and_edit_button_update)
        self.task_list.bind('<Delete>', lambda event: self.delete_task())

        frame.pack(side='top', padx=40, pady=15, fill='x')

    def frame_task_options(self):
        frame = ttk.Frame(self, height=45)

        self.task_completion_button = ttk.Button(
            frame,
            text='Task done',
            bootstyle='secondary-TButton',
            takefocus=False,
            state='disabled',
            width=11,
            command=self.task_completion_button_action
        )
        self.task_completion_button.place(relx=0, rely=0.5, anchor='w')

        self.edit_task_button = ttk.Button(
            frame,
            text='Edit task',
            bootstyle='secondary-TButton',
            takefocus=False,
            width=11,
            state='disabled',
            command=self.edit_button_action
        )
        self.edit_task_button.place(relx=0.5, rely=0.5, anchor='center')

        self.delete_task_button = ttk.Button(
            frame,
            text='Delete task',
            bootstyle='secondary-TButton',
            takefocus=False,
            width=11,
            state='disabled',
            command=self.delete_task
        )
        self.delete_task_button.place(relx=1, rely=0.5, anchor='e')

        frame.pack(side='top', padx=40, pady=5, fill='x')

    def task_list_scrollbar_update(self):
        if len(self.data_task_list) > 11:
            self.task_list_scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
        else:
            self.task_list_scrollbar.place_forget()

    def add_new_task(self):
        if self.task_string_var.get() != '':
            self.data_dict_items_list.append([self.task_string_var.get().strip(), False])
            self.data_task_list.append(self.task_string_var.get().strip())
            self.task_list_var.set(self.data_task_list)
            self.task_string_var.set('')
            self.task_list_scrollbar_update()
            self.task_list.select_clear(0, 'end')
            self.widgets_reset()

    def delete_task(self):
        if self.task_list.curselection() != ():
            task_idx = self.task_list.curselection()[0]
            del self.data_dict_items_list[task_idx]
            del self.data_task_list[task_idx]
            self.task_list_var.set(self.data_task_list)
            self.load_completed_task()
            self.task_list_scrollbar_update()
            self.widgets_reset(erase=False)

    def task_completion_button_action(self):
        if self.task_list.curselection() != ():
            task_idx = self.task_list.curselection()[0]
            if self.data_dict_items_list[task_idx][1]:
                self.data_dict_items_list[task_idx][1] = False
                self.data_dict_items_list[task_idx][0] = self.data_dict_items_list[task_idx][0][2:]
                self.data_task_list[task_idx] = self.data_task_list[task_idx][2:]
                self.task_list_var.set(self.data_task_list)
                self.task_completion_undo_format()
            else:
                self.data_dict_items_list[task_idx][1] = True
                self.data_dict_items_list[task_idx][0] = '\u2713 ' + self.data_dict_items_list[task_idx][0]
                self.data_task_list[task_idx] = '\u2713 ' + self.data_task_list[task_idx]
                self.task_list_var.set(self.data_task_list)
                self.task_completion_format()
            self.task_list.select_clear(0, 'end')
        self.widgets_reset(erase=False)

    def task_completion_and_edit_button_update(self, event):
        if len(self.data_task_list) > 0 and event.widget.curselection():
            task_idx = self.task_list.curselection()[0]
            self.task_completion_button.configure(state='enabled')
            self.edit_task_button.configure(state='enabled')
            self.delete_task_button.configure(state='enabled')
            if self.data_dict_items_list[task_idx][1]:
                self.task_completion_button.configure(text='Uncheck task')
            else:
                self.task_completion_button.configure(text='Task done')

    def load_completed_task(self):
        for idx, item in enumerate(self.data_dict_items_list):
            self.task_list.selection_set(idx)
            if item[1]:
                self.task_completion_format()
            else:
                self.task_completion_undo_format()
            self.task_list.select_clear(idx)

    def task_completion_format(self):
        task_idx = self.task_list.curselection()[0]
        self.task_list.itemconfig(
            task_idx,
            fg='#efefef',
            selectforeground='#252525',
            selectbackground='#95a5a6'
        )

    def task_completion_undo_format(self):
        task_idx = self.task_list.curselection()[0]
        self.task_list.itemconfig(
            task_idx,
            fg='#212529',
            selectbackground='#95a5a6'
        )

    def load_task_from_file(self):
        file_path = os.path.join(ToDoApp.main_path, 'data', 'app_data')
        file = f'task_data_{self.date_var[:4]}_{self.date_var[5:7]}.dat'
        if os.path.exists(file_path) and os.path.isfile(os.path.join(file_path, file)):
            with open(os.path.join(file_path, file), 'rb') as f:
                self.data_dict_var = pickle.load(f)
            self.data_dict_items_list = self.data_dict_var.get(self.date_var, [])
            self.data_task_list = [item[0] for item in self.data_dict_items_list]
        else:
            self.data_dict_var = {}
            self.data_dict_items_list = []
            self.data_task_list = []

    def save_task_to_file(self):
        self.data_dict_var_update()
        file_path = os.path.join(ToDoApp.main_path, 'data', 'app_data')
        file = f'task_data_{self.date_var[:4]}_{self.date_var[5:7]}.dat'
        if len(self.data_dict_var) > 0:
            if not os.path.exists(file_path):
                os.mkdir(file_path)
            with open(os.path.join(file_path, file), 'wb') as f:
                pickle.dump(self.data_dict_var, f)
        else:
            if os.path.exists(file_path) and os.path.isfile(os.path.join(file_path, file)):
                os.remove(os.path.join(file_path, file))

    def load_task_for_date(self):
        self.widgets_reset(erase=False)
        # check if year and month change
        if self.date_var[:7] == self.calendar_button.entry.get()[:7]:
            self.data_dict_var_update()
            self.date_var = self.calendar_button.entry.get()
            self.data_dict_items_list = self.data_dict_var.get(self.date_var, [])
            self.data_task_list = [item[0] for item in self.data_dict_items_list]
            self.task_list_var.set(self.data_task_list)
            self.load_completed_task()
        else:
            self.save_task_to_file()
            self.date_var = self.calendar_button.entry.get()
            self.load_task_from_file()
            self.task_list_var.set(self.data_task_list)
            self.load_completed_task()
        self.date_label.configure(text=f'Tasks for day {self.date_var}')

    def data_dict_var_update(self):
        size = len(self.data_dict_items_list)
        if size > 0:
            self.data_dict_var[self.date_var] = self.data_dict_items_list
        elif size == 0 and self.date_var in self.data_dict_var:
            del self.data_dict_var[self.date_var]

    def exit_by_x(self):
        self.save_task_to_file()
        self.destroy()

    def edit_button_action(self):
        # set index variable and widgets display configuration
        self.task_index = self.task_list.curselection()[0]
        self.task_completion_button.configure(state='disabled')
        self.delete_task_button.configure(state='disabled')
        self.select_date_button.configure(state='disabled')
        self.task_list.configure(state='disabled')
        self.add_label.configure(text='Task:')
        self.calendar_button.configure(state='disabled')
        self.edit_task_button.configure(text='Cancel editing')
        self.add_task_button.configure(text='Edit')
        
        # set commands to add and edit buttons
        self.add_task_button.configure(command=self.edit_task)
        self.edit_task_button.configure(command=lambda: self.widgets_reset(erase=False))

        # override binding
        self.new_task_field.bind('<Return>', lambda event: self.edit_task())

        # set task entry variable
        if self.data_dict_items_list[self.task_index][1]:
            self.task_string_var.set(self.task_list.get(self.task_index)[2:])
        else:
            self.task_string_var.set(self.task_list.get(self.task_index))

    def widgets_reset(self, erase=True):
        # reset widgets display configuration
        self.task_index = None
        self.task_completion_button.configure(text='Task done')
        self.task_completion_button.configure(state='disabled')
        self.delete_task_button.configure(state='disabled')
        self.select_date_button.configure(state='enabled')
        self.task_list.configure(state='normal')
        self.add_label.configure(text='New:')
        self.calendar_button.configure(state='normal')
        self.edit_task_button.configure(text='Edit')
        self.edit_task_button.configure(state='disabled')
        self.add_task_button.configure(text='Add')
        self.task_list.select_clear(0, 'end')

        # reset commands to add and edit buttons
        self.add_task_button.configure(command=self.add_new_task)
        self.edit_task_button.configure(command=self.edit_button_action)

        # override (reset) binding
        self.new_task_field.bind('<Return>', lambda event: self.add_new_task())

        # reset task entry variable
        if erase:
            self.task_string_var.set('')

    def edit_task(self):
        if self.task_string_var.get() != '':
            if self.data_dict_items_list[self.task_index][1]:
                task_text = '\u2713 ' + self.task_string_var.get().strip()
            else:
                task_text = self.task_string_var.get().strip()
            self.data_dict_items_list[self.task_index][0] = task_text
            self.data_task_list[self.task_index] = task_text
            self.task_list_var.set(self.data_task_list)
            self.task_list_scrollbar_update()
        self.widgets_reset()
