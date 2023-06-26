import ttkbootstrap as ttk
from ttkbootstrap.widgets import DateEntry
from ttkbootstrap.dialogs import Querybox, DatePickerDialog
from ttkbootstrap.constants import *
from tkinter import END
from datetime import datetime


class CustomDateEntry(DateEntry):
    def _configure_set(self, **kwargs):
        """Override configure method to allow for setting custom
        DateEntry parameters"""

        if "state" in kwargs:
            state = kwargs.pop("state")
            if state in ["readonly", "invalid"]:
                self.entry.configure(state=state)
            elif state in ("disabled", "normal"):
                self.entry.configure(state=state)
                self.button.configure(state=state)
            else:
                kwargs[state] = state
        if "dateformat" in kwargs:
            self._dateformat = kwargs.pop("dateformat")
        if "firstweekday" in kwargs:
            self._firstweekday = kwargs.pop("firstweekday")
        if "startdate" in kwargs:
            self._startdate = kwargs.pop("startdate")
        if "bootstyle" in kwargs:
            self._bootstyle = kwargs.pop("bootstyle")
            # disable Entry field bootstyle definition
            # self.entry.configure(bootstyle=self._bootstyle)
            self.button.configure(bootstyle=[self._bootstyle, "date"])
        if "width" in kwargs:
            width = kwargs.pop("width")
            self.entry.configure(width=width)

        super(ttk.Frame, self).configure(**kwargs)

    # methode to configure bootstyle for Entry field
    def entry_configure(self, bootstyle: str, font):
        self.entry.configure(bootstyle=bootstyle)
        self.entry.configure(font=font)

    def button_focus_disable(self):
        self.button.configure(takefocus=False)

    def _on_date_ask(self):
        """Callback for pushing the date button"""
        _val = self.entry.get() or datetime.today().strftime(self._dateformat)
        try:
            self._startdate = datetime.strptime(_val, self._dateformat)
        except Exception as e:
            print("Date entry text does not match", self._dateformat)
            self._startdate = datetime.today()
            self.entry.delete(first=0, last=END)
            self.entry.insert(
                END, self._startdate.strftime(self._dateformat)
            )

        old_date = datetime.strptime(_val, self._dateformat)

        # get the new date and insert into the entry
        new_date = CustomQuerybox.get_date(
            parent=self.entry,
            startdate=old_date,
            firstweekday=self._firstweekday,
            bootstyle=self._bootstyle,
        )
        self.entry.delete(first=0, last=END)
        self.entry.insert(END, new_date.strftime(self._dateformat))
        self.entry.focus_force()


class CustomQuerybox(Querybox):
    @staticmethod
    def get_date(
            parent=None,
            title=" ",
            firstweekday=6,
            startdate=None,
            bootstyle="secondary",
    ):
        """Shows a calendar popup and returns the selection.

        ![](../../assets/dialogs/querybox-get-date.png)

        Parameters:

            parent (Widget):
                The parent widget; the popup will appear to the
                bottom-right of the parent widget. If no parent is
                provided, the widget is centered on the screen.

            title (str):
                The text that appears on the popup titlebar.

            firstweekday (int):
                Specifies the first day of the week. `0` is Monday, `6` is
                Sunday (the default).

            startdate (datetime):
                The date to be in focus when the widget is displayed;

            bootstyle (str):
                The following colors can be used to change the color of the
                title and hover / pressed color -> primary, secondary, info,
                warning, success, danger, light, dark.

        Returns:

            datetime:
                The date selected; the current date if no date is selected.
        """
        # change to CustomDatePicker
        chooser = CustomDatePickerDialog(
            parent=parent,
            title=title,
            firstweekday=firstweekday,
            startdate=startdate,
            bootstyle=bootstyle,
        )
        return chooser.date_selected


class CustomDatePickerDialog(DatePickerDialog):
    def _draw_calendar(self):
        self._update_widget_bootstyle()
        self._set_title()
        self._current_month_days()
        self.frm_dates = ttk.Frame(self.frm_calendar)
        self.frm_dates.pack(fill=BOTH, expand=YES)

        for row, weekday_list in enumerate(self.monthdays):
            for col, day in enumerate(weekday_list):
                self.frm_dates.columnconfigure(col, weight=1)
                if day == 0:
                    ttk.Label(
                        master=self.frm_dates,
                        text=self.monthdates[row][col].day,
                        anchor=CENTER,
                        padding=5,
                        bootstyle=INFO,
                    ).grid(row=row, column=col, sticky=NSEW)
                else:
                    if all(
                        [
                            day == self.date_selected.day,
                            self.date.month == self.date_selected.month,
                            self.date.year == self.date_selected.year,
                        ]
                    ):
                        day_style = "secondary-button"      # change from 'toolbutton' to 'button'
                    else:
                        day_style = f"{self.bootstyle}-calendar"

                    def selected(x=row, y=col):
                        self._on_date_selected(x, y)

                    btn = ttk.Radiobutton(
                        master=self.frm_dates,
                        variable=self.datevar,
                        value=day,
                        text=day,
                        bootstyle=day_style,
                        padding=5,
                        command=selected,
                    )
                    btn.grid(row=row, column=col, sticky=NSEW)
