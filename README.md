# _stock_GUI_Tkinter_

stock_GUI_app.py
'''
#-------------------------------
#1, Imports the tkinter module.
#-------------------------------
import tkinter
from tkinter import ttk
import stock_GUI_backend as backend

#-------------------------------
#2, Creates a main GUI window.
#-------------------------------
#2.1 Defines the main window
root = tkinter.Tk()
root.title("台積電股價")
root.resizable(0,0)

#2.2 Defines colors
bg_color = '#313131'
forecolor = '#E5E5E5'
button_color = '#AFAFAF'
root.config(bg = bg_color)

#-------------------------------
#3, Adds widgets to the window.
#-------------------------------
#3.1 Creates frames.
greeting_frame = tkinter.Frame(root, bg=bg_color)
textbox_frame = tkinter.Frame(root, bg=bg_color)
radio_frame = tkinter.LabelFrame(root, text='Selct a dataset', bg=bg_color, fg=forecolor)
combobox_frame = tkinter.Frame(root, bg=bg_color)
button_frame = tkinter.Frame(root, bg=bg_color)
treeview_frame = tkinter.Frame(root, bg=bg_color)

#3.2 Arranges the frames.
greeting_frame.pack()
textbox_frame.pack()
radio_frame.pack()
combobox_frame.pack()
button_frame.pack()
treeview_frame.pack()

#3.3 Uses the greeting frame to organize widgets.
#3.3.1 Adds a label to the greeting frame.
greeting_label = tkinter.Label(greeting_frame, text='Welcome', bg=bg_color, fg=forecolor)

#3.3.2 Arranges the label.
greeting_label.pack(pady=(10,5))

#3.4 Arrange the textbox frame.
#3.4.1 Adds a label to the textbox frame.
entry_label = tkinter.Label(textbox_frame, text='Stock Ticker Symbol:', bg=bg_color, fg=forecolor)

#3.4.2 Adds a text box to the textbox frame and set the initial value.
text_entry = tkinter.Entry(textbox_frame)
initial_value = '2330.TW'
text_entry.insert(0, initial_value)

#3.4.3 Defines the frame layout.
entry_label.grid(row=0, column=0, padx=(10,0), pady=5)
text_entry.grid(row=0, column=1, padx=5, pady=5)

#3.4.4 Bind to the event
text_entry.bind("<ButtonPress-1>", lambda event, initial_message = initial_value: backend.entry_click(event, initial_value))

#3.5 Arranges the radio frame.
#3.5.1 Set initial value.
number = tkinter.IntVar()
number.set(1)

#3.6 Arranges the combobox frame.
#3.6.1 Add labels, comboboxes and the get button to the frame.
period_label = tkinter.Label(combobox_frame, text='Period:', width = 6, anchor='e', bg=bg_color, fg=forecolor)
period_combobox = ttk.Combobox(combobox_frame, value=['1d','5d','1mo'], width=8, justify='center', state="readonly")
interval_label = tkinter.Label(combobox_frame, text='Interval:', width = 6, anchor='e', bg=bg_color, fg=forecolor)
interval_combobox = ttk.Combobox(combobox_frame, value=['15m','30m','1h'], width=8,justify='center', state="readonly")

#3.6.2 Set default selection.
period_combobox.current(0)
interval_combobox.current(0)

#3.6.3 Define the frame layout
period_label.grid(row=0, column=0, padx=(5,0), pady=5)
period_combobox.grid(row=0, column=1, padx=(0,5), pady=5)
interval_label.grid(row=0, column=2, padx=(5,0), pady=5)
interval_combobox.grid(row=0, column=3, padx=(0,5), pady=5)

#3.7 Arrange the button frame.
#3.7.1 Adds a button to the button frame.
get_button = tkinter.Button(button_frame, 
                            text = "Get Data",
                            command = lambda:backend.get_data(tree, text_entry, number, period_combobox, interval_combobox),
                            width = 34, borderwidth = 3, bg = button_color)

#3.7.2 Defines the frame layout.
get_button.pack()

#3.8 Arrange the treeview frame.
#3.8.1 Adds a treeview to the treeview frame.
columns = ['col0','col1','col2','col3']
col_width = [190, 90, 110, 190]
default_headings = ['Datetime', 'Open', 'Close', 'Volume']
tree = ttk.Treeview(treeview_frame, columns = columns, show = 'headings', height = 12)
# assigns the column width and headings
for index, col in enumerate(columns):
    tree.column(col, width = col_width[index], anchor = 'center')
    tree.heading(col, text=default_headings[index])

#3.8.2 Add a scrollbar to the treeview frame.
scrollbar = ttk.Scrollbar(treeview_frame, orient = tkinter.VERTICAL, command = tree.yview)
tree.configure(yscroll = scrollbar.set)

#3.8.3 Defines the frame layout.
tree.grid(row = 0, column = 0, sticky = 'nsew', padx = (5,0), pady = 5)
scrollbar.grid(row = 0, column = 1, sticky = 'ns', padx = (0,5), pady = 5)

#-------------------------------
#4, Runs the window's main loop.
#-------------------------------
root.mainloop()
'''
stock_GUI_app.py
'''
import tkinter
import yfinance as yf
import pandas as pd

def entry_click(event, initial_message):
    if event.widget.get() == initial_message:
        event.widget.delete(0, tkinter.END)

def clear_treeview(treeView):
    for row in treeView.get_children():
        treeView.delete(row)

def make_selection(treeView, number, period_combobox, interval_combobox):
    column_headings = ['Datetime', 'Open', 'Close', 'Volume']
    col_anchor = ['center', 'center', 'center', 'center']
    period_combobox.config(state = "readonly")
    interval_combobox.config(state = "readonly")
    clear_treeview(treeView)    
    for index, col in enumerate(column_headings):
        treeView.heading(index, text = col)
        treeView.column(index, anchor=col_anchor[index])

def invalid_entry(entry):
    entry.insert(0, "*")
    entry.insert(tkinter.END, "*")

def get_data(tree, symbol_entry, number, period_combobox, interval_combobox):
    clear_treeview(tree)
    dataset = None
    ticket = yf.Ticker(symbol_entry.get())
    if ticket.institutional_holders is None:
        return invalid_entry(symbol_entry)
    period = period_combobox.get()
    interval = interval_combobox.get()
    data = ticket.history(period = period, interval = interval)
    if data.empty == False:
        data.reset_index(inplace = True)
        dataset = data[['Datetime', 'Open', 'Close', 'Volume']].copy()
        dataset['Datetime'] = dataset['Datetime'].dt.strftime("%Y-%m-%d %H:%M")
        dataset[['Open', 'Close', 'Volume']] = dataset[['Open', 'Close', 'Volume']].applymap(lambda x: '{0:.4f}'.format(x))
    else:
        dataset = pd.DataFrame()
    for index in range(len(dataset)):
        #https://tkdocs.com/tutorial/tree.html
        tree.insert('', tkinter.END, values=list(dataset.loc[index]))
'''
