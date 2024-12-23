class PrettyTable:
    def __init__(self, headers, data):
        """
        Initializes the PrettyTable with headers and data.

        :param headers: List of column headers.
        :param data: List of rows, where each row is a list of column values.
        """
        self.headers = headers
        self.data = data
        self.column_widths = [max(len(str(item)) for item in col) for col in zip(*data, headers)]
        
    def get_table(self):
        """
        Prints the table to the console with nice formatting
        """
        table_str = ""
        header_row = " | ".join(f"{header:^{self.column_widths[i]}}" for i, header in enumerate(self.headers))        
        table_str =header_row + "\n"
        table_str += "-" * len(header_row) + "\n" 
        
        # Data rows
        for row in self.data:
            table_str += " | ".join(f"{str(row[i]):^{self.column_widths[i]}}" for i in range(len(row))) + "\n"
        
        return table_str
        
        