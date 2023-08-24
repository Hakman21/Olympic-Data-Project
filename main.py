try:
    import pandas as pd, keyword, os, random, datetime, colorama, time, json
    from colorama import Fore, Style
except ImportError:
    with open("log.txt", "a") as log_file:
        log_file.write("ERROR IMPORTING MODULES" + '\n')
    print("An Error Occured, Are You Sure You Have The Required Modules Installed? Try Running Setup.bat")
    print("Required Modules: pandas, os, colorama, datetime, random, time")
    quit = input("\n Press Any Button To Quit.")
    exit()

def quit(yeslist, nolist, now):
    loop = True
    while loop:
        selection = input("Are You Sure You Want To Quit? ")
        if selection.lower() in yeslist:
            loop = False
            print(f"{Fore.RED}[{now.strftime('%H:%M:%S')}] CLOSING PROGRAM{Style.RESET_ALL}")
            logs(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] PROGRAM TERMINATED")
            exit()
        elif selection.lower() in nolist:
            loop = False
            menu()
        else:
            print("Invalid Input, Please Try Again")

def error():
    quit = input("\n Press Any Button To Quit.")
    exit()

def logs(command):
    with open("log.txt", "a") as log_file:
        log_file.write(command + '\n')

def view_logs():
    with open("log.txt", "r") as log_file:
        for line in log_file:
            print(line.strip())
    
def load():
    df = pd.read_csv("temp.csv")
    return df

def configure(now):
    if not os.path.exists("config.json"):
        config = {"SAVE_MISSING_DATA": "TRUE", "DISPLAY_AFTER_FILTER": "TRUE"}
        with open("config.json", "w") as f:
            json.dump(config, f)
        save_missing_data_option = "yes"
        display_after_filter_option = "yes"
        logs(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] config.json DOES NOT EXIST. CREATING NEW CONFIGURATION FILE.")
        logs(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] FILE CREATED: config.json")
    else:
        with open ("config.json", "r") as f:
            config = json.load(f)

        if config["SAVE_MISSING_DATA"] == "TRUE":
            save_missing_data_option = "yes"
        elif config["SAVE_MISSING_DATA"] == "FALSE":
            save_missing_data_option = "no"

        if config["DISPLAY_AFTER_FILTER"] == "TRUE":
            display_after_filter_option = "yes"
        elif config["DISPLAY_AFTER_FILTER"] == "FALSE":
            display_after_filter_option = "no"
        logs(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] CONFIG LOADED SUCCESSFULLY")
    return save_missing_data_option, display_after_filter_option

def edit_display_after_filter_option(yeslist, nolist, display_after_filter_option):
        
    loop = True
    while loop:
        if display_after_filter_option == "yes":
            print(f"CURRENTLY: ENABLED")
        else:
            print(f"CURRENTLY: DISABLED")
    
        selection = input("Are You Sure You Want To Toggle Display After Filter Option?")
        if selection.lower() in yeslist:
            with open("config.json", "r") as f:
                config = json.load(f)
            if display_after_filter_option == "yes":
                config["DISPLAY_AFTER_FILTER"] = "FALSE"
                with open('config.json', 'w') as f:
                    json.dump(config, f)
            else:
                config["DISPLAY_AFTER_FILTER"] = "TRUE"
                with open('config.json', 'w') as f:
                    json.dump(config, f)
            loop = False
            return display_after_filter_option
        elif selection.lower() in nolist:
            return
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Invalid Input. Please Try Again")

