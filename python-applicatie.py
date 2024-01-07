import json
import requests
from tkinter import *
import datetime

jort_ID = 76561198424424214
camiel_ID = 76561199075949807
abi_ID = 76561199499642445
joeri_ID = 76561198811411788
viggo_ID = 76561198901321655

steam_api_key = "61D1D964724B68FC9F340D584CD500E3"
user_id = "76561198424424214"

def binary_search(lst, target):     #binary search
    sorted_list = my_sort(lst)
    low, high = 0, len(sorted_list) - 1
    while low <= high:
        mid = (low + high) // 2
        mid_word = sorted_list[mid]
        if target == mid_word:
            return mid_word
        elif target < mid_word:
            high = mid - 1
        elif target > mid_word:
            low = mid + 1
    return "No results..."

def my_sort(lst):       #sort function selection sort? (vgm is het bubble sort)
    lst_sorted = lst.copy()
    gewisseld = True
    while gewisseld:
        gewisseld = False
        for i in range(0, len(lst_sorted) - 1):
            if lst_sorted[i] > lst_sorted[i + 1]:
                lst_sorted[i], lst_sorted[i + 1] = lst_sorted[i + 1], lst_sorted[i]
                gewisseld = True
            else:
                continue
    return lst_sorted

def get_json_file(steam_api_link):
    response = requests.get(steam_api_link)
    data = response.json()
    return json.dumps(data, indent=2)

def get_friendlist(steamid):
    return get_json_file(f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={steam_api_key}&steamid={steamid}&relationship=friend")

# print(get_friendlist(user_id))

def get_player_info(steamid):
    return get_json_file(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={steam_api_key}&steamids={steamid}")

def get_personaname(steamid):
    response = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={steam_api_key}&steamids={steamid}")
    data = response.json()
    personaname = data['response']['players'][0]['personaname']
    return personaname

def unix_to_normal(unix_date):
    datetime_object = datetime.datetime.fromtimestamp(unix_date)

    date_format = "%d-%m-%Y %H:%M"
    return datetime_object.strftime(date_format)

def last_logoff_friendlist(steamid):  # get each friend of friendlist with last logoff
    global friendinfo_lst
    friend_info_list = []
    friendinfo_lst = []

    response = requests.get(
        f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={steam_api_key}&steamid={steamid}&relationship=friend")
    data = response.json()
    steamid_list = []
    for friend in data['friendslist']['friends']:
        steamid = friend['steamid']
        steamid_list.append(steamid)
    for steamid in steamid_list:
        response = requests.get(
            f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={steam_api_key}&steamids={steamid}")
        data = response.json()
        personaname = data['response']['players'][0]['personaname']

        if 'lastlogoff' in data['response']['players'][0]:
            lastlogoff = data['response']['players'][0]['lastlogoff']
            lastlogoff = unix_to_normal(lastlogoff)
        else:
            lastlogoff = "N/A"

        if 'loccountrycode' in data['response']['players'][0]:
            countrycode = data['response']['players'][0]['loccountrycode']
        else: countrycode = "N/A"

        if 'personastate' in data['response']['players'][0]:
            personastate = data['response']['players'][0]['personastate']
            if personastate == 0:
                online_status = "Offline"
            elif personastate == 1:
                online_status = "Online"
            elif personastate == 2:
                online_status = "Do Not Disturb"
            elif personastate == 3:
                online_status = "Away"
            elif personastate == 4:
                online_status = "Snooze"
            else:
                online_status = "N/A"
        friend_info_dict = {'personaname': personaname, 'onlinestatus': online_status, 'lastlogoff': lastlogoff}
        friend_info_list.append(friend_info_dict)
        if personastate == 0:
            friendinfo = f"{personaname} - {online_status} - Last online: {lastlogoff}"
        else:
            friendinfo = f"{personaname} - {online_status}"
        friendinfo_lst.append(friendinfo)

    return friendinfo_lst, friend_info_list


def main_gui():
    steamid = steamid_input.get()

    root1.destroy()
    root2 = Tk()
    root2.geometry("1200x600")
    root2.title("Main screen")

    personaname = get_personaname(steamid)

    lbl = Label(master=root2, text=f"Welcome {personaname}")
    lbl.pack()

    lbl2 = Label(master=root2, text=f"friendlist")
    lbl2.pack()
    last_logoff_friendlist(steamid)
    for i, friend in enumerate(friendinfo_lst):
        label = Label(root2, text=friend)
        label.pack()
    root2.mainloop()

def login_gui():
    global root1
    global steamid_input
    root1 = Tk()
    root1.geometry("1200x600")
    root1.title("Login")
    # root.resizable(0,0)
    root1.configure(bg="#1b2838")

    lbl1 = Label(master=root1, text="What is your steam ID?", bg="#66c0f4")
    lbl1.pack(pady=20)

    steamid_input = Entry(master=root1)
    steamid_input.pack()

    confirm_btn = Button(master=root1, text="Confirm", command=main_gui)
    confirm_btn.pack(pady=20)


    root1.mainloop()

login_gui()
