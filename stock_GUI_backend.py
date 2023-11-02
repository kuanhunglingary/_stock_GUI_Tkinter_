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