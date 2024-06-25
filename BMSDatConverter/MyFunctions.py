import PySimpleGUI as sg
import os
import winreg
import sys
import shutil

#verify if the proto file already exists
def verify_proto(_folder, _file):
    _extension = ".dat"
    _proto = _file.replace(_extension,".txtpb")
    exist_file = _folder + "\\" + _proto
    print("=> MYFUN/BACK - source proto: ", _file)
    print("=> MYFUN/BACK - exist proto: ", exist_file)
    print("=> MYFUN/BACK - exist proto: ", os.path.exists(exist_file))
    return (os.path.exists(exist_file))

#create a .dat backup before overwrite it
def create_backup(_file):
    source_file = sg.user_settings_get_entry("-setdata-") + "\\" + _file
    _extension = ".dat"
    _backup = _file.replace(_extension,".bkp")
    target_file = sg.user_settings_get_entry("-setdata-") + "\\" + _backup
    print("=> MYFUN/BACK - source: ", source_file)
    print("=> MYFUN/BACK - backup: ", target_file)
    shutil.copyfile(source_file, target_file)

#check if required folders do exist using bms path settings
def check_folders(_exist, _folder):
    if _exist == False:
        print(">> MYFUN/CHECK - folder:", _folder, " not found!")
        return("Folder not found!")
    else:
        print(">> MYFUN/CHECK -  folder:", _folder, " OK!")
        return("<<< Ok!")

#list of bms versions to be shown in settings_window
def get_list_of_BMS():
     list_of_BMS = []
     for path_ in get_installed_BMS_path().values():
         list_of_BMS.append(path_)
         print("=> MYFUN/USER - list of bms: ", list_of_BMS)
     return list_of_BMS

#Find all BMS installed using winreg
def get_installed_BMS_path():
    BMS_sub_key = "SOFTWARE\WOW6432Node\Benchmark Sims"
    BMS_Sub_key_name = "baseDir"
    list_of_BMS_keys = []
    list_of_BMS_address = []
    try:
        hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, BMS_sub_key, 0, winreg.KEY_READ)
        index = 0
        while True:
            try:
                key_name = winreg.EnumKey(hkey, index)
                sub_key_path = BMS_sub_key + "\\" + key_name
                hsubkey = winreg.OpenKey(hkey, key_name)
                sub_key_value = winreg.QueryValueEx(hsubkey, BMS_Sub_key_name)[0]
                print("=> MYFUN/PATH: ", f"{key_name} : {sub_key_value}")
                list_of_BMS_keys.append(key_name)
                list_of_BMS_address.append(sub_key_value)
                sim_path = sub_key_value + "\Data\Sim"
                print("=> MYFUN/PATH - Sim path: ", sim_path)
                for entry in os.listdir(sim_path):
                    if os.path.isdir(os.path.join(sim_path, entry)):
                        print("=> MYFUN/PATH - Sim folder: ", entry)
                winreg.CloseKey(hsubkey)
                index += 1
            except OSError:
                break
    except FileNotFoundError:
        print("=> MYFUN/PATH - >>>Falcon BMS not found!<<<")
        sg.popup("Falcon BMS not found!", text_color = ("red"))
    finally:
        if hkey:
            winreg.CloseKey(hkey)
    list_of_installed_BMS = dict(zip(list_of_BMS_keys, list_of_BMS_address))
    print("=>MYFUN/PATH: ", list_of_installed_BMS)
    print("=> MYFUN/PATH - regKeys: ", list_of_installed_BMS.keys())
    print("=> MYFUN/PATH - regValues: ", list_of_installed_BMS.values())
    return list_of_installed_BMS

#get original readme file to be displayed
def get_readme_text():
   try:
       with open("README.md") as readme_txt:
           list_readme = readme_txt.read()
           #print("=> MYFUN/USERSET - text: ", list_readme)
   except:
       sg.popup("README.md not found! Program will close!", text_color = ("red"))
       print(">>>> MYFUN - READ: ", "README.md not found!")
       sys.exit(0)
   return list_readme

#get list of all .dat files to be displayed
def extension_dat (_folder):
    list_of_files_in_folder = os.listdir(_folder)
    selected_dat_extension = [f for f in list_of_files_in_folder if os.path.isfile(os.path.join(_folder, f)) and f.lower().endswith((".dat"))]
    return selected_dat_extension

#sort the type of file (dat, proto) extension to be displayed
def extension_to_be_displayed (_folder, _txtpb, _dat, _all):
    list_of_files_in_folder = os.listdir(_folder)
    if _txtpb == True:
        selected_file_extension = [f for f in list_of_files_in_folder if os.path.isfile(os.path.join(_folder, f)) and f.lower().endswith((".txtpb"))]
    elif _dat ==  True:   
        selected_file_extension = [f for f in list_of_files_in_folder if os.path.isfile(os.path.join(_folder, f)) and f.lower().endswith((".dat"))]
    elif _all == True:  
        selected_file_extension = [f for f in list_of_files_in_folder if os.path.isfile(os.path.join(_folder, f)) and f.lower().endswith((".txtpb", ".dat"))]
    else:
        sg.popup("You must select a type of extension!", no_titlebar = True, any_key_closes = True, keep_on_top = True, modal = True)
    return selected_file_extension

#convert folder name from list to string
def get_folder (_folder):
    folder_address = _folder
    print("=> MYFUN/FOLD - fold selected: ", folder_address)
    return folder_address   

#get file selected and convert it from list to string
def get_file_selection (_filelist):
    print("=> MYFUN/FILE - in: ", _filelist)
    file_selection = _filelist [0]
    print("=> MYFUN/FILE - out: ", file_selection)
    return file_selection

#get content inside the file
def get_file_contents (_folder, _filelist):
    with open(os.path.join(get_folder(_folder), get_file_selection(_filelist))) as file_to_read:
        contents_in_file=file_to_read.read()
        #print(">>>> MYFUN/CONT - file contents: ", contents_in_file)
    return contents_in_file

#Not used
# def get_list_of_files (_filelist):
#     file_list = _filelist
#     print("===============================> MYFUN/FILE - file list: ", file_list)
#     return file_list