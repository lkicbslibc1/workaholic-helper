from datetime import datetime, timedelta
import time
import os
import webbrowser
import random
import json
import requests
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

with open('programs.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

def find_matching_question(user_input, data):
    closest_question = None
    closest_answer = None
    highest_similarity_score = 0

    for qa_pair in data:
        if 'question' in qa_pair:
            question = qa_pair['question']
            similarity_score = fuzz.ratio(user_input, question)

            if similarity_score > highest_similarity_score:
                highest_similarity_score = similarity_score
                closest_question = question
                closest_answer = qa_pair['answer']

    return closest_question, closest_answer


name = ""
worklist = []

          
agreemessage = ("yes", "yeah", "yea","ok","okay","go on","k", "sure", "why not", "ya", "shoot", "go", "fine", "thanks","thx","thank")
disagreemessage = ("no", "nah", "naw", "nuh uh", "nope", "not a chance", "na", "stop")

def get_worklistname(name):
    return name + "_worklist.json"

def add_work(worklist, workname,due_date, priority):
    worklist.append({"work": workname, "due_date": due_date, "priority": priority})

def load_worklist(filename):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    else :
        return []

def save_worklist(worklist, filename):
    with open(filename, "w") as file:
        json.dump(worklist, file)

def show_worklist(worklist):
    today = datetime.now().date()
    print("\n   [ Here's your unfinished works ]\n")

    late_works = []
    due_today_works = []
    future_works = []

    for work in worklist:
        due_date = datetime.strptime(work["due_date"], "%d-%m-%Y").date()
        days_left = (due_date - today).days
        days_late = (today - due_date).days

        if days_late > 0:
            late_works.append((work, days_late))
        elif days_left == 0:
            due_today_works.append(work)
        else:
            future_works.append(work)
    late_works.sort(key=lambda x: x[1])
    future_works.sort(key=lambda x: (datetime.strptime(x["due_date"], "%d-%m-%Y").date() - today).days)

    print("{:<10} {:<30} {:<15} {:<20}".format("Priority:", "Name Of Work:", "Due Date:", "Status:"))

    for work, days_late in late_works:
        if int(work['priority']) == 1:
            prioritystars = " ***"
        elif int(work['priority']) == 2:
            prioritystars = " **"
        else:
            prioritystars = ""
        print("{:<10} {:<30} {:<15} {:<20}".format(prioritystars, work['work'], work['due_date'], "***Days late: {} ***".format(days_late)))

    for work in due_today_works:
        if int(work['priority']) == 1:
            prioritystars = " ***"
        elif int(work['priority']) == 2:
            prioritystars = " **"
        else:
            prioritystars = ""
        print("{:<10} {:<30} {:<15} {:<20}".format(prioritystars, work['work'], work['due_date'], "DUE TODAY"))

    for work in future_works:
        due_date = datetime.strptime(work["due_date"], "%d-%m-%Y").date()
        days_left = (due_date - today).days
        days_left_str = "0" if days_left == 0 else str(days_left)

        if int(work['priority']) == 1:
            prioritystars = " ***"
        elif int(work['priority']) == 2:
            prioritystars = " **"
        else:
            prioritystars = ""
        print("{:<10} {:<30} {:<15} {:<20}".format(prioritystars, work['work'], work['due_date'], "Days left: {}".format(days_left_str)))



def getname():
    file_path = "name.txt"
    global name
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            name = file.read()
            return name
    else:
        print("Aidy : It looks like it's your first time using this program.")
        name = input("Aidy : What is your name, buddy? ")
        with open(file_path, "w") as file:
             file.write(name)
def Hello():
    print (40*"=")
    print ("""            _____ _______     __
     /\   |_   _|  __ \ \   / /
    /  \    | | | |  | \ \_/ / 
   / /\ \   | | | |  | |\   /  
  / ____ \ _| |_| |__| | | |   
 /_/    \_\_____|_____/  |_|   
                               
                               """)
    print (40*"=")
    hour = datetime.now().hour
    if hour >= 0 and hour< 12:
        print("\nAidy : Good morning,", name + ". How can I help you?")
    elif hour >= 12 and hour < 15:
        print("\nAidy : Good afternoon," , name + ". How can I help you?")
    else:
        print("\nAidy : Good evening,", name + ". How can I help you?")

def rockpaperscissor ():
        global name
        option = ("rock", "paper", "scissors")
        print ("Aidy : Okay, 'r' is for rock, 'p' is for paper and 's' is for scissors !)")
        aidyoption = random.choice(option)
        tieresponse = ("What a fate :D", "It's a tie! cool!", "It's a tie, Such a destiny >:D", "A tie? I guess great minds think alike. ", "Unbelievable! We're in sync.")
        winresponse = ("Call me champion >:)", "Look like luck was on my side, Hehehe", "They say practice makes perfect, and I just proved it! Winner!","I win ! What am i gonna do to the lose one now? hehe", "Victory is mine!")
        loseresponse = ("Ow, I thought I had it. Good game, pal!", "You're the winner this time. Congrats.","I lose. Well played!", "Nice move. You win!", "You win fair and square, so I will put off the date I invade the earth :)", "Ochie :P")
        time.sleep(0.3)
        playeroption = input("What's your move? : ").lower()
        if playeroption == "r":
            playeroption = "rock"
        elif playeroption == "p":
            playeroption = "paper"
        elif playeroption == "s":
            playeroption = "scissors"

        print (name , " : ",playeroption)
        print ("Aidy : ",aidyoption ,"!")
        time.sleep(0.3)
        if playeroption == aidyoption :
            response = random.choice(tieresponse)
            print ("Aidy : ", response)
        elif playeroption == "rock" and aidyoption == "paper":
            response = random.choice(winresponse)
            print ("Aidy : ", response)
        elif playeroption == "rock" and aidyoption == "scissors":
            response = random.choice(loseresponse)
            print("Aidy : ", response)
        elif playeroption == "paper" and aidyoption == "rock":
            response = random.choice(loseresponse)
            print("Aidy : ", response)
        elif playeroption == "paper" and aidyoption == "scissors":
            response = random.choice(winresponse)
            print("Aidy : ", response)
        elif playeroption == "scissors" and aidyoption == "paper":
            response = random.choice(loseresponse)
            print("Aidy : ", response)
        elif playeroption == "scissors" and aidyoption == "rock":
            response = random.choice(winresponse)
            print("Aidy : ", response)
        else:
            print ("Aidy : No-no, It's not in an option >:( ")

def notify_due_work(worklist):
    today = datetime.now().date()
    three_days_delta = timedelta(days=3)
    notifications = []
    
    for work in worklist:
        due_date = datetime.strptime(work["due_date"], "%d-%m-%Y").date()
        days_left = (due_date - today).days
        
        if days_left == 0:
            notifications.append(("Your work '{}' is due today !! ".format(work['work']), days_left))
        elif 0 < days_left <= 3:
            notifications.append(("You have {} days left to finish '{}'.".format(days_left, work['work']), days_left))
    
    if not notifications:
        print("No work due today or this 3 days !")
        return
    
    notifications.sort(key=lambda x: (x[1], x[0]))
    
    print("\n   [ Today's Notifications ]")
    for notification, _ in notifications:
        print(notification)

def notify():
    worklist = load_worklist(get_worklistname(name))
    notify_due_work(worklist)

def save_wakeup_times(wakeup_times):
    file_path = "wakeup_times.json"
    with open(file_path, "w") as file:
        json.dump(wakeup_times, file)

def load_wakeup_times(filename):
  try:
    if os.path.exists(filename): 
        with open(filename, "r") as file:
           wakeup_times = json.load(file) 
           return wakeup_times
    else:
        return {}
  except Exception as e:
        print("Error loading wake-up times:", str(e))
        return {}

def notify_sleep_status(wakeup_times):
    print("\n\n---------------- WAKE-UP TIMES ----------------")
    for day, wakeup_time in wakeup_times.items():
        print("{:<30} {:<15}".format(day.capitalize(), wakeup_time))
    time.sleep(0.3)

def edit_wakeup_times(wakeup_times):
    while True:
        print("\nType 'back' to go to the previous page")
        day_to_edit = input("Which day's wake-up time do you want to edit? : ")

        if day_to_edit in wakeup_times:
            while True:
                new_wakeup_time = input("Enter the new wake-up time for {} (e.g., 07:00 AM) : ".format(day_to_edit))
                new_wakeup_time = new_wakeup_time.upper()
                standardized_time = validate_wakeup_time(new_wakeup_time)

                if standardized_time:
                    wakeup_times[day_to_edit] = standardized_time
                    print("Wake-up time for {} updated successfully!".format(day_to_edit))
                    save_wakeup_times(wakeup_times)
                    break
                else:
                    print("Invalid time format. Please enter the time in the format 'hh:mm AM/PM'.")
        elif day_to_edit == "back":
            break
        else:
            print("Invalid day. Please enter a valid day.")
       

def set_wakeup_times(wakeup_times):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    print("Aidy: Let's set your wake-up times for each day \n")
    for day in days:
         while True:
            wakeup_time = input("What time do you usually wake up on {} (e.g., 07:00 AM): ".format(day))
            wakeup_time = wakeup_time.upper()
            standardized_time = validate_wakeup_time(wakeup_time)
            
            if standardized_time:
                wakeup_times[day] = standardized_time
                break
            
    save_wakeup_times(wakeup_times)
    print("Aidy: Wake-up times have been set successfully!")


def validate_wakeup_time(input_time):
    try:
        datetime.strptime(input_time, "%I:%M %p")
        return input_time
    except ValueError:
        print("Invalid time format. Please enter the time in the format 'hh:mm AM/PM'.")
        return None

def print_wakeup(wakeup_times):
    now = datetime.now()
    today = now.strftime("%A")

    next_day = (now + timedelta(days=1)).strftime("%A")  
    if next_day in wakeup_times:
        wakeup_time = datetime.strptime(wakeup_times[next_day], "%I:%M %p").time()

        wakeup_datetime = datetime.combine(now.date(), wakeup_time)
        
        if wakeup_datetime <= now:
            wakeup_datetime += timedelta(days=1)
        
        time_until_wakeup = wakeup_datetime - now
        hours_until_wakeup = time_until_wakeup.seconds // 3600
        minutes_until_wakeup = (time_until_wakeup.seconds // 60) % 60
        if time_until_wakeup < timedelta(hours=9):
            print(f"\nAidy: It's only {hours_until_wakeup} hours and {minutes_until_wakeup} minutes until your wakeup time on {next_day}!")
    else:
        print("Aidy: There's no wakeup time set for the next day.")


def help():
    global name
    global agreemessage
    wakeup_times = load_wakeup_times("wakeup_times.json")
    while True:
        print ("\n\n   [ HELP PAGE ]")
        time.sleep(0.1)
        print ("\nWant to change a name? - type 1 \nNotificate you if you're late at night - type 2 \nIntroduction - type 3")
        helpcommand = input("\n\n"+name+" : ")
        if helpcommand == "1":
            print ("\n\n---------------- CHANGING NAME ----------------")
            newname = input("Aidy : Please enter your new name - ")
            with open("name.txt", "w") as file:
                file.write(newname)
            name = newname
            print("Name changed successfully!")
            time.sleep(0.3)

        elif helpcommand == "2":
           if not wakeup_times:
                print("Aidy: It seems you haven't set your wake-up times yet. Let's set them up! \n")
                set_wakeup_times(wakeup_times)
           while True:
               notify_sleep_status(wakeup_times)
               save_wakeup_times(wakeup_times)
               edittime = input("\nDo you want to edit your wake-up time ?  (yes/no) - ")
               if edittime in agreemessage or "yes" in edittime:
                   edit_wakeup_times(wakeup_times)
               else:
                   break
               time.sleep(1)
        elif helpcommand == "3":
            time.sleep(0.3)
            print ("Aidy : Heya! My name is Aidy \nAidy : and my mission is to make your work-life easier!")
            time.sleep(0.2)
            print ("Aidy : You can type 'back' to return to the previous page y'know")
            time.sleep(0.2)
            print("Aidy : And this is what I can do :D")
            time.sleep(0.2)
            print ("\n1. Work Schedule section :\n   - You can manage your work schedule here, and Aidy will remind you as the due dates get closer. ")
            print ("\n2. Work advice :\n   - you can ask Aidy for work-related advice or request a summary of a lengthy article.")
            print ("\n3. Free Chat : \n   - you can ask aidy for open website for you if you are busy and if you are tired you can ask aidy to play game with you\n   - You can just chill and chat with Aidy. he'll do whatever it takes to entertain you.(comming soon..)")
            input("( Press any key to continue )")
        elif helpcommand == "back":
            time.sleep (0.3)
            break

command = {
    "changename": ["change a name", "fix a name", "rename"],
    "changeduedate": ["change a deadline", "change a due date","fix a deadline","fix a due date","delay the date","postpone a date"],
    "changepriority": ["change priority", "priority"],   
    "hello" : ["Hi", "Hello", "Aidy", "Yo","help"],
    "addwork" : ["add work", "new work", "add more work"],
    "satisfy" : ["ok", "good","thank", "wow","well","thx"],
    "showwork": ["show work", "list of work","scheduled","show all work"],
    "mostimportant" : ["show a most important work", "first priority","important appointment","important work"],
    "specificwork" : ["due on", "has a deadline","deadline of","deadline is","due in","deadline in"],
    "delete1" : ["remove all","delete all","remove every","delete every"],
    "deletelate" : ["remove all late work", "all work pass deadline","overdue"],
    "remove" : ["remove","delete"]
}

def match_command(user_input):
    highest_score = 0
    matched_command = None
    
    for cmd, keywords in command.items():
        for keyword in keywords:
            similarity_score = fuzz.ratio(user_input, keyword)
            if similarity_score > highest_score:
                highest_score = similarity_score
                matched_command = cmd
    
    threshold = 80
    if highest_score >= threshold:
        return matched_command
    else:
        choices = [keyword for keywords in command.values() for keyword in keywords]
        closest_match = process.extractOne(user_input, choices)
        if closest_match[1] >= threshold:
            for cmd, keywords in command.items():
                if closest_match[0] in keywords:
                    return cmd
    return None

def notlate(work):
    today = datetime.now().date()
    due_date = datetime.strptime(work["due_date"], "%d-%m-%Y").date()
    return due_date >= today


#########################################################################################
def task():
  try:
    global name
    worklist = load_worklist(get_worklistname(name))
    time.sleep(0.1)
    print ("\n\n---------------- FIRST PAGE ----------------")
    time.sleep(0.1)
    print ("\nWork schedule - type : 1 \nWork advice? - type : 2\nFree chat - type : 3")
    print ("** For additional help type 'help' **")
    commandwork = input("\n\n"+name+" : ")
    if commandwork == "1":
      global agreemessage
      menuwork = True
      
      while True:
        if menuwork:
            print ("\n\n---------------- WORK MANAGING ----------------")
            time.sleep(0.1)
            print("\nShow your work schedule - type : 1 \nAdd new scheduled - type : 2\nModify your scheduled - type : 3\n(Or, you can simply type commands to manage your work schedule.)")
            managework = input(name + " : ").lower()
        else:
           managework = input(name + " : ").lower()
        if managework == "1":
            show_worklist(worklist)
            time.sleep(1.5)
        elif managework == "2":
            while True:
                workname = input("Enter the name of work : ")
                if workname.lower() == "back":
                    break
                while True:
                    duedate = input("Enter the due date (ex. 31-8-2023): ")
                    try:
                        datetime.strptime(duedate, "%d-%m-%Y")
                        break
                    except ValueError:
                        print("Aidy : Invalid date format. Please enter the date in d-m-Y format")
        
                while True:
                            priority = input("Please enter the priority (1=highest, 5=lowest) : ")
                            if priority.isdigit() and 1 <= int(priority) <= 5:
                                break
                            else:
                                print("Aidy : Invalid input. Please enter a number between 1 and 5.")
                add_work(worklist, workname, duedate, priority)
                print("Work scheduled successfully!")
                show_worklist(worklist)
                save_worklist(worklist, get_worklistname(name))
                time.sleep(0.1)
                another_work = input("\nDo you want to add more work? (yes/no) : ").lower()
                if another_work in disagreemessage:
                    break


        elif managework == "3":
                show_worklist(worklist)
                modified_worklist = worklist.copy()
                work_to_modify = input("\nEnter the name of your work that you wanted to modify/remove \n(If multiple works, use 'and' in between) : ")
                work_names_to_modify = [name.strip() for name in work_to_modify.split("and")]
                works_to_modify = []
                for work in modified_worklist:
                    if work["work"] in work_names_to_modify:
                        print("\nWork found!")
                        print("Workname:", work["work"])
                        print("Due Date:", work["due_date"])
                        time.sleep(0.3)
                        works_to_modify.append(work)

                if len(works_to_modify) > 0:
                    modify_option = input("Do you want to modify or remove these works? (modify/remove) : ").lower()

                    if modify_option == "remove":
                        for work in works_to_modify:
                            modified_worklist.remove(work)
                        print(len(works_to_modify), "work(s) removed successfully!")
                        time.sleep(0.5)
                        worklist = modified_worklist
                        save_worklist(worklist, get_worklistname(name))
                        time.sleep(0.3)
                        show_worklist(modified_worklist)

                    elif modify_option == "modify":
                         if len(works_to_modify) == 1:
                            work = works_to_modify[0]
                            new_name = input("Enter the new name for this work: ")
                            work["work"] = new_name
                            while True:
                                new_due_date = input("Enter the new due date for this work (ex. 31-8-2023) : ")
                                try:
                                    datetime.strptime(new_due_date, "%d-%m-%Y")
                                    break
                                except ValueError:
                                    print("Aidy : Invalid date format. Please enter the date in d-m-Y format")
                            
                            work["due_date"] = new_due_date
                            print("Work due date modified successfully!")
                            time.sleep(0.5)
                            save_worklist(worklist, get_worklistname(name))
                            show_worklist(modified_worklist)
                         else:
                            while True:
                                new_duedate = input("Enter the new due date for these works (ex. 31-8-2023) : ")
                                try:
                                        datetime.strptime(new_duedate, "%d-%m-%Y")
                                        break
                                except ValueError:
                                        print("Aidy : Invalid date format. Please enter the date in d-m-Y format")
                            for work in works_to_modify:
                                work["due_date"] = new_duedate
                            print("Due dates modified successfully!")
                            time.sleep(0.5)
                            save_worklist(worklist, get_worklistname(name))
                            show_worklist(worklist)
                    
                else:
                    print("No work found in your schedule. Please make sure you input the correct name(s).")
                    time.sleep(0.5)

        elif managework == "back":
                break
        elif managework == "":
            pass

        else:
            menuwork = False
            userinput = match_command(managework)
            worklist = load_worklist(get_worklistname(name))
            worklistformodify = worklist.copy()
            while True:
                if userinput == "changename":
                        time.sleep(0.3)
                        ask = input("Aidy : You want to change your work/appointment name ? \n"+name+" : ")
                        if ask in agreemessage:
                            workoldname = input("Aidy : Please enter the name of work you'd like to change.\n"+name+" : ")
                            found = False
                            for work in worklistformodify:
                                if work["work"] == workoldname:
                                    time.sleep(0.3)
                                    print("Aidy : Work found!")
                                    print("Workname:", work["work"])
                                    print("Due Date:", work["due_date"])
                    
                                    newname = input("Aidy : Okay, now enter the new name for this work\n"+name+" : ")
                                    work["work"] = newname
                                    found = True
                                    break
            
                            if found:
                                save_worklist(worklistformodify, get_worklistname(name))
                                time.sleep(0.3)
                                print("Aidy : Done!")
                                time.sleep(0.3)
                                print("Aidy : Here's the work you renamed")
                                print("Workname:", newname)
                                print("Due Date:", work["due_date"])
                                break
                            else :
                                    print ("Aidy : I can't seem to find that work. Please double-check if you've entered the correct name?")
                        else :
                            break

                elif userinput == "changeduedate":
                        time.sleep(0.3)
                        ask = input("Aidy : You want to change your work/appointment duedate ? \n"+name+" : ")
                        if ask in agreemessage:
                            time.sleep(0.3)
                            workoldduedate = input("Aidy : Please enter the name of work for due date update.\n"+name+" : ")
                            found = False
                            for work in worklistformodify:
                                if work["work"] == workoldduedate:
                                    time.sleep(0.3)
                                    print("Aidy : Work found!")
                                    print("Workname:", work["work"])
                                    print("Due Date:", work["due_date"])
                    
                                    newduedate = input("Aidy : Okay, now enter the new due date for this work\n"+name+" : ")
                                    try:
                                        datetime.strptime(newduedate, "%d-%m-%Y")
                                        break
                                    except ValueError:
                                        print("Aidy : Invalid date format. Please enter the date in d-m-Y format")
                                    work["due_date"] = newduedate
                                    found = True
                                    break
            
                            if found:
                                save_worklist(worklistformodify, get_worklistname(name))
                                time.sleep(0.3)
                                print("Aidy : Done!")
                                time.sleep(0.3)
                                print("Aidy : Here's the work you updated")
                                print("Workname:", work["work"])
                                print("Due Date:", newduedate)
                                break
                            else :
                                    print ("Aidy : I can't seem to find that work. Please double-check if you've entered the correct name?")
                        else :
                            break
                elif userinput == "changepriority":
                        time.sleep(0.3)
                        ask = input("Aidy : You want to change your work/appointment priority ? \n"+name+" : ")
                        if ask in agreemessage:
                            time.sleep(0.3)
                            workolddpriority = input("Aidy : Please provide the name of the work you want to update its priority\n"+name+" : ")
                            found = False
                            for work in worklistformodify:
                                if work["work"] == workolddpriority:
                                    time.sleep(0.3)
                                    print("Aidy : Work found!")
                                    print("Workname:", work["work"])
                                    print("Priority:", work["priority"])                
                                    while True:
                                        time.sleep(0.3)
                                        newpriority = input("Aidy : Please enter how much its priority (1=highest, 5=lowest)\n"+name+" : ")                                  
                                        if newpriority.isdigit() and 1 <= int(newpriority) <= 5:
                                            break
                                        else:
                                            print("Aidy : Invalid input. Please enter a number between 1 and 5.")
                                    work["priority"] = newpriority
                                    found = True
                                    break
            
                            if found:
                                save_worklist(worklistformodify, get_worklistname(name))
                                time.sleep(0.3)
                                print("Aidy : Done!")
                                time.sleep(0.3)
                                print("Aidy : Here's the work you updated")
                                print("Workname:", work["work"])
                                print("Priority:", newpriority)
                                break
                            else :
                                    print ("Aidy : I can't seem to find that work. Please double-check if you've entered the correct name?")
                        else :
                            break
                elif userinput == "showwork":
                    show_worklist(worklist)
                    break
                elif userinput == "addwork":
                    time.sleep(0.3)
                    ask = input("Aidy : It seems you want to add a new work?\n"+name+" : ")
                    if ask in disagreemessage:
                        break
                    while True:
                        time.sleep(0.3)
                        print ("Aidy : OK! let me help")
                        workname = input("Aidy : Please enter the name of work \n"+name+" : ")
                        while True:
                               duedate = input("Aidy : now please enter the due date (ex.31-8-2023) \n"+name+" : ")
                               try:
                                    datetime.strptime(duedate, "%d-%m-%Y")
                                    break
                               except ValueError:
                                    print("Aidy : Invalid date format. Please enter the date in d-m-Y format")
                        while True:
                            priority = input("Aidy : Okay, Please enter the priority (1=highest, 5=lowest)\n"+name+" : ")
                            if priority.isdigit() and 1 <= int(priority) <= 5:
                                break
                            else:
                                print("Aidy : Invalid input. Please enter a number between 1 and 5.")
                        add_work(worklist, workname, duedate, priority)
                        print("Aidy : Done!")
                        time.sleep(0.3)
                        print("Workname:", workname)
                        print("Due date:", duedate)
                        print("Priority:", priority) 
                        save_worklist(worklist, get_worklistname(name))
                        time.sleep(0.3)
                        another_work = input("Aidy : Do you want to add more work? (yes/no) \n"+name+" : ").lower()
                        if another_work in disagreemessage:
                            break
                       
                elif userinput == "mostimportant":
                    ask = input("Aidy : You want to know only the important one on your schedule?\n"+name+" : ")
                    if ask in agreemessage:
                        print("\n   [ Here's your important and unfinished works ]\n")
                        today = datetime.now().date()
                        important_works = []
                        for work in worklist:
                            due_date = datetime.strptime(work["due_date"], "%d-%m-%Y").date()
                            days_left = (due_date - today).days
                            days_late = (today - due_date).days

                            if work['priority'] == "1" or work['priority'] == "2":
                                important_works.append((work, days_late, days_left))
                                break

                        if not important_works:
                            print("No important and unfinished works found.")
                            break
                        else:
                            print("{:<10} {:<30} {:<15} {:<20}".format("Priority:", "Name Of Work:", "Due Date:", "Status:"))

                            for work, days_late, days_left in important_works:
                                priority_stars = " ***" if int(work['priority']) == 1 else " **"
                                if days_late > 0:
                                    status = "***Days late: {} ***".format(days_late)
                                elif days_left == 0:
                                    status = "DUE TODAY"
                                else:
                                    status = "Days left: {}".format(days_left)

                                print("{:<10} {:<30} {:<15} {:<20}".format(priority_stars, work['work'], work['due_date'], status))
                                break
                        break
                    else:
                        break

                elif userinput == "specificwork":
                    time.sleep(0.3)
                    ask = input("Aidy : Oh, Want to see work that's due on a specific day?\n"+name+" : ")
                    today = datetime.now().date()
                    if ask in agreemessage:                            
                        while True:
                               showondate = input("Aidy : Please enter the deadline (d-m-Y format, e.g., '28-10-2023') \n" + name + " : ")
                               try:
                                    datetime.strptime(showondate, "%d-%m-%Y")
                                    break
                               except ValueError:
                                    print("Aidy : Invalid date format. Please enter the date in d-m-Y format")
                        matchdate = datetime.strptime(showondate, "%d-%m-%Y").date()
                        today = datetime.now().date()

                        matchwork = []

                        for work in worklist:
                            due_date = datetime.strptime(work["due_date"], "%d-%m-%Y").date()

                            if due_date == matchdate:
                                matchwork.append(work)

                        if matchwork:
                            matchwork.sort(key=lambda x: (datetime.strptime(x["due_date"], "%d-%m-%Y").date() - today).days)
                            print("{:<10} {:<30} {:<20}".format("Priority:", "Name Of Work:", "Status:"))
                            for work in matchwork:
                                due_date = datetime.strptime(work["due_date"], "%d-%m-%Y").date()
                                days_left = (due_date - today).days
                                if days_left < 0:
                                    prioritystars = " ***"
                                    print("{:<10} {:<30} {:<20}".format(prioritystars, work["work"], "Days late: " + str(abs(days_left))))
                                elif days_left == 0:
                                    prioritystars = " DUE TODAY"
                                    print("{:<10} {:<30} {:<20}".format(prioritystars, work["work"], work["due_date"]))
                                else:
                                    prioritystars = ""
                                    print("{:<10} {:<30} {:<20}".format(prioritystars, work["work"], "Days left: " + str(days_left))) 
                        else:
                            print(f"Aidy : No works are due on {matchdate.strftime('%d-%m-%Y')}.")
                        break
                    else:
                        break
                elif userinput == "delete1":
                    ask = input("Aidy : You want me to delete ALL of the work/appointments in your schedule, Am I right?\n"+name+" : ")
                    if ask in agreemessage or ask not in agreemessage:
                        askagain = input("Aidy : Are you sure? delete everything on your schedule?\n"+name+" : ")
                        if askagain in agreemessage:
                            worklist.clear()
                            print("Aidy : All work/appointments have been deleted from your schedule.")
                            save_worklist(worklist, get_worklistname(name))
                        else:
                            print("Aidy : Okay :)")
                        break
                    else:
                        break
                elif userinput == "deletelate" :
                    time.sleep(0.3)
                    ask = input("Aidy : You want me to delete all of the work/appointments that pass its deadline , Am I right?\n"+name+" : ")
                    if ask in agreemessage or ask not in agreemessage:
                        notlateworks = [work for work in worklist if notlate(work)]
                        worklist.clear()
                        worklist.extend(notlateworks)
                        time.sleep(0.3)
                        print("Aidy: Roger that, overdue work/appointments have been deleted from your schedule")
                        save_worklist(worklist, get_worklistname(name))
                    
                    else:
                        time.sleep(0.3)
                        print("Aidy: Got it. No overdue work/appointments were deleted")
                        
                    break
                elif userinput == "remove":
                    time.sleep(0.3)
                    ask = input("Aidy: Do you want to delete some work from your schedule?\n"+name+" : ")
    
                    if ask in agreemessage or ask not in agreemessage:
                        time.sleep(0.3)
                        work_to_remove = input("Aidy: Enter the name of the work(s) you want to remove\n"+name+" : ")
                        work_names_to_remove = [name.strip() for name in work_to_remove.split("and")]
                        removed_works = []
                        modified_worklist = worklist.copy()
        
                        for work in modified_worklist:
                            if work["work"] in work_names_to_remove:
                                print("\nWork found!")
                                print("Workname:", work['work'])
                                print("Due Date:",work['due_date'])
                                time.sleep(0.3)
                                removed_works.append(work)
                
                        if removed_works:
                            for work in removed_works:
                                modified_worklist.remove(work)
                            print(f"{len(removed_works)} work(s) removed successfully!")
                            time.sleep(0.5)
                            worklist = modified_worklist
                            save_worklist(worklist, get_worklistname(name))
                            break
                        else:
                            print("Aidy: I couldn't find any matching work. Please double-check the work name(s) you entered.")
                            break
                    else:
                        print("Aidy: Okay, no work will be removed.")
                    break


                elif userinput == "hello":
                    greeting = ("Hello!, How can I help you with your scheduled?", "Heya, May I help you?", "Aidy's at you service :D","Greetings!","Hmm?")
                    said = random.choice(greeting)
                    time.sleep(0.3)
                    print ("Aidy : "+said)
                    break
                elif userinput == "satisfy":
                    urwelcome = ("Glad I could help :D", "Let me know if you need me","Anytime!", "It's good to know I could support you!","Mission accomplished :D")
                    said = random.choice(urwelcome)
                    time.sleep(0.3)
                    print ("Aidy : "+said)
                    break
                elif userinput == "back":
                    break
                else:
                    print("Aidy : I'm sorry, I'm a bit confused.  Can you please rephrase that?")
                    break


    elif commandwork == "2":
        print("\n\n---------------- ADVICE ----------------")
        print ("Aidy : Here's some advice I can give to you :D")
        time.sleep(0.3)
        print ("\n - summarize an article\n - about working programs  \n - about decoration ideas ")
        while True:   
            user_input = input(name + " : ").lower()
            response = None
            if user_input == "back":
                break

            else :
                    for qa_pair in data:
                         if 'question' in qa_pair and user_input == qa_pair['question']:
                            print(f"Answer: {qa_pair['answer']}")
                            break
                    questions = [qa_pair['question'] for qa_pair in data if 'question' in qa_pair]
                    tfidf_vectorizer = TfidfVectorizer()
                    tfidf_matrix = tfidf_vectorizer.fit_transform(questions + [user_input])
                    similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])[0]
                    most_similar_index = similarity_scores.argmax()
                    most_similar_question = questions[most_similar_index]
                    string_similarity_score = fuzz.ratio(user_input, most_similar_question)
                    similarity_threshold = 0.8

                    if similarity_scores[most_similar_index] > similarity_threshold:
                        print(f"Answer: {data[most_similar_index]['answer']}")
                    else:
                        closest_question, closest_answer = find_matching_question(user_input, data)

                        if closest_question and closest_answer:
                            print("Aidy:", closest_answer)
                        else:
                            print("Aidy: I'm sorry, I couldn't find an answer to your question.")
                

    elif commandwork == "3":
      print ("\n\n---------------- TALK ----------------")
      time.sleep(0.3)
      print ("Aidy : Let's talk! :D \n(Type 'back' to go to previous page)")
      time.sleep(0.3)
      print("Aidy : If you are bored or tired with work. You can play some game with me!")
      while True:
          user_input = input(name + " : ").lower()
          if user_input.startswith("open "):
                website_name = user_input.split("open ", 1)[1].split()[0]
                if website_name == "yt":
                    website_name = "youtube"
                elif website_name == "ig":
                      website_name = "instagram"
                elif website_name == "fb":
                    website_name = "facebook"
                elif website_name == "gg":
                    website_name = "google"
                elif website_name == "twitter":
                    website_name = "x"
                web_url = "https://" + website_name + ".com"
                webbrowser.open(web_url)
                print("Aidy: Opening", website_name.capitalize(), ", Enjoy!")

          elif "play" in user_input or "bored" in user_input or "game" in user_input:
               wannaplay = input("Aidy : Do you want to play a game with me? such as rock paper scissors \n" + name +" : ")
               if wannaplay in agreemessage or "yes" in wannaplay:
                while True:
                   rockpaperscissor()
                   time.sleep(0.3)
                   again = input("\nAidy: Do you want to play again? - ").lower()
                   if again in disagreemessage or "no" in user_input:
                       print("Aidy: Okay, Let me know if you need anything else!")
                       break
               else:
                   print ("Aidy : Okay, we won't ;(")
                   if "bored" in user_input :
                       time.sleep(0.3)
                       answer =  input("Aidy : How about I share an idea to help you kick boredom to the curb?\n"+name+" : ")
                       if answer in agreemessage or "yes" in answer:
                           idea = ("How about playing a online game? Multiplayer games or explore single-player adventures would be fun!.",
                                   "How about journaling? Write down your thoughts, ideas, and experiences to reflect on and revisit them later",
                                   "How about help me take over the world >:)",
                                   "How about painting? You can draw anything you want. That's the literally powerful power of all y'know :D",
                                   "Doing a DIY stuff? like making a vending machine, sewing a doll, or crafting a keychain?",
                                   "How about listening to music? I personally enjoy pop music :D",
                                   "Hold a pretend cooking show in your kitchen, complete with dramatic commentary and taste tests.",
                                   "Start an imaginary debate between two different types of colors to determine which one is the coolest one.",
                                   "Write a song about your love life.",
                                   "Have a debate about life between people from the medieval and modern times.",
                                   )
                           randomidea = random.choice(idea)
                           time.sleep (0.3)
                           print ("Aidy : "+ randomidea)
                           if user_input in disagreemessage or "no" in user_input:
                               print ("Aidy : "+ randomidea)
                           elif user_input in agreemessage or "yes" in user_input or "thank" in user_input:
                               glad = ("It was my pleasure to help.", "It's good to know I could support you!", "Glad I could help!","I'm here with my helpful cape on >:)", "Mission accomplished :D")
                               gladrandom = random.choice(glad)
                               print("Aidy : "+gladrandom)
          elif user_input == "back":
               break

    elif commandwork == "help":
        help()
    else:
         pass
  except Exception as e:
     print(f"An error occurred: {str(e)}")


getname()
Hello()
notify()
wakeup_times = load_wakeup_times("wakeup_times.json")
print_wakeup(wakeup_times)
while True:
    task()