def edit_save_missing_data_option(yeslist, nolist, save_missing_data_option):
    
    loop = True
    while loop:
        if save_missing_data_option == "yes":
            print(f"CURRENTLY: ENABLED")
        else:
            print(f"CURRENTLY: DISABLED")
    
        selection = input("Are You Sure You Want To Toggle Save To Seperate File Option?")
        if selection.lower() in yeslist:
            with open("config.json", "r") as f:
                config = json.load(f)
            if save_missing_data_option == "yes":
                config["SAVE_MISSING_DATA"] = "FALSE"
                with open('config.json', 'w') as f:
                    json.dump(config, f)
            else:
                config["SAVE_MISSING_DATA"] = "TRUE"
                with open('config.json', 'w') as f:
                    json.dump(config, f)
            loop = False
        elif selection.lower() in nolist:
            return
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Invalid Input. Please Try Again")

def save(df):
    df.to_csv("temp1.csv", index=False)
    os.remove("temp.csv")
    os.rename("temp1.csv", "temp.csv")

def finish(yeslist, nolist, now):
    try:
        os.rename("temp.csv", "cleaned_olympic_dataset.csv")
        exit()
    except:
        print(f"Failed To Save. Does cleaned_olympic_data.csv Already Exist?")
        print(f"Cleaned Dataset Will Now Be Saved As temp.csv")
        time.sleep(3)
        exit()

def filter_missing(olddf, yeslist, nolist, now, save_missing_data_option, display_after_filter_option):
    columns = ["Name", "Sex", "Age", "Height", "Weight", "Team", "NOC", "Games", "Season", "City", "Sport", "Event"]
    rows_missing = olddf[olddf[columns].isnull().any(axis=1)]
    if save_missing_data_option == "yes":
        rows_missing.to_csv("rows_with_missing_data.csv", index=False)
        logs(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] SAVED ROWS WITH MISSING DATA TO FILE")
    
    cleaned_df = olddf.dropna(subset=columns, how='any') 
    save(cleaned_df)
    if display_after_filter_option == "yes":
        print(cleaned_df)
    return

def gender(yeslist, nolist, now, display_after_filter_option):
    df = load()
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""{Fore.CYAN}
OPTIONS:
1) Filter By Gender
2) Return To Previous Menu
{Style.RESET_ALL}""")
    selection = input("Enter an option: ")
    if selection == "1":
        loop = True
        while loop:
            gender_option = input("Enter Gender (Male/Female): ")
            if gender_option.lower() in ["male", "m", "man", "boy", "guy", "gentleman", "dude", "fellow", "mr.", "masculine"]:
                filtered_df = df[df["Sex"].str.lower() == "m"]  # Change "M" to "m"
                loop = False
            elif gender_option.lower() in ["female", "f", "woman", "lady", "girl", "feminine", "ms.", "miss", "madam"]:
                filtered_df = df[df["Sex"].str.lower() == "f"]  # Change "F" to "f"
                loop = False
            else:
                print("Invalid Input. Please Try Again")
        save(filtered_df)
        print("Filtered dataset saved as temp.csv")
        logs(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] FILTERED BY GENDER: {gender_option}")
        if display_after_filter_option == "yes":
            print(filtered_df)
        return 
    elif selection == "2":
        return 

def age(yeslist, nolist, now, display_after_filter_option):
    df = load()
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""{Fore.CYAN}
OPTIONS:
1) Filter By Age Range
2) Return To Previous Menu
{Style.RESET_ALL}""")
    selection = input("Enter an option: ")
    if selection == "1":
        try:
            bound1 = int(input("Enter Lower Bound For Age: "))
            bound2 = int(input("Enter Upper Bound For Age: "))
            if bound1 > bound2:
                print("Invalid input. Lower bound should be less than or equal to upper bound.")
            else:
                filtered_df = df[(df["Age"] >= bound1) & (df["Age"] <= bound2)]
                save(filtered_df)
                print("Filtered dataset saved as temp.csv")
                logs(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] FILTERED BY AGE RANGE: {bound1} - {bound2}")
                if display_after_filter_option == "yes":
                    print(filtered_df)
            return
        except ValueError:
            print("Invalid input. Please enter valid integer age values.")
    elif selection == "2":
        return
    
