# Importing 
import os
from datetime import datetime, date

# Defining global variable
DATETIME_STRING_FORMAT = "%d-%m-%Y"

# Creating new class for Task
class Task:
    def __init__(self, username = None, title = None, description = None, due_date = None, assigned_date = None, completed = None):
        '''
        Inputs:
        username: String
        title: String
        description: String
        due_date: DateTime
        assigned_date: DateTime
        completed: Boolean
        '''
        self.username = username
        self.title = title
        self.description = description
        self.due_date = due_date
        self.assigned_date = assigned_date
        self.completed = completed

    def from_string(self, task_str):
        '''
        Convert from string in tasks.txt to object
        '''
        task = task_str.split(";")
        username = task[0]
        title = task[1]
        description = task[2]
        due_date = datetime.strptime(task[3], DATETIME_STRING_FORMAT).date()
        assigned_date = datetime.strptime(task[4], DATETIME_STRING_FORMAT).date()
        completed = True if task[5] == "Yes" else False
        self.__init__(username, title, description, due_date, assigned_date, completed)


    def to_string(self):
        '''
        Convert to string for storage in tasks.txt
        '''
        str_attrs = [
            self.username,
            self.title,
            self.description,
            self.due_date.strftime(DATETIME_STRING_FORMAT),
            self.assigned_date.strftime(DATETIME_STRING_FORMAT),
            "Yes" if self.completed else "No"
        ]
        return ";".join(str_attrs)

    def display(self):
        '''
        Display object in readable format
        '''
        disp_str = f"Task: \t\t\t\t {self.title}\n"
        disp_str += f"Assigned to: \t\t\t {self.username}\n"
        disp_str += f"Date Assigned: \t\t\t {self.assigned_date.strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t\t\t {self.due_date.strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \t\t {self.description}\n"
        return disp_str
        


# Read and parse tasks.txt
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]  # List of all tasks in strings


    task_list = []  # List of objects from Task class
    for t_str in task_data:
        curr_t = Task()
        curr_t.from_string(t_str)
        task_list.append(curr_t)

# Read and parse user.txt
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

    # Convert to a dictionary
    username_password = {}
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password


