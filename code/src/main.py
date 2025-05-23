from SparseMatrix import SparseMatrix

def main():
    print("Sparse Matrix Operations")
    print("Select operation:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")

    choice = input("Enter choice (1/2/3): ").strip()

    if choice not in ['1', '2', '3']:
        print("Invalid choice. Please enter 1, 2, or 3.")
        return

    # Get file paths for input matrices
    file1 = input("Enter path for first matrix file: ").strip()
    file2 = input("Enter path for second matrix file: ").strip()

    try:
        # Load matrices
        matrix1 = SparseMatrix(file_path=file1)
        matrix2 = SparseMatrix(file_path=file2)

        # Perform selected operation
        if choice == '1':
            result = matrix1.add(matrix2)
            print("Addition completed successfully.")
        elif choice == '2':
            result = matrix1.subtract(matrix2)
            print("Subtraction completed successfully.")
        else:
            result = matrix1.multiply(matrix2)
            print("Multiplication completed successfully.")

        # Save result
        output_file = input("Enter path for output file: ").strip()                                                    result.save_to_file(output_file) 
        print(f"Result saved to {output_file}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()                           thats for main.py
