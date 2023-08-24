import plotly.express as px, pandas as pd, os, datetime, colorama
from colorama import Fore, Style


def visualise(filename, selection):
    df = pd.read_csv(filename)
    if selection == "1":
        gender_counts = df["Sex"].value_counts()
        fig = px.bar(gender_counts, x=gender_counts.index, y=gender_counts.values, title="Distribution of Genders")
        fig.show()
    elif selection == "2":
        age_counts = df["Age"].value_counts()
        fig = px.bar(age_counts, x=age_counts.index, y=age_counts.values, title="Distribution of Ages")
        fig.show()
    elif selection == "3":
        height_counts = df["Height"].value_counts()
        fig = px.bar(height_counts, x=height_counts.index, y=height_counts.values, title="Distribution of Heights")
        fig.show()

def scatter(filename):
    df = pd.read_csv(filename)
    fig = px.scatter(df, x="Age", y="Height", color="Sex", title="Age vs. Height of Athletes",
                     labels={"Age": "Age (years)", "Height": "Height (cm)"}, 
                     hover_data=["Name", "Sport", "Medal"])
    fig.show()


def menu(filename):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""{Fore.MAGENTA}
 ██████╗ ██╗  ██╗   ██╗███╗   ███╗██████╗ ██╗ ██████╗    ██████╗  █████╗ ████████╗ █████╗     ██╗   ██╗██╗███████╗██╗   ██╗ █████╗ ██╗     ██╗███████╗███████╗██████╗ 
██╔═══██╗██║  ╚██╗ ██╔╝████╗ ████║██╔══██╗██║██╔════╝    ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗    ██║   ██║██║██╔════╝██║   ██║██╔══██╗██║     ██║██╔════╝██╔════╝██╔══██╗
██║   ██║██║   ╚████╔╝ ██╔████╔██║██████╔╝██║██║         ██║  ██║███████║   ██║   ███████║    ██║   ██║██║███████╗██║   ██║███████║██║     ██║███████╗█████╗  ██████╔╝
██║   ██║██║    ╚██╔╝  ██║╚██╔╝██║██╔═══╝ ██║██║         ██║  ██║██╔══██║   ██║   ██╔══██║    ╚██╗ ██╔╝██║╚════██║██║   ██║██╔══██║██║     ██║╚════██║██╔══╝  ██╔══██╗
╚██████╔╝███████╗██║   ██║ ╚═╝ ██║██║     ██║╚██████╗    ██████╔╝██║  ██║   ██║   ██║  ██║     ╚████╔╝ ██║███████║╚██████╔╝██║  ██║███████╗██║███████║███████╗██║  ██║
 ╚═════╝ ╚══════╝╚═╝   ╚═╝     ╚═╝╚═╝     ╚═╝ ╚═════╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝      ╚═══╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝╚══════╝╚══════╝╚═╝  ╚═╝                                                                                                                                                                                                                                                                                                                                                                                                               
{Style.RESET_ALL}""")  
    
    while True:
        print(f"""{Fore.CYAN}
OPTIONS:
1) Visualise Gender
2) Visualise Age
3) Visualise Height
4) ...
5) ...
6) Quit Program

{Style.RESET_ALL}""")

        selection = input("Enter An Option: ") 
        if selection in ["1", "2", "3"]:
            visualise(filename, selection)
        elif selection == "4": 
            scatter(filename)
        elif selection == "5":
            print("placeholder")
        elif selection == "6":
            exit()
        else:
            print("Invalid Input. Please Try Again")


def start():
    filename = input("Enter Filename")
    menu(filename)

if __name__ == "__main__":
    start()