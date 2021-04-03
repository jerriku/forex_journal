from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random, pandas, os.path, matplotlib, numpy
import matplotlib.pyplot as plt

root = Tk()
root.geometry('+800+400')
root.resizable(0, 0)
root.title("Journal")

class Strategy:
    def __init__(self, pattern, profit, wins, losses, total):
        self.name = pattern
        self.earned = profit
        self.wins = wins
        self.losses = losses
        self.total = total

    def add_win(self):
        self.wins += 1
    
    def add_loss(self):
        self.losses +=1

    def add_total(self):
        self.total += 1

    def add_profit(self, profit):
        is_there_nan = False
        for i in range(len(self.earned)):
            if numpy.isnan(self.earned[i]):
                self.earned[i] = profit
                is_there_nan = True
                break
        
        if not is_there_nan:
            self.earned.append(profit)


#### CREATE DATA ####
def save_dataframe(patterns, wins, losses, totals):
    new_dataframe = pandas.DataFrame({"Patterns": patterns, "Wins": wins, "Losses": losses, "Total": totals})
    new_dataframe.to_excel("./journal.xlsx", sheet_name="Journal")


if not os.path.exists("./journal.xlsx"):
    save_dataframe([], [], [], [])


if not os.path.exists("./profit.xlsx"):
    pandas.DataFrame({}).to_excel("./profit.xlsx", sheet_name="Profit", index=False)
#### CREATE DATA ####

#### THE BRAIN ####
def show_values(event):
    patterns = [pattern.name for pattern in strategies  ]
    wins     = [pattern.wins for pattern in strategies  ]
    losses   = [pattern.losses for pattern in strategies]
    totals   = [pattern.total for pattern in strategies ]
    choice = pattern_options.get()
    if choice:
        pattern_label.config(text=f"Patterns: {patterns[patterns.index(choice)]}")
        wins_label.config(text=f"Wins: {wins[patterns.index(choice)]}")
        losses_label.config(text=f"Losses: {losses[patterns.index(choice)]}")
        totals_label.config(text=f"Total: {totals[patterns.index(choice)]}")


def add_pattern(name):
    patterns = [pattern.name for pattern in strategies]
    if name and not name in patterns:
        strategies.append(Strategy(name, [], 0, 0, 0))
        patterns = [pattern.name for pattern in strategies  ]
        wins     = [pattern.wins for pattern in strategies  ]
        losses   = [pattern.losses for pattern in strategies]
        totals   = [pattern.total for pattern in strategies ]
        save_dataframe(patterns, wins, losses, totals)

        profit_dataframe = pandas.read_excel("./profit.xlsx", sheet_name="Profit")
        profit_dataframe[name] = ""
        profit_dataframe.to_excel("./profit.xlsx", sheet_name="Profit", index=False)
        pattern_options.config(values = patterns)
    pattern_entry.delete(0, END)


def update_after_delete(patterns, wins, losses, totals):
    try:
        pattern_options.set(patterns[0])
        pattern_label.config(text=f"Patterns: {patterns[0]}")
        wins_label.config(text=f"Wins: {wins[0]}")
        losses_label.config(text=f"Losses: {losses[0]}")
        totals_label.config(text=f"Total: {totals[0]}")
    except IndexError:
        pattern_options.set("")
        pattern_label.config(text=f"Patterns")
        wins_label.config(text=f"Wins")
        losses_label.config(text=f"Losses")
        totals_label.config(text=f"Total")


def delete_pattern(choice):
    if choice:
        patterns = [pattern.name for pattern in strategies   if pattern.name != choice]
        wins     = [pattern.wins for pattern in strategies   if pattern.name != choice]
        losses   = [pattern.losses for pattern in strategies if pattern.name != choice]
        totals   = [pattern.total for pattern in strategies  if pattern.name != choice]
        save_dataframe(patterns, wins, losses, totals)

        profit_dataframe = pandas.read_excel("./profit.xlsx", sheet_name="Profit")
        profit_dataframe.drop(choice, inplace=True, axis=1)
        profit_dataframe.to_excel("./profit.xlsx", sheet_name="Profit", index=False)
        
        pattern_options.config(values = patterns)
        update_after_delete(patterns, wins, losses, totals)
    else:
        messagebox.showerror("Error", "Select a pattern to delete.")


def update_profitdata(choice, profit, window, condition):
    window.destroy()
    patterns = [pattern.name for pattern in strategies  ]
    wins     = [pattern.wins for pattern in strategies  ]
    losses   = [pattern.losses for pattern in strategies]
    totals   = [pattern.total for pattern in strategies ]
    pattern  = [strategies[index] for index in range(len(strategies)) if strategies[index].name == choice][0]
    if condition:
        pattern.add_win()
        wins[patterns.index(choice)] += 1
        wins_label.config(text=f"Wins: {wins[patterns.index(choice)]}")
    else:
        pattern.add_loss()
        losses[patterns.index(choice)] += 1
        losses_label.config(text=f"Losses: {losses[patterns.index(choice)]}")
    pattern.add_total()
    totals[patterns.index(choice)] += 1
    pattern.add_profit(profit)
    totals_label.config(text=f"Total: {totals[patterns.index(choice)]}")
    save_dataframe(patterns, wins, losses, totals)
    
    profit_dataframe = pandas.read_excel("./profit.xlsx", sheet_name="Profit")
    df2 = pandas.DataFrame([profit], columns=[pattern.name])
    profit_dataframe = profit_dataframe.append(df2, ignore_index=True)
    profit_dataframe[pattern.name] = pandas.Series(pattern.earned)
    print("After", profit_dataframe)
    profit_dataframe.to_excel("./profit.xlsx", sheet_name="Profit", index=False)