def height(yeslist, nolist, now, display_after_filter_option):
    df = load()
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""{Fore.CYAN}
OPTIONS:
1) Filter By Height
2) Return To Previous Menu
{Style.RESET_ALL}""")
    selection = input("Enter an option: ")
    if selection == "1":
        try:
            bound1 = int(input("Enter Lower Bound For Height: "))
            bound2 = int(input("Enter Upper Bound For Height: "))
            if bound1 > bound2:
                print("Invalid input. Lower bound should be less than or equal to upper bound.")
            else:
                filtered_df = df[(df["Height"] >= bound1) & (df["Height"] <= bound2)]
                save(filtered_df)
                print("Filtered dataset saved as temp.csv")
                logs(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] FILTERED BY HEIGHT RANGE: {bound1} - {bound2}")
                if display_after_filter_option == "yes":
                    print(filtered_df)
                df = filtered_df
            return 
        except ValueError:
            print("Invalid input. Please enter valid integer height values.")
    elif selection == "2":
        return
    
def country(yeslist, nolist, now, display_after_filter_option):
    df = load()
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""{Fore.CYAN}
OPTIONS:
1) Filter By Country / NOC
2) Return To Previous Menu
{Style.RESET_ALL}""")
    selection = input("Enter an option: ")
    if selection == "1":
        country_name = input("Enter Country / NOC: ")
        filtered_df = df[df["Team"].str.lower() == country_name.lower()]
        save(filtered_df)
        print("Filtered dataset saved as temp.csv")
        logs(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] FILTERED BY COUNTRY / NOC: {country_name}")
        if display_after_filter_option == "yes":
            print(filtered_df)
        return 
    elif selection == "2":
        return 
    
def year(yeslist, nolist, now, display_after_filter_option):
    df = load()
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""{Fore.CYAN}
OPTIONS:
1) Filter By Year Range
2) Return To Previous Menu
{Style.RESET_ALL}""")
    selection = input("Enter an option: ")
    if selection == "1":
        try:
            bound1 = int(input("Enter Lower Bound For Year: "))
            bound2 = int(input("Enter Upper Bound For Year: "))
            if bound1 > bound2:
                print("Invalid input. Lower bound should be less than or equal to upper bound.")
            else:
                filtered_df = df[(df["Year"] >= bound1) and (df["Year"] <= bound2)]
                save(filtered_df)
                print("Filtered dataset saved as temp.csv")
                logs(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] FILTERED BY Year RANGE: {bound1} - {bound2}")
                if display_after_filter_option == "yes":
                    print(filtered_df)
            return 
        except ValueError:
            print("Invalid input. Please enter valid integer age values.")
    elif selection == "2":
        return
    
def season(yeslist, nolist, now, display_after_filter_option):
    df = load()
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""{Fore.CYAN}
OPTIONS:
1) Filter By Season
2) Return To Previous Menu
{Style.RESET_ALL}""")
    selection = input("Enter an option: ")
    if selection == "1":
        season_name = input("Enter Season (Summer/Winter): ")
        filtered_df = df[df["Season"].str.lower() == season_name.lower()]
        save(filtered_df)
        print("Filtered dataset saved as temp.csv")
        logs(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] FILTERED BY SEASON: {season_name}")
        if display_after_filter_option == "yes":
            print(filtered_df)
        return 
    elif selection == "2":
        return