# Keep trying until a successful login
def logging_in():
    logged_in = False
    
    while not logged_in:

        print("LOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        if curr_user not in username_password.keys():
            print("User does not exist")
            continue
        elif username_password[curr_user] != curr_pass:
            print("Wrong password")
            continue
        else:
            print("Login Successful!")
            logged_in = True
        
        return curr_user

curr_user = logging_in()


def validate_string(input_str):
    '''
    Function for ensuring that string is safe to store
    '''
    if ";" in input_str:
        print("Your input cannot contain a ';' character")
        return False
    return True

def check_username_and_password(username, password):
    '''
    Ensures that usernames and passwords can't break the system
    '''
    # ';' character cannot be in the username or password
    if ";" in username or ";" in password:
        print("Username or password cannot contain ';'.")
        return False
    return True

def write_usernames_to_file(username_dict):   
    '''
    Function to write username to file
    Input: dictionary of username-password key-value pairs
    '''
    with open("user.txt", "w") as out_file:
        user_data = []
        for k in username_dict:
            user_data.append(f"{k};{username_dict[k]}")
        out_file.write("\n".join(user_data))
        
def reg_user():
    
    # Registers new user

    # Request input of a new username
    if curr_user != 'admin':
        print("Registering new users requires admin privileges")
        main_menu()

    else:
        while True:
            # Request input of a new username
            new_username = input("New Username: ")
            
            # Check if username is longer than 3 char
            if len(new_username) >= 3:
                # Check if the username exists in a dictionary
                if new_username in username_password:
                    print("This user name is already used. Try again with a different username.")
                
                else:
                    # Request input of a new password
                    new_password = input("New Password: ")
                    if len(new_password) >= 3:
                        if not check_username_and_password(new_username, new_password):
                            # Username or password is not safe for storage - continue
                            continue
                        else:
                            # Request input of password confirmation.
                            confirm_password = input("Confirm Password: ")

                            # Check if the new password and confirmed password are the same.
                            if new_password == confirm_password:
                                # If they are the same, add them to the user.txt file,
                                
                                # Add to dictionary and write to file
                                username_password[new_username] = new_password
                                write_usernames_to_file(username_password)
                                

                                print("New user added")
                                break
                            # Otherwise you present a relevant message.
                            else:
                                print("Passwords do no match")
                    else:
                        print("Password needs to be at least 3 letters long.")

            else:
                print('Username must have at least 3 letters.')
            
# Obtain and parse current date
curr_date = date.today()

def add_task():
    # Add a new task
        # Prompt a user for the following: 
        #     A username of the person whom the task is assigned to,
        #     A title of a task,
        #     A description of the task and 
        #     the due date of the task.
    while True:
        # Ask for username
        task_username = input("User name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue

        # Get title of task and ensure safe for storage
        while True:
            task_title = input("Title of Task: ")
            if validate_string(task_title):
                break

        # Get description of task and ensure safe for storage
        while True:
            task_description = input("Description of Task: ")
            if validate_string(task_description):
                break

        # Obtain and parse due date
        while True:
            try:

                task_due_date = input("Due date of task (DD-MM-YYYY): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT).date()
                break
            except ValueError:
                print("Invalid datetime format. Please use the format specified")

        
        # Create a new Task object and append to list of tasks
        t = Task(task_username, task_title, task_description, due_date_time, curr_date, False)
        task_list.append(t)

        # Write to tasks.txt
        with open("tasks.txt", "w") as task_file:
            task_file.write("\n".join([t.to_string() for t in task_list]))
        print("Task successfully added.")
        break


def view_all():
    
    # Prints out all tasks on the screen

    print("---------------------------------")

    if len(task_list) == 0:
        print("There are no tasks.")
        print("-----------------------------------")

    for t in task_list:
        print("")
        print(t.display())
        print("-----------------------------------")

def main_menu():
    while True:
        # Get input from user
        print()
        if curr_user == 'admin':
            menu = input('''Select one of the following Options below:
        r - registering a user
        a - adding a task
        va - View all tasks
        vm - view my task
        gr - generate report
        ds - display statistics
        e - exit
        : ''').lower()
        else:
            menu = input('''Select one of the following Options below:
        r - registering a user
        a - adding a task
        va - view all tasks
        vm - view my task
        e - exit
        : ''').lower()

        if menu == 'r': # Register new user (if admin)
            reg_user()

        elif menu == 'a': 
            add_task()
            
        elif menu == 'va': # View all tasks
            view_all()

        elif menu == 'vm': # View my tasks
            view_mine()

        elif menu == 'gr' and curr_user == 'admin':
            generate_stat()

        elif menu == 'ds' and curr_user == 'admin': # If admin, display statistics
            display_stats()

        elif menu == 'e': # Exit program
            print('Goodbye!!!')
            exit()

        else: # Default case
            print("You have made a wrong choice, Please Try again")

def view_mine():
    print("-----------------------------------")
    has_task = False
    user_tasks_list = []
    for t in task_list:
            
        if t.username == curr_user:
            has_task = True
            user_tasks_list.append(t)
    for i, ta in enumerate(user_tasks_list):
                
        print(f'Task {i}')
        print(ta.display())
        print("-----------------------------------")

    if not has_task:
        print("You have no tasks.")
        print("-----------------------------------")

    while True:
        
        task_choice = input("Enter a number of task you would like to edit or '-1' to return to main menu: ").strip()
        if task_choice in [str(i) for i in range(len(user_tasks_list))]:
            if user_tasks_list[int(task_choice)].completed == "Yes":
                print("You can not edit completed task.")
            else:
        
                print('Task: ')
                print(user_tasks_list[int(task_choice)].display())
                to_change = input("""Choose option:
                1 - to change a person assigned to the task
                2 - to change due date
                3 - to mark as completed
                """).strip()

                if to_change == "1":
                    while True:
                        new_username = input("Please enter a name of new user assigned to this task: ")
                        if new_username in username_password:
                            user_tasks_list[int(task_choice)].username = new_username
                            print(f"This task is now reassigned to {new_username}")
                            break
                        else:
                            print("Choose different user.")

                elif to_change == "2":
                    while True:
                        new_due_date = input('Please enter a new date in format (DD-MM-YYYY): ')
                        try:
                            new_due_date_time = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT).date()
                            break
                        except:
                            print("Please enter new date in a proper format.")

                elif to_change == "3":
                    user_tasks_list[int(task_choice)].complete = 'Yes'
                    print("The task has been marked as completed")
            
        elif task_choice == '-1':
            break

        else: 
            print("Please enter a valid number.")


def generate_stat():
    
    # Generate statistics
    # task_overview.txt -> general statistics
    # user_overview.txt -> statistics for users
    
    # in task_overview.txt
    with open("task_overview.txt", 'w') as task_overview:
        # Checks how many tasks are in tasks.txt
        number_of_tasks = len(task_list)
        # Cheks if any tasks in the file.
        if number_of_tasks > 0:
            uncompleted_tasks = 0
            uncompleted_overdue = 0
            for task in task_list:
                if task.completed == "No":
                    uncompleted_tasks += 1
                    if curr_date > task.due_date:
                        uncompleted_overdue += 1
            completed_tasks = number_of_tasks - uncompleted_tasks

            
            overview_list =["-----------------------------------\n", 
            f"Total number of tasks: \t\t\t\t\t\t{number_of_tasks}\n",
            f"Total number of completed tasks: \t\t\t{completed_tasks}\n",
            f'Total number of uncompleted tasks: \t\t\t{uncompleted_tasks}\n',
            f'Total number of overdue uncompleted tasks: \t{uncompleted_overdue}\n',
            f'Percent of uncomplete tasks: \t\t\t\t{uncompleted_tasks/number_of_tasks*100:.0f} \n',
            f'Percent of uncomplete overdue tasks: \t\t{uncompleted_overdue/number_of_tasks*100:.0f} \n',
            "-----------------------------------"]
        
            task_overview.write("".join(overview_list))

        else:
            print("No tasks yet.")

    # user_overwiew.txt
    with open("user_overwiew.txt", "w") as user_overview:

        num_of_users = len(username_password)
        user_overview_global = [
            f"Total number of users: \t{num_of_users}\n",
            f"Total number of tasks: \t{number_of_tasks}\n"]
        
        
        for user in username_password:  
            users_tasks = []
            for task in task_list:
                if user == task.username:
                    users_tasks.append(task)

            total_tasks_number = len(users_tasks)
            if total_tasks_number == 0:
                no_tasks_user = ["-------------------------------\n",
                f"User: \t\t\t\t\t\t\t\t\t{user}\n",
                f"Total number of tasks: \t\t\t\t\t0  \n",
                "-------------------------------\n"]
                user_overview_global += no_tasks_user

            else:
                user_uncompleted_overdue = 0
                user_uncompleted = 0
                for t in users_tasks:
                    if t.completed == 'No':
                        user_uncompleted +=1
                        if curr_date > task.due_date:
                            user_uncompleted_overdue += 1
            
                user_completed = total_tasks_number - user_uncompleted
                    
                user_overview_local = [
                "-------------------------------\n"
                f"User: \t\t\t\t\t\t\t\t\t{user}\n",
                f"Total number of tasks: \t\t\t\t\t{total_tasks_number} \n",
                f"Percent of tasks assigned: \t\t\t\t{total_tasks_number/number_of_tasks*100:.0f} \n",
                f"Percent of completed tasks: \t\t\t{user_completed/total_tasks_number*100:.0f} \n",
                f"Percent of uncompleted tasks: \t\t\t{(user_uncompleted)/total_tasks_number*100:.0f} \n",
                f"Percent of uncompleted overdue tasks: \t{(user_uncompleted_overdue/total_tasks_number)*100:.0f}\n",
                "-------------------------------\n"]

                user_overview_global += user_overview_local

        user_overview.write("".join(user_overview_global))

    print("The reports has been generated")



def display_stats():

    # Displays general stats on the screen
    num_users = len(username_password.keys())
    num_tasks = len(task_list)
    print("-----------------------------------")
    print(f"Number of users: \t\t {num_users}")
    print(f"Number of tasks: \t\t {num_tasks}")
    print("-----------------------------------")


#########################
# Main Program
######################### 

main_menu()

