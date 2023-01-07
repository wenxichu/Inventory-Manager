import tkinter
from tkinter import messagebox
from database import write_csv, lab_data, sum_mult
from inventory import update_values, glass_df, cell_df, chem_df, supply_df, instr_df, df_to_table

# Lab Window
inv_win = tkinter.Tk(className="inventory manager")
win_w = 880
win_h = 566

sw = inv_win.winfo_screenwidth()
sh = inv_win.winfo_screenheight()
x_pos = (sw / 2) - (win_w / 2)
y_pos = (sh / 2) - (win_h / 2)

inv_win.geometry("%dx%d+%d+%d" % (win_w, win_h, x_pos, y_pos))
inv_win["bg"] = "light gray"
inv_win.resizable(False, False)

new_page = tkinter.StringVar()
new_frame = tkinter.Label(inv_win, textvariable=new_page, background="#B3EAF4", font=("Courier", 12))

all_pgs = {1: [glass_df, "No. in Stock", "Unit Price"],
           2: [cell_df, "No. in Stock.1", "Unit Price.1"],
           3: [chem_df, "No. in Stock.2", "Unit Price.2"],
           4: [supply_df, "No. in Stock.3", "Unit Price.3"],
           5: [instr_df, "No. in Stock.4", "Unit Price.4"]}

page_ct = 0


def get_num(n):
    global page_ct
    page_ct = n
    return page_ct


def sort_col(choice):
    page_df = all_pgs[page_ct][0]

    if choice == "No. in Stock":
        update_values(page_df, all_pgs[page_ct][1])
    elif choice == "Unit Price":
        update_values(page_df, all_pgs[page_ct][2])

    new_table = df_to_table(page_df.columns[0], page_df)
    set_frame(new_table)


# Dropdown Select
var = tkinter.StringVar(inv_win)
var.set("Select One")
dropdown = tkinter.OptionMenu(inv_win, var, "No. in Stock", "Unit Price", command=sort_col)
dropdown.config(width=11, bg="light gray", activebackground="silver", font=("Times New Roman", 14))
dropdown["menu"].config(font=("Times New Roman", 14), bg="silver")
dropdown.pack()
dropdown.place(x=100, y=20)

prev_btn = tkinter.Button(inv_win, text="\u2190 Prev", font=("Times New Roman", 15), bg="#A2E5F1",
                          activebackground="silver", command=lambda: None)

next_btn = tkinter.Button(inv_win, text="Next \u2192", font=("Times New Roman", 15), bg="#A2E5F1",
                          activebackground="silver", command=lambda: None)

prev_btn.place(x=270, y=500)
next_btn.place(x=500, y=500)


# Export Data
def confirm(file, df):
    prompt = messagebox.askyesno("Question", "Do you want to export the data?", parent=inv_win)
    if prompt:
        write_csv(file, df)


export_btn = tkinter.Button(inv_win, text="Export", font=("Times New Roman", 15), bg="#A2E5F1",
                            activebackground="silver", command=lambda: None)
export_btn.place(x=390, y=500)


def set_frame(df_table):
    new_page.set(df_table)
    new_frame.pack(side="top", fill="y", padx=20, pady=78)
    return new_frame


budget = tkinter.Message(inv_win, text="Total Value: ", font=("Calibri", 15, "bold"), width=180, bg="lightgray")
budget.pack()
budget.place(x=315, y=448)

calculate = tkinter.Label(inv_win, text="0.00", background="#B3EAF4", font=("Calibri", 15), bg="whitesmoke")
calculate.pack()
calculate.place(x=435, y=450)


# Lab Inventory
class Page1:
    def __init__(self):
        self._name = "Glassware"
        get_num(1)
        glass_db = df_to_table(glass_df.columns[0], glass_df)
        self.glass_f = set_frame(glass_db)
        prev_btn.configure(command=lambda: Page5())
        next_btn.configure(command=lambda: Page2())
        self.export_file()
        calculate.configure(text=sum_mult(glass_df['No. in Stock'], glass_df['Unit Price']))

    @property
    def df_name(self):
        return self._name

    def export_file(self):
        export_btn.configure(command=lambda: confirm(self._name, glass_df))


class Page2:
    def __init__(self):
        self._name = "Cell Culture"
        get_num(2)
        cell_db = df_to_table(cell_df.columns[0], cell_df)
        self.cell_f = set_frame(cell_db)
        prev_btn.configure(command=lambda: Page1())
        next_btn.configure(command=lambda: Page3())
        self.export_file()
        calculate.configure(text=sum_mult(cell_df['No. in Stock.1'], cell_df['Unit Price.1']))

    @property
    def df_name(self):
        return self._name

    def export_file(self):
        export_btn.configure(command=lambda: confirm(self._name, cell_df))


class Page3:
    def __init__(self):
        self._name = "Chemicals"
        get_num(3)
        chem_db = df_to_table(chem_df.columns[0], chem_df)
        self.chem_f = set_frame(chem_db)
        prev_btn.configure(command=lambda: Page2())
        next_btn.configure(command=lambda: Page4())
        self.export_file()
        calculate.configure(text=sum_mult(chem_df['No. in Stock.2'], chem_df['Unit Price.2']))

    @property
    def df_name(self):
        return self._name

    def export_file(self):
        export_btn.configure(command=lambda: confirm(self._name, chem_df))


class Page4:
    def __init__(self):
        self._name = "Lab Supplies"
        get_num(4)
        supply_db = df_to_table(supply_df.columns[0], supply_df)
        self.supply_f = set_frame(supply_db)
        prev_btn.configure(command=lambda: Page3())
        next_btn.configure(command=lambda: Page5())
        self.export_file()
        calculate.configure(text=sum_mult(supply_df['No. in Stock.3'], supply_df['Unit Price.3']))

    @property
    def df_name(self):
        return self._name

    def export_file(self):
        export_btn.configure(command=lambda: confirm(self._name, supply_df))


class Page5:
    def __init__(self):
        self._name = "Instrument"
        get_num(5)
        instr_db = df_to_table(instr_df.columns[0], instr_df)
        self.instr_f = set_frame(instr_db)
        prev_btn.configure(command=lambda: Page4())
        next_btn.configure(command=lambda: Page1())
        self.export_file()
        calculate.configure(text=sum_mult(instr_df['No. in Stock.4'], instr_df['Unit Price.4']))

    @property
    def df_name(self):
        return self._name

    def export_file(self):
        export_btn.configure(command=lambda: confirm(self._name, instr_df))


Page1()

s_label = tkinter.Label(inv_win, text="Search", font=("Calibri", 16, "bold"), padx=4, bg="lightgray")
s_label.pack(side="left")
s_label.place(x=285, y=24)
s_var = tkinter.StringVar()

search = tkinter.Entry(inv_win, textvariable=s_var, width=35, font=("Calibri", 16), bg="#E7EEF0")


# Search Inventory
def default_text():
    search.insert("0", "Press enter to search...")
    search.config(font=("Calibri", 16, "italic"))
    search.bind("<FocusIn>", lambda event: search.delete("0", "end"))


def get_input():
    query = lab_data.search_df(search.get())
    set_frame(query)


default_text()
search.pack()
search.place(x=365, y=24)
search.bind("<1>", lambda event: search.focus_set())
search.bind("<Return>", lambda event: [get_input(), inv_win.focus_set()])
inv_win.mainloop()
