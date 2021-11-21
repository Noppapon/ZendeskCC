import requests
import json
import getpass #for safety reason when user input their password

invalid_command_msg = "Invalid command! Please re-enter a valid command."

def main():
    #Start of the program
    print("\nWelcome to the ticket viewer\n")
    subdomain = str(input("Please enter the subdomain name you want to access: "))
    email_address = str(input("Please enter your email address: "))
    password = getpass.getpass("Please enter your password (Hidden): ")

    #https:///{subdomain_name}.zendesk.com/api/v2/tickets.json', auth=('{email_address}', '{password}'
    tickets_request = requests.get('https://'+subdomain+'.zendesk.com/api/v2/tickets.json', auth = (email_address, password))
    
    if tickets_request.status_code == 200:
        print("Success!\n")
    elif tickets_request.status_code//100 == 4:
        print("Authentication failed, terminating the program...\n")
        return
    elif tickets_request.status_code//100 == 5:
        print("Server error, terminating the program...\n")
        return
    else:
        print("Unknown error occurred, terminating the program...\n")
        print("Status code: " + str(tickets_request.status_code))
        return
    
    tickets_json = tickets_request.json()

    m_or_q = None
    while True:
        m_or_q = input("Type 'menu' to view options or 'quit' to exit: ")
        if m_or_q == 'quit':
            print("\nThanks for using the viewer. Goodbye.")
            return
        elif m_or_q == 'menu':
            menu(tickets_json)
            return
        else:
            print(invalid_command_msg)

def menu(tickets_json):
    select_option_str = """
    Select view options:
    * Press 1 to view all tickets
    * Press 2 to view a ticket
    * Type 'quit' to exit
    Your input = """
    
    while True:
        option = input(select_option_str)
        if option == 'quit':
            print("Thanks for using the viewer. Goodbye.")
            return
        elif option == "1":
            #DO SOMETHING
            print("\n")
            tickets_list = tickets_json["tickets"]
            num_tickets = len(tickets_list)
            print("There is a total of " + str(num_tickets) + "tickets, 25 tickets will be displayed per page")
            print("n: next page, b: page before, q: quit, back to home screen\n")
            start_page = 0
            break_outer = False


            while True:
                print("PAGE " + str(start_page + 1))
                for i in range(start_page*25, (start_page*25) + 25):

                    if i < num_tickets:
                        ticket_num = i + 1 #omit ticket_num = 0
                        created_at = tickets_list[i]["created_at"]
                        subject = tickets_list[i]["subject"]
                        print("ticket number = "+ str(ticket_num) + " | Created at " + str(created_at[:10]) + " | Subject: " + str(subject))
                    else:
                        break

                while True:
                    print("\n")
                    command = input("n: next page, b: page before, q: quit, back to home screen. Your input = ")
                    if command == "n":
                        if (start_page + 1)*25 < num_tickets:
                            start_page += 1
                        else:
                            print("This is the last page, re-displaying page " + str(start_page + 1))
                        break
                    elif command == "b":
                        if (start_page - 1)*25 >= 0:
                            start_page -= 1
                        else:
                            print("This is the first page, re-displaying page 1")
                        break
                    elif command == "q":
                        break_outer = True
                        break
                    else:
                        print(invalid_command_msg)
                if break_outer == True:
                    break

        elif option == "2":
            tickets_list = tickets_json["tickets"]
            num_tickets = len(tickets_list)
            while True:
                command = input("\nInput your ticket number, or press q: quit, back to home screen. Your input = ")
                if command.isnumeric():
                    num = int(command) - 1 #index starts from 1 in the interface
                    if num < num_tickets and num >= 0:
                        requester_id = tickets_list[num]["requester_id"]
                        assignee_id = tickets_list[num]["assignee_id"]
                        subject = tickets_list[num]["subject"]
                        description = tickets_list[num]["description"]
                        created_at = tickets_list[num]["created_at"]

                        print("\n")
                        print("--------"*5)
                        print("SUBJECT: " + subject + "     Created at: " + str(created_at))
                        print("\n")
                        print(description)
                        print("\n")
                        print("requester_id = " + str(requester_id) + "      assignee_id = " + str(assignee_id))
                        print("--------"*5)
                        break
                    else:
                        print("This ticket number does not exist, please re-enter a new ticket number")
                elif command == "q":
                    break
                    
                else:
                    print(invalid_command_msg)
            
        else:
            print(invalid_command_msg)




