import logging
import tkinter as tk


class TextHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        log_msg = self.format(record) + "\n"
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, log_msg)
        self.text_widget.see(tk.END)
        self.text_widget.config(state=tk.DISABLED)

