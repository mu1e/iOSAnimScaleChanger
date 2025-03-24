import os

def create_plist_from_input(plist_content: str, file_name: str = "output.plist"):
    """
    Creates a .plist file with the content provided by the user.
    
    :param plist_content: The content of the .plist file as a string.
    :param file_name: The name of the output .plist file (default is 'output.plist').
    """
    with open(file_name, 'w') as plist_file:
        plist_file.write(plist_content)
    print(f"Plist file '{file_name}' created successfully.")

def read_plist_file(file_path: str):
    """
    Reads and prints the content of a .plist file.
    
    :param file_path: The path to the .plist file.
    """
    if not os.path.exists(file_path):
        print(f"File '{file_path}' does not exist.")
        return

    with open(file_path, 'r') as plist_file:
        content = plist_file.read()
    print("Content of the plist file:")
    print(content)

def main_menu():
    """
    Displays the main menu for the program.
    """
    while True:
        print("\nPlist Manager")
        print("1. Create a new plist file")
        print("2. Read an existing plist file")
        print("3. Exit")
        choice = input("Please choose an option (1-3): ")
        
        if choice == '1':
            plist_content = input("Enter the content for the plist file:\n")
            file_name = input("Enter the file name (with .plist extension): ")
            create_plist_from_input(plist_content, file_name)
        
        elif choice == '2':
            file_path = input("Drag and drop the plist file here: ").strip().strip('"')
            read_plist_file(file_path)
        
        elif choice == '3':
            print("Exiting the program.")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
