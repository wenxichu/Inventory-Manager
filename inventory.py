import pandas as pd
from prettytable import PrettyTable

# Directory
file_data = pd.read_csv("Lab Data.csv")

glass_df = pd.DataFrame(file_data.iloc[0:15, 0:5], columns=["Glassware", "No. in Stock", "Location",
                                                            "Vendor", "Unit Price"])
cell_df = pd.DataFrame(file_data.iloc[0:15, 5:10], columns=["Cell Culture", "No. in Stock.1", "Location.1",
                                                            "Vendor.1", "Unit Price.1"])
chem_df = pd.DataFrame(file_data.iloc[0:16, 10:15], columns=["Chemicals", "No. in Stock.2", "Location.2",
                                                             "Vendor.2", "Unit Price.2"])
supply_df = pd.DataFrame(file_data.iloc[0:14, 15:20], columns=["Lab Supplies", "No. in Stock.3", "Location.3",
                                                               "Vendor.3", "Unit Price.3"])
instr_df = pd.DataFrame(file_data.iloc[0:13, 20:25], columns=["Instrument", "No. in Stock.4", "Location.4",
                                                              "Vendor.4", "Unit Price.4"])


class Database:
    def __init__(self, new_df):
        self.new_df = new_df.to_numpy().tolist()

    def entries(self):
        return self.new_df

    def __len__(self):
        return len(self.new_df)


def del_sign(col_val):
    char = "$,"
    for s in char:
        col_val = str(col_val).replace(s, "")
    return float(col_val)


def sort_values(df_arr, col_num):

    if len(df_arr) > 1:

        midpt = len(df_arr) // 2
        l_arr = df_arr[:midpt]
        r_arr = df_arr[midpt:]

        sort_values(l_arr, col_num)
        sort_values(r_arr, col_num)

        i = j = k = 0

        while i < len(l_arr) and j < len(r_arr):
            l_val = l_arr[i][col_num]
            r_val = r_arr[j][col_num]

            if del_sign(l_val) <= del_sign(r_val):
                df_arr[k] = l_arr[i]
                i += 1
            else:
                df_arr[k] = r_arr[j]
                j += 1
            k += 1

        while i < len(l_arr):
            df_arr[k] = l_arr[i]
            i += 1
            k += 1

        while j < len(r_arr):
            df_arr[k] = r_arr[j]
            j += 1
            k += 1

    return df_arr


def update_values(table, column):
    stock = "No. in Stock"
    price = "Unit Price"
    value = 0

    if stock in str(column):
        value = 1
    elif price in str(column):
        value = 4

    list_df = Database(table).entries()
    sorted_df = sort_values(list_df, value)
    new_df = pd.DataFrame(sorted_df, columns=table.columns)
    table.update(new_df, overwrite=True)


def df_to_table(name, df):
    pt = PrettyTable()
    pt.field_names = [name, "No. in Stock", "Location", "Vendor", "Unit Price"]
    for e in df.index:
        pt.add_row(df.iloc[e])
    return pt


glassware = df_to_table("Glassware", glass_df)
cell_culture = df_to_table("Cell Culture", cell_df)
chemicals = df_to_table("Chemicals", chem_df)
lab_supplies = df_to_table("Lab Supplies", supply_df)
instrument = df_to_table("Instrument", instr_df)
