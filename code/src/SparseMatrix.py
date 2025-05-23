class SparseMatrix:
    def __init__(self, file_path=None, num_rows=0, num_cols=0):
        self.rows = 0
        self.cols = 0
        self.matrix_data = {}  # Dictionary of dictionaries: {row: {col: value}}

        if file_path:
            self._load_from_file(file_path)
        else:
            if num_rows <= 0 or num_cols <= 0:
                raise ValueError("Matrix dimensions must be positive.")
            self.rows = num_rows
            self.cols = num_cols

    def _load_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                lines = [line.strip() for line in file if line.strip()]
                
                # Validate format and parse rows and cols
                if not lines[0].startswith('rows=') or not lines[1].startswith('cols='):
                    raise ValueError("Input file has wrong format")

                try:
                    self.rows = int(lines[0][5:].strip())
                    self.cols = int(lines[1][5:].strip())
                except ValueError:
                    raise ValueError("Input file has wrong format")

                self.matrix_data = {}
                for line in lines[2:]:
                    if len(line) < 7 or line[0] != '(' or line[-1] != ')':
                        raise ValueError("Input file has wrong format")
                    
                    content = line[1:-1].replace(' ', '')
                    parts = content.split(',')
                    if len(parts) != 3:
                        raise ValueError("Input file has wrong format")
                    
                    try:
                        row = int(parts[0])
                        col = int(parts[1])
                        val = int(parts[2])

                        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
                            raise ValueError("Matrix indices out of bounds.")

                        if val != 0:
                            if row not in self.matrix_data:
                                self.matrix_data[row] = {}
                            self.matrix_data[row][col] = val
                    except ValueError:
                        raise ValueError("Input file has wrong format")
        except FileNotFoundError:
            raise FileNotFoundError(f"File {file_path} not found.")

    def get_element(self, row, col):
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            raise ValueError("Matrix indices out of bounds.")
        
        return self.matrix_data.get(row, {}).get(col, 0)

    def set_element(self, row, col, value):
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            raise ValueError("Matrix indices out of bounds.")
        
        if value == 0:
            if row in self.matrix_data:
                if col in self.matrix_data[row]:
                    del self.matrix_data[row][col]
                    if not self.matrix_data[row]:  # Remove empty row dict
                        del self.matrix_data[row]
        else:
            if row not in self.matrix_data:
                self.matrix_data[row] = {}
            self.matrix_data[row][col] = value

    def add(self, other_matrix):
        if self.rows != other_matrix.rows or self.cols != other_matrix.cols:
            raise ValueError("Matrices must have the same dimensions for addition.")
        
        result = SparseMatrix(num_rows=self.rows, num_cols=self.cols)

        all_rows = set(self.matrix_data.keys()).union(other_matrix.matrix_data.keys())

        for row in all_rows:
            common_cols = set(self.matrix_data.get(row, {}).keys()).union(
                          other_matrix.matrix_data.get(row, {}).keys())
            for col in common_cols:
                sum_val = self.get_element(row, col) + other_matrix.get_element(row, col)
                result.set_element(row, col, sum_val)
        
        return result

    def subtract(self, other_matrix):
        if self.rows != other_matrix.rows or self.cols != other_matrix.cols:
            raise ValueError("Matrices must have the same dimensions for subtraction.")
        
        result = SparseMatrix(num_rows=self.rows, num_cols=self.cols)

        all_rows = set(self.matrix_data.keys()).union(other_matrix.matrix_data.keys())

        for row in all_rows:
            common_cols = set(self.matrix_data.get(row, {}).keys()).union(
                          other_matrix.matrix_data.get(row, {}).keys())
            for col in common_cols:
                diff_val = self.get_element(row, col) - other_matrix.get_element(row, col)
                result.set_element(row, col, diff_val)
        
        return result

    def multiply(self, other_matrix):
        if self.cols != other_matrix.rows:
            raise ValueError("Incompatible dimensions for matrix multiplication.")
        
        result = SparseMatrix(num_rows=self.rows, num_cols=other_matrix.cols)

        for row in self.matrix_data:
            for col1, val1 in self.matrix_data[row].items():
                if col1 in other_matrix.matrix_data:
                    for col2, val2 in other_matrix.matrix_data[col1].items():
                        current = result.get_element(row, col2)
                        result.set_element(row, col2, current + val1 * val2)
        
        return result

    def save_to_file(self, file_path):
        with open(file_path, 'w') as file:
            file.write(f"rows={self.rows}\n")
            file.write(f"cols={self.cols}\n")
            
            for row in sorted(self.matrix_data.keys()):
                row_dict = self.matrix_data[row]
                for col in sorted(row_dict.keys()):
                    file.write(f"({row}, {col}, {row_dict[col]})\n")