def sport(yeslist, nolist, now, display_after_filter_option):
    df = load()
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""{Fore.CYAN}
OPTIONS:
1) Filter By Sport
2) Return To Previous Menu
{Style.RESET_ALL}""")
    selection = input("Enter an option: ")
    if selection == "1":
        sport_name = input("Enter Sport: ")
        filtered_df = df[df["Sport"].str.lower() == sport_name.lower()]
        save(filtered_df)
        print("Filtered dataset saved as temp.csv")
        logs(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] FILTERED BY SPORT: {sport_name}")
        if display_after_filter_option == "yes":
            print(filtered_df)
        return 
    elif selection == "2":
        return
    
def medal(yeslist, nolist, now, display_after_filter_option):
    df = load()
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""{Fore.CYAN}    
OPTIONS:
1) Filter By Medal (Gold/Silver/Bronze)
2) Return To Previous Menu
{Style.RESET_ALL}""")
    selection = input("Enter an option: ")
    if selection == "1":
        medal_name = input("Enter Medal (Gold/Silver/Bronze): ")
        filtered_df = df[df["Medal"].str.lower() == medal_name.lower()]
        save(filtered_df)
        print("Filtered dataset saved as temp.csv")
        logs(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] FILTERED BY MEDAL: {medal_name}")
        if display_after_filter_option == "yes":
            print(filtered_df)
        return
    elif selection == "2":
        return

def settings(yeslist, nolist, save_missing_data_option, display_after_filter_option):
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        print(f"""{Fore.CYAN}
OPTIONS:
1) View Logs
2) Save Missing Data To Seperate File
3) Display After Filter
4) Return To Main Menu

{Style.RESET_ALL}""")
        
        selection = input("Enter An Option: ")
        if selection == "1":
            view_logs()
        elif selection == "2":
            edit_save_missing_data_option(yeslist, nolist, save_missing_data_option)          
        elif selection == "3": 
            edit_display_after_filter_option(yeslist, nolist, display_after_filter_option)
        elif selection == "4": 
            return

def menu(yeslist, nolist, now, save_missing_data_option, display_after_filter_option):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""{Fore.MAGENTA}
      /$$$$$$  /$$   /$$     /$$ /$$      /$$ /$$$$$$$  /$$$$$$  /$$$$$$        /$$$$$$$   /$$$$$$  /$$$$$$$$ /$$$$$$         /$$$$$$   /$$$$$$  /$$$$$$$  /$$$$$$$$ /$$$$$$$$ /$$$$$$$ 
     /$$__  $$| $$  |  $$   /$$/| $$$    /$$$| $$__  $$|_  $$_/ /$$__  $$      | $$__  $$ /$$__  $$|__  $$__//$$__  $$       /$$__  $$ /$$__  $$| $$__  $$|__  $$__/| $$_____/| $$__  $$
    | $$  \ $$| $$   \  $$ /$$/ | $$$$  /$$$$| $$  \ $$  | $$  | $$  \__/      | $$  \ $$| $$  \ $$   | $$  | $$  \ $$      | $$  \__/| $$  \ $$| $$  \ $$   | $$   | $$      | $$  \ $$
    | $$  | $$| $$    \  $$$$/  | $$ $$/$$ $$| $$$$$$$/  | $$  | $$            | $$  | $$| $$$$$$$$   | $$  | $$$$$$$$      |  $$$$$$ | $$  | $$| $$$$$$$/   | $$   | $$$$$   | $$$$$$$/
    | $$  | $$| $$     \  $$/   | $$  $$$| $$| $$____/   | $$  | $$            | $$  | $$| $$__  $$   | $$  | $$__  $$       \____  $$| $$  | $$| $$__  $$   | $$   | $$__/   | $$__  $$
    | $$  | $$| $$      | $$    | $$\  $ | $$| $$        | $$  | $$    $$      | $$  | $$| $$  | $$   | $$  | $$  | $$       /$$  \ $$| $$  | $$| $$  \ $$   | $$   | $$      | $$  \ $$
    |  $$$$$$/| $$$$$$$$| $$    | $$ \/  | $$| $$       /$$$$$$|  $$$$$$/      | $$$$$$$/| $$  | $$   | $$  | $$  | $$      |  $$$$$$/|  $$$$$$/| $$  | $$   | $$   | $$$$$$$$| $$  | $$
     \______/ |________/|__/    |__/     |__/|__/      |______/ \______/       |_______/ |__/  |__/   |__/  |__/  |__/       \______/  \______/ |__/  |__/   |__/   |________/|__/  |__/                                                                                                                                                                                                                                                                                                                                  
{Style.RESET_ALL}""")  
    
    while True:
        print(f"""{Fore.CYAN}
