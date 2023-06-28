# ToDoList Application

ToDo List GUI Application made with ttkbootstrap.

Simple To Do List app with options to add, edit, mark completion and delete tasks. 
App allows user to choose date from callendar and save tasks for each choosen day separately.
Tasks are beeing saved in files (separate file for each month) and are loaded/saved automatically when opening/closing, app and when selecting tasks for different month.


## Setup
Python version: 3.7 and later.

Required modules:
* ttkbootstrap 1.10.1
* Pillow 9.5.0

To install required modules use `requirements.txt` file. In terminal type:
```bash
python -m pip install -r requirements.txt
```


## How to run

To run application from terminal from main directory type:
```bash
python todolist
```

`__main__.py` file will initiate application automatically.

To run application from terminal directly from file type:
```bash
python todolist\todolist.py
```


## Usage

### Add new task:
To add new task type task in Entry Field and press "Add" button or press "Enter" key.

### Check/uncheck task completion:
To check/uncheck task completion select task from list and press "Task done"/"Uncheck task" button.
(The button label and the appearance of the task depends on the status of the task completion, and will change automatically after pressing the button.)

### Delete task:
To delete existing task select task from list and press "Delete" button or press "Delete" key.

### Edit task:
To edit existing task select task from list and press "Edit" button. Task text will show in Entry Field.
Edit task in Entry Field and press "Edit" button.

### Cancel task editing:
To cancel task editing press "Cancel editing" button or press "Escape" key.

### Select date:
To show tasks for different date press callendar button. New window with callendar will appear.
In new window select desired date. Window will close automatically and new date will show in Date Entry Field.
Press "Show tasks" button to load tasks for selected date.

### Reset app state:
To reset buttons, labels and entry fields state while adding or editing new task, and to uncheck selected task from list press "Escape" key.


### Sample tasks
Sample tasks were added on date 2023-06-12 to 2023-06-14.


## License

This project is licensed under the MIT License - see the LICENSE.md file for details.