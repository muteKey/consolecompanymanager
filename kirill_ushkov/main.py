

# if __name__ == "__main__":
#     print("test")

while True:
    print("List of available commands:")
    print("add_department <department_name> - creates department with <department_name>")
    print("select_department <department_name> - selects department with <department_name>")
    print("quit - actually quits program :)")

    user_input = input("Please enter command:\n")
    command = user_input.strip().lower()

    if command == "quit":
        print("Goodbye!")
        break
    elif command == "add_department":
        print("Add department command selected")
        break
    elif command == "select_department":
        print("Select department command selected")
        break
    else:
        print("Unrecognized command!")
        continue


