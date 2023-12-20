"""
Input field class for tkinter
"""

from tkinter import Entry, Label, Frame, LEFT, RIGHT, BOTH
from tkinter.constants import BOTTOM, TOP
from tkinter.ttk import Button


class TkInputFieldValidator(Frame):
    """
    define a button to validate the input fields of he current frame
    """

    def __init__(self, frame, callback, *args, **kwargs):
        """
        :param frame: the frame to validate the input fields of
        :param callback: the callback to call when the button is pressed
        """
        Frame.__init__(self, *args, **kwargs)
        self.__frame = frame
        self.__callback = callback
        self.__button = Button(self, text="Validate", command=self.__callback)
        self.__button.pack(side=RIGHT)
        self.pack(expand=True, fill=BOTH)


class TkInputField(Frame):
    """
    Define a text input field with a label and
    """

    def __init__(self, master_frame, field_name: str, field_type: type, input_size: int = 10,
                 secured_input: bool = False, *args, **kwargs):
        """
        :param master_frame: the frame to attach the input field to
        :param field_name: the name of the field to display (label)
        :param field_type: the type of the field to accept/transform to
        """
        Frame.__init__(self, master_frame, *args, **kwargs)
        self.__field_name = field_name
        self.__field_type = field_type
        self.__input_size = input_size
        self.__label = Label(self, text=field_name)
        self.__label.pack(side=TOP)
        if secured_input:
            self.__entry = Entry(self, show="*")
        else:
            self.__entry = Entry(self)
        self.__entry.pack(side=BOTTOM)
        self.pack(expand=False)

    @property
    def value(self):
        """
        :return: the typed value of the field
        """
        entry = self.__entry.get()
        if self.__field_type == str and len(entry) > self.__input_size:
            return None
        return self.__field_type(self.__entry.get())