OPTIONS:
1) Finish
2) Filter By Gender
3) Filter By Age
4) Filter By Height
5) Filter By Country / NOC
6) Filter By Year
7) Filter By Season
8) Filter By Sport
9) Filter By Medal
10) Settings
11) Quit Program
{Style.RESET_ALL}""")

        selection = input("Enter An Option: ") 
        if selection == "1":
            finish(yeslist, nolist, now)
        elif selection == "2": 
            gender(yeslist, nolist, now, display_after_filter_option)
        elif selection == "3": 
            logs(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] SELECTED OPTION: Filter Out Entries With Missing Data")
            age(yeslist, nolist, now, display_after_filter_option)
        elif selection == "4": 
            height(yeslist, nolist, now, display_after_filter_option)
        elif selection == "5": 
            country(yeslist, nolist, now, display_after_filter_option)
        elif selection == "6": 
            year(yeslist, nolist, now, display_after_filter_option)
        elif selection == "7": 
            season(yeslist, nolist, now, display_after_filter_option)
        elif selection == "8": 
            sport(yeslist, nolist, now, display_after_filter_option)
        elif selection == "9": 
            medal(yeslist, nolist, now, display_after_filter_option)
        elif selection == "10":
            settings(yeslist, nolist, save_missing_data_option, display_after_filter_option)
        elif selection == "11":  
            quit(yeslist, nolist, now)

def start():
    now = datetime.datetime.now()
    print(f"{Fore.GREEN}[{now.strftime('%H:%M:%S')}] STARTING PROGRAM{Style.RESET_ALL}")
    logs(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] PROGRAM STARTED")

    save_missing_data_option, display_after_filter_option = configure(now)
    print(save_missing_data_option)
    print(display_after_filter_option)

    yeslist = ["yes", "y", "affirmative", "certainly", "indeed", "absolutely", "sure", "yeah", "yep", "for sure", "definitely", "agreed", "roger", "okay", "alright", "aye", "positive", "you bet", "no problem", "gladly", "undoubtedly", "without a doubt", "by all means", "of course", "naturally", "exactly", "totally", "unquestionably", "positively", "good", "correct", "true", "yup", "aye aye", "ok", "affirm", "acknowledge", "accept", "grant", "approve", "endorse", "validate"]
    nolist = ["no", "n", "negative", "not at all", "nay", "absolutely not", "certainly not", "definitely not", "by no means", "no way", "never", "not really", "not necessarily", "decline", "deny", "refuse", "reject", "oppose", "veto", "disagree", "disapprove", "contradict", "rebut", "object", "withhold", "nullify", "void", "negate", "null", "void", "dismiss", "discard", "overrule", "invalidate", "quash", "rebuff", "rebuff", "spurn", "repudiate"]

    try:
        original_df = pd.read_csv("dataset_olympics.csv")
        dftemp = original_df.copy(deep=True)
        dftemp.to_csv("temp.csv", index=False)
        olddf = pd.read_csv("temp.csv")
        logs(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] FILE LOADED")
        print(f"{Fore.GREEN}[{now.strftime('%H:%M:%S')}] CLEANING DATA{Style.RESET_ALL}")
        logs(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] CLEANING DATA")
        filter_missing(olddf, yeslist, nolist, now, save_missing_data_option, display_after_filter_option)
        menu(yeslist, nolist, now, save_missing_data_option, display_after_filter_option)
    except LookupError:
        print("Error Loading File, Are You Sure dataset_olympics.csv Exists And Is In The Same Folder As This Program?")
        logs(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] FILE LOADING ERROR")
        error()

if __name__ == "__main__":
    start()
