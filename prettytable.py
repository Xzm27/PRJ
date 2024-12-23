class PrettyTable:
    def __init__(self, headers: list, data: list[list])-> None:
        """
        Initializes the PrettyTable with headers and data.

        Args:
            headers (list): List of headers for the table
            data (list[list]): 2d array of the data to be presented
        """
        self.headers = headers
        self.data = data
        self.column_widths = [max(len(str(item)) for item in col) for col in zip(*data, headers)]
        
    def get_table(self)-> str:
        """
        Prints the table to the console with nice formatting
        
        Returns:
            string: returns the table in string format
        """
        table_str = ""
        header_row = " | ".join(f"{header:^{self.column_widths[i]}}" for i, header in enumerate(self.headers))        
        table_str =header_row + "\n"
        table_str += "-" * len(header_row) + "\n" 
        
        # Data rows
        for row in self.data:
            table_str += " | ".join(f"{str(row[i]):^{self.column_widths[i]}}" for i in range(len(row))) + "\n"
        
        return table_str
        
        