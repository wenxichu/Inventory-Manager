from inventory import glass_df, cell_df, chem_df, supply_df, instr_df
from tabulate import tabulate


class Page:
    def __init__(self, data=None):
        self.data = data
        self.prev = None
        self.next = None


class DoubleLL:
    def __init__(self, data):
        new_node = Page(data)
        self.head = new_node
        self.tail = new_node
        self.length = 1

    def add_df(self, data):
        new_node = Page(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.length += 1
        return True

    def pop_df(self):
        if self.length == 0:
            return None
        temp = self.tail
        if self.length == 1:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
            temp.prev = None
        self.length -= 1
        return temp

    def get_page(self, index):
        if index < 0 or index >= self.length:
            return None
        temp = self.head
        if index < self.length / 2:
            for _ in range(index):
                temp = temp.next
        else:
            temp = self.tail
            for _ in range(self.length - 1, index, -1):
                temp = temp.prev
        return temp

    def prev_page(self, index):
        try:
            temp = self.get_page(index)
            if not index == 0:
                temp = temp.prev
            return temp.data
        except AttributeError:
            return "The page does not exist."

    def next_page(self, index):
        try:
            temp = self.get_page(index)
            if index < self.length - 1:
                temp = temp.next
            return temp.data
        except AttributeError:
            return "The page does not exist."

    def search_df(self, item):
        temp = self.head
        upper = item.title()
        while temp is not None:
            df = temp.data
            name = df.columns.values[0]
            if df[name].str.contains(upper).any():
                result = df.loc[df[name].str.contains(upper)]
                keys = [name, "No. in Stock", "Location", "Vendor", "Unit Price"]
                new_tb = tabulate(result, headers=keys, tablefmt="pretty", showindex=False)
                return new_tb
            temp = temp.next
        else:
            return "This item is not in stock. Try something else."


def write_csv(name, new_df):
    titles = [name, "No. in Stock", "Location", "Vendor", "Unit Price"]
    new_df.to_csv(str(name + ".csv"), header=titles, index=False)


def sum_mult(stock_col, price_col):
    new_col = price_col.map(lambda x: x.strip("$").replace(",", ""))
    col_1 = stock_col.astype(int)
    col_2 = new_col.astype(float)

    mult_cells = col_1 * col_2
    return "${:,.2f}".format(mult_cells.sum())


lab_data = DoubleLL(glass_df)
lab_data.add_df(cell_df)
lab_data.add_df(chem_df)
lab_data.add_df(supply_df)
lab_data.add_df(instr_df)
# print(lab_data.prev_page(4))
# print(lab_data.next_page(3))
