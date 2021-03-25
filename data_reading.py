from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random, pandas, os.path, matplotlib, numpy
import matplotlib.pyplot as plt

root = Tk()
root.geometry('+800+400')
root.resizable(0, 0)
root.title("Journal")


def save_dataframe(patterns, wins, losses, totals):
    new_dataframe = pandas.DataFrame({"Patterns": patterns, "Wins": wins, "Losses": losses, "Total": totals})
    new_dataframe.to_excel("./journal.xlsx", sheet_name="Journal")


if not os.path.exists("./journal.xlsx"):
    save_dataframe([], [], [], [])


def show_values(event):
    global patterns, wins, losses, totals
    choice = pattern_options.get()
    if choice:
        pattern_label.config(text=f"Patterns: {patterns[patterns.index(choice)]}")
        wins_label.config(text=f"Wins: {wins[patterns.index(choice)]}")
        losses_label.config(text=f"Losses: {losses[patterns.index(choice)]}")
        totals_label.config(text=f"Total: {totals[patterns.index(choice)]}")


def add_pattern(name):
    global patterns, wins, losses, totals
    if name and not name in patterns:
        patterns.append(name)
        wins.append(0)
        losses.append(0)
        totals.append(0)
        save_dataframe(patterns, wins, losses, totals)
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
    global patterns, wins, losses, totals
    if choice:
        wins.pop(patterns.index(choice))
        losses.pop(patterns.index(choice))
        totals.pop(patterns.index(choice))
        patterns.pop(patterns.index(choice))
        
        save_dataframe(patterns, wins, losses, totals)
        pattern_options.config(values = patterns)
        update_after_delete(patterns, wins, losses, totals)
    else:
        messagebox.showerror("Error", "Select a pattern to delete.")


def add_win(choice):
    global patterns, wins, losses, totals
    if choice:
        wins[patterns.index(choice)] += 1
        totals[patterns.index(choice)] += 1
        wins_label.config(text=f"Wins: {wins[patterns.index(choice)]}")
        totals_label.config(text=f"Total: {totals[patterns.index(choice)]}")
    else:
        messagebox.showerror("Error", "Select a pattern.")
    save_dataframe(patterns, wins, losses, totals)


def add_loss(choice):
    global patterns, wins, losses, totals
    if choice:
        losses[patterns.index(choice)] += 1
        totals[patterns.index(choice)] += 1
        losses_label.config(text=f"Losses: {losses[patterns.index(choice)]}")
        totals_label.config(text=f"Total: {totals[patterns.index(choice)]}")
    else:
        messagebox.showerror("Error", "Select a pattern.")
    save_dataframe(patterns, wins, losses, totals)

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
    global patterns, wins, losses, totals
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

#######################################################GUI WINDOW#######################################################
patterns_dataframe = pandas.read_excel("./journal.xlsx", sheet_name="Journal", usecols=[1, 2, 3, 4])
patterns = []
wins     = []
losses   = []
totals   = []

for i in range(patterns_dataframe.size):
    try:
        patterns.append(patterns_dataframe.at[i, "Patterns"])
        wins.append(patterns_dataframe.at[i, "Wins"])
        losses.append(patterns_dataframe.at[i, "Losses"])
        totals.append(patterns_dataframe.at[i, "Total"])
    except KeyError:
        break

first_frame = Frame(root, width=500, height=500)
first_frame.pack()

variable = StringVar(root)
# pattern_options = OptionMenu(first_frame, variable, *patterns)
pattern_options = ttk.Combobox(first_frame, textvariable=variable, state="readonly", width=30, values=patterns)
pattern_options.bind("<<ComboboxSelected>>", show_values)
pattern_entry   = Entry(first_frame, width=33)
pattern_button  = Button(first_frame, width=30, text="Add Pattern", command=lambda: add_pattern(pattern_entry.get()))
win_button      = Button(first_frame, width=30, text="Add Win", command=lambda: add_win(pattern_options.get()))
loss_button     = Button(first_frame, width=30, text="Add Loss", command=lambda: add_loss(pattern_options.get()))
delete_button   = Button(first_frame, width=30, text="Delete Pattern", command=lambda: delete_pattern(pattern_options.get()))
graph_button    = Button(first_frame, width=30, text="Show Bar Chart", command=lambda: show_barchart())

label_frame     = Frame(first_frame)

pattern_label   = Label(label_frame, text="Pattern")
wins_label      = Label(label_frame, text="Wins")
losses_label    = Label(label_frame, text="Losses")
totals_label    = Label(label_frame, text="Total")

pattern_options.pack()
label_frame.pack()
pattern_label.pack()
wins_label.pack()
losses_label.pack()
totals_label.pack()
pattern_entry.pack()
pattern_button.pack()
delete_button.pack()
graph_button.pack()
win_button.pack()
loss_button.pack()
#######################################################GUI WINDOW#######################################################
root.bind('<KeyPress>', check_keypress)
root.mainloop()