def check_entry(choice, profit, window, condition):
    if profit:
        try:
            profit = float(profit)
            update_profitdata(choice, profit, window, condition)
        except ValueError:
            messagebox.showerror("Error", "Enter a number indicating the profit gain/loss.")
    else:
        messagebox.showerror("Error", "Enter a number indicating the profit gain/loss.")


def add_win(choice, root):
    if choice:
        window = Toplevel(root)
        window.geometry('+800+400')
        window_label  = Label(window, width=30, text="How much profit?")
        window_entry  = Entry(window, width=30)
        window_button = Button(window, width=30, text="Add", command=lambda: check_entry(choice, window_entry.get(), window, True))

        window_label.pack()
        window_entry.pack()
        window_button.pack()
    else:
        messagebox.showerror("Error", "Select a pattern.")


def add_loss(choice, root):
    if choice:
        window = Toplevel(root)
        window.geometry('+800+400')
        window_label  = Label(window, width=30, text="How much loss?")
        window_entry  = Entry(window, width=30)
        window_button = Button(window, width=30, text="Add", command=lambda: check_entry(choice, "-" + window_entry.get(), window, False))
        
        window_label.pack()
        window_entry.pack()
        window_button.pack()

# Plotting bar chart
def autolabel(rects, ax):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), # 3 points vertical offset
                    textcoords="offset points",
                    ha="center", va="bottom")


def calc_mean(a, b):
    if not a or  not b:
        return 0
    return round(((b / a) * 100), 2)


def show_barchart():
    patterns = [pattern.name for pattern in strategies  ]
    wins     = [pattern.wins for pattern in strategies  ]
    losses   = [pattern.losses for pattern in strategies]
    totals   = [pattern.total for pattern in strategies ]
    if patterns:
        means = list(map(calc_mean, totals, wins))
        print(means)

        x = numpy.arange(len(patterns))
        width = 0.35

        fig, ax = plt.subplots()
        rects = ax.bar(x - width/2, means, width, label="Patterns")

        ax.set_ylabel("Win(%)")
        ax.set_title("Win % of each patterns")
        ax.set_xticks(x)
        ax.set_xticklabels(patterns)
        plt.xticks(rotation=90)
        ax.legend()

        autolabel(rects, ax)

        fig.tight_layout()
        plt.show()


def check_keypress(event):
    key = "{0}".format(event.keysym)
    if key == "Return":
        add_pattern(pattern_entry.get())
#### THE BRAIN ####

#### READ AND SAVE DATA ####
patterns_dataframe = pandas.read_excel("./journal.xlsx", sheet_name="Journal", usecols=[1, 2, 3, 4])
strategies = []


def get_profits(pattern_name):
    profit_dataframe = pandas.read_excel("./profit.xlsx", sheet_name="Profit")
    profit_patterns = profit_dataframe.columns
    profit_size = profit_dataframe.index.size

    for index in range(profit_patterns.size):
        this_name = profit_patterns[index]
        if pattern_name == this_name:
            return [float(profit_dataframe.at[index, this_name]) for index in range(profit_size)]

def update_patterndata(strategies):
    for i in range(patterns_dataframe.size):
        try:
            profits = get_profits(patterns_dataframe.at[i, "Patterns"])
            strat = Strategy( patterns_dataframe.at[i, "Patterns"],
                                                        profits,
                            patterns_dataframe.at[i,     "Wins"],
                            patterns_dataframe.at[i,   "Losses"],
                            patterns_dataframe.at[i,    "Total"])
            strategies.append(strat)
        except KeyError:
            break
    return strategies

strategies = update_patterndata(strategies)
#### READ AND SAVE DATA ####

#### GUI WINDOW ####
first_frame = Frame(root, width=500, height=500)
first_frame.pack()

def get_names():
    return [item.name for item in strategies]

variable = StringVar(root)
pattern_options = ttk.Combobox(first_frame, textvariable=variable, state="readonly", width=30, values=get_names())
pattern_options.bind("<<ComboboxSelected>>", show_values)
pattern_entry   = Entry(first_frame, width=33)
pattern_button  = Button(first_frame, width=30, text="Add Pattern", command=lambda: add_pattern(pattern_entry.get()))
win_button      = Button(first_frame, width=30, text="Add Win", command=lambda: add_win(pattern_options.get(), root))
loss_button     = Button(first_frame, width=30, text="Add Loss", command=lambda: add_loss(pattern_options.get(), root))
delete_button   = Button(first_frame, width=30, text="Delete Pattern", command=lambda: delete_pattern(pattern_options.get()))
graph_button    = Button(first_frame, width=30, text="Show Bar Chart", command=lambda: show_barchart())

label_frame     = Frame(first_frame)

pattern_label   = Label(label_frame, text="Pattern")
wins_label      = Label(label_frame, text="Wins")
losses_label    = Label(label_frame, text="Losses")
totals_label    = Label(label_frame, text="Total")
profits_label   = Label(label_frame, text="Profits")

pattern_options.pack()
label_frame.pack()
pattern_label.pack()
wins_label.pack()
losses_label.pack()
totals_label.pack()
profits_label.pack()
pattern_entry.pack()
pattern_button.pack()
delete_button.pack()
graph_button.pack()
win_button.pack()
loss_button.pack()
#### GUI WINDOW ####

root.bind('<KeyPress>', check_keypress)
root.mainloop()
