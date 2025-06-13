from datetime import datetime
import random 
from fpdf import FPDF
from getpass import getpass

prompts = ["Who do you trust most? Why?",
            "What are your strengths in relationships (kindness, empathy, etc.)?",
            "How do you draw strength from loved ones?",
            "What do you value most in relationships (trust, respect, sense of humor, etc.)?",
            "What three important things have you learned from previous relationships?",
            "What five traits do you value most in potential partners?",
            "How do you use your personal strengths and abilities at work?",
            "How do your co-workers and supervisors recognize your strengths?",
            "How does work fulfill you? Does it leave you wanting more?",
            "What part of your workday do you most enjoy?",
            "What about your work feels real, necessary, or important to you?",
            "Do you see yourself in the same job in 10 years?",
            "What are your career ambitions?",
            "What values do you consider most important in life (honesty, justice, altruism, loyalty, etc.)? How do your actions align with those values?",
            "What three changes can you make to live according to your personal values?",
            "Describe yourself using the first 10 words that come to mind. Then, list 10 words that you’d like to use to describe yourself. List a few ways to transform those descriptions into reality.",
            "What do you appreciate most about your personality? What aspects do you find harder to accept?", 
            "Describe your favorite thing to do when feeling low.",
            "What three ordinary things bring you the most joy?",
            "List three strategies that help you stay present in your daily routines. Then, list three strategies to help boost mindfulness in your life.",
            "How do you prioritize self-care?",
            "Describe two or three things you do to relax.",
            "What aspects of your life are you most grateful for?"]

#Signup and login function
def login():
    while True:
        #menu
        print("\n Welcome")
        print("1. Login")
        print("2. Sign-Up")
        choice = input("Enter your choice: ")

        #if-else function 
        if choice == "1":
            attempts = 3 
            while attempts > 0:
                username = input("Enter Username: ")
                password = getpass("Enter Password: ")
                #username and password compared to file
                try:
                    with open("users.txt", "r") as f:
                        users = f.readlines()
                        for user in users:
                            stored_username, stored_password = user.strip().split(":")
                            if username == stored_username and password == stored_password:
                                print("Login Successful!\n")
                                return True
                except FileNotFoundError:
                    print("User file not found.")
                    return False

                attempts -= 1
                print(f"Incorrect username or password. {attempts} attempts left.\n")

            print("Too many failed attempts. Access denied.\n")
            return False
        #sign up to store username and password
        elif choice == "2":
            print("\n Register New User")
            username = input("Choose a username: ")
            password = input("Choose a password: ")

            with open("users.txt", "a") as f:
                f.write(f"{username}:{password}\n")

            print("Registration successful. Please log in.\n")

        else:
            print("Invalid choice. Please try again.")

def export():
    print("Would you like to export as 1. txt or 2. pdf")
    choice = input("txt or pdf: ")
    if choice == "1":
        try:
            with open("journal.txt", "r") as f:
                content = f.read()
            with open("exported_journal.txt", "w") as export_file:
                export_file.write(content)
            print("Journal exported as 'exported_journal.txt'")
        except FileNotFoundError:
            print("No entries to export.")
    elif choice == 2: 
        try:
            with open("journal.txt", "r") as f:
                content = f.readlines()

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            for line in content:
                pdf.cell(200, 10, txt=line.strip(), ln=True)

            pdf.output("exported_journal.pdf")
            print("Journal exported as 'exported_journal.pdf'")
        except FileNotFoundError:
            print("No entries to export.")

#menu function 
def menu():
    while True:
        print("\nMental Health Journal ")
        print("1. New Journal Entry")
        print("2. View Previous Entries")
        print("3. Search for Entry")
        print("4. Export Entries")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1": 
            daily_entry()
        elif choice == "2":
            try:
                with open("journal.txt", "r") as f:
                    entries = f.read().strip().split("\n\n")
                    print("\n--- Previous Entries ---")
                    for i, entry in enumerate(entries, 1):
                        print(f"\nEntry {i}:\n{entry}")
            except FileNotFoundError:
                print("No entries found yet.")
        elif choice == "3":
            search = input("Search by date: ")
            try:
                with open("journal.txt", "r") as f:
                    entries = f.read().strip().split("\n\n")
                    found = False
                    for entry in entries:
                        if f"Date: {search}" in entry:
                            print("\n--- Matching Entry Found ---")
                            print(entry)
                            found = True
                        if not found:
                            print("No entry found for that date.")
            except FileNotFoundError:
                print("User file not found.")
                    
        elif choice == "4":
            export()
        elif choice == "5":
            print("👋 Take care. See you soon!")
            break
        else:
            print("Invalid choice. Please try again.\n")

#entry function
def daily_entry(): 
    print("\nWelcome Back!")

    #random prompt 
    prompt = random.choice(prompts)
    print(f"Reflection Prompt: {prompt}")

    mood = int(input("How would you rate your mood today 1-10: "))
    entry = input("How are we feeling today? ")
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M")

    with open("journal.txt", "a") as f:
        f.write(f"Mood: {mood}\n")
        f.write(f"Date: {timestamp}\n")
        f.write(f"Entry: {entry}\n")
        f.write("-" * 40 + "\n\n")

    print("\nEntry saved successfully!")
    print(f"Date: {timestamp}")
    if mood <=3:
        print("I'm so sorry you're having a rough day. But I know how strong you are, you can get through this.")
    elif mood>3 and mood<= 7:
        print("I'm here for you!")
    elif mood >=8:
        print("Yay! I'm glad you're having a good one.")
    print(f"Entry: {entry}\n")

# Start the app with login
if login():
    menu()
else:
    print("🔒 Access denied.")

