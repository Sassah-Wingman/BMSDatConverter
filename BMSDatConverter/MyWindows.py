import PySimpleGUI as sg
import os
import subprocess
from pathlib import Path
import MyFunctions
from BMSDatConverter import __version__

#generic prompt window
def prompt_option_window(option):
    print("** MYWIN/PROM - prompt window summoned.")
    sg.popup(f"Please, select a {option}" , font = "Arial, 14", text_color = ("Dark Red"), no_titlebar = True, modal = True, keep_on_top=True)

#show readme file from original BMS folder
def readme_window():
    readme_tooltips = ["Close readme window."]
    layout = [[sg.Button("CLOSE", key = "-close-", tooltip = readme_tooltips[0])], 
              [sg.Multiline(default_text = MyFunctions.get_readme_text(), 
                            selected_background_color = "yellow",  
                            selected_text_color = "Dark Blue", 
                            font = "Arial, 12", 
                            disabled=True, 
                            size = (900 , 700))],]
     
    readme_window = sg.Window("Text from README file.", layout, finalize = True, size = (1000 , 800))

    while True:
            event, values = readme_window.read()
            print("** MYWIN/READ - events: ", event)
            
            if event in (sg.WIN_CLOSED, "-close-"):
                print("** MYWIN/READ - readme window closed.")
                break
                   
    readme_window.close()
    return readme_window

#convert to proto window
def convert_window():
    convert_tooltips = ["List of installed files.", 
                        "File content.", 
                        "Convert from dat to proto.", 
                        "Not implemented.", 
                        "Delete the selected file.", 
                        "Close this window.", 
                        "Show dat files only.",
                        "Show proto files only.",
                        "Show dat and proto files."]
    
    left_col = sg.Column([[sg.Text("List of Files:")],
                          [sg.Listbox(values = MyFunctions.extension_dat(sg.user_settings_get_entry("-setdata-")),
                                      enable_events = True, 
                                      size = (10,19),
                                      key="-FILE_LIST-",
                                      disabled = False,
                                      expand_x = True, 
                                      expand_y = True,
                                      tooltip = convert_tooltips[0],
                                      select_mode = sg.LISTBOX_SELECT_MODE_SINGLE)],], 
                           element_justification = "Left", expand_x = True, expand_y = False, vertical_alignment = "top")

    right_col = sg.Column([[sg.Text(" ", key = "-TOUT-")],
                          [sg.Multiline(size  =(30,20),
                                        background_color = "light gray",
                                        key = "-TEXT-", 
                                        expand_x = True, 
                                        expand_y = False, 
                                        disabled = True,
                                        tooltip = convert_tooltips[1],
                                        do_not_clear = False)],], 
                           element_justification = "Left", expand_x = True, expand_y=False, vertical_alignment = "top")
    
    buttons_line = [[sg.Text(" ")],
                    [sg.HorizontalSeparator()],
                    [sg.Text(" ")],
                    [sg.Push(), sg.Button(button_text = "Convert to proto", 
                                          key = "-TOPROTO-",
                                          disabled = True, 
                                          size = (16, 1), 
                                          font = "_ 12", 
                                          tooltip = convert_tooltips[2]),
                     sg.Button(button_text = "Convert to .dat", 
                               key = "-TODAT-", 
                               disabled = True, 
                               size = (16, 1), 
                               font = "_ 12", 
                               tooltip = convert_tooltips[3]),
                     sg.Button(button_text = "Delete File", 
                               key = "-DELETE-",
                               disabled = True,
                               button_color = "red",  
                               size = (16, 1), 
                               font = "_ 12", 
                               tooltip = convert_tooltips[4]),
                     sg.Button(button_text = "Close", 
                               key = "-CLOSE-", 
                               size = (16, 1), 
                               font = "_ 12",  
                               tooltip = convert_tooltips[5]), 
                     sg.Push(),],
                    [sg.Push(), sg.Text("Choose the type of file to be displayed.", text_color = "#ffffff", font = "_ 14",), sg.Push()],
                    [sg.Push(), sg.Radio("Show .dat Only", "RADIO1", enable_events = True, circle_color = "#ffffff", default =  True, key = "-DAT-", tooltip = convert_tooltips[6]),
                     sg.Radio("Show .txtpb Only", "RADIO1", enable_events = True, circle_color = "#ffffff", default = False, key = "-PRO-", tooltip = convert_tooltips[7]), 
                     sg.Radio("Show both Files", "RADIO1", enable_events = True, circle_color = "#ffffff", default =  False, key = "-ALL-", tooltip = convert_tooltips[8]), sg.Push()],]

    layout = [[left_col, right_col], [buttons_line]]

    convert_window = sg.Window("Select a File", layout, return_keyboard_events = False, finalize=True, resizable=True, keep_on_top = True, size = (800, 700))
    
    while True:
        event, values = convert_window.read()
        print("** MYWIN/CONV events: ", event)
        print(">> MYWIN/CONV List of Files: ", values["-FILE_LIST-"])
        print(">> MYWIN/CONV proto check: ", values["-PRO-"])
        print(">> MYWIN/CONV dat check: ", values["-DAT-"])
        print(">> MYWIN/CONV all check: ", values["-ALL-"])
        convert_window["-FILE_LIST-"].update(MyFunctions.extension_to_be_displayed(sg.user_settings_get_entry("-setdata-"), values["-PRO-"], values["-DAT-"], values["-ALL-"]))
        convert_window["-TEXT-"].update(" ")
        convert_window["-TOUT-"].update(" ")
        convert_window["-DELETE-"].update(disabled = True)
        convert_window["-TOPROTO-"].update(disabled = True)
        
        #close convert window
        if event in (sg.WIN_CLOSED, "-CLOSE-"):
            print("** MYWIN/CONV - convert window closed.")
            break
        
        #show files and contents for selection
        if event == "-FILE_LIST-" and len(values["-FILE_LIST-"]) > 0:
            #display a list of installed dat/proto files in the folder (if not empty)
            MyFunctions.get_file_contents(sg.user_settings_get_entry("-setdata-"), values["-FILE_LIST-"])
            #display the name of the file above the multiline
            convert_window["-TOUT-"].update(os.path.join(MyFunctions.get_folder(sg.user_settings_get_entry("-setdata-")), MyFunctions.get_file_selection(values["-FILE_LIST-"])))
            #display multiline with content from selected text file
            convert_window["-TEXT-"].update(MyFunctions.get_file_contents(sg.user_settings_get_entry("-setdata-"), values["-FILE_LIST-"]))
            selected_folder = MyFunctions.get_folder(sg.user_settings_get_entry("-setdata-"))
            selected_file = MyFunctions.get_file_selection(values["-FILE_LIST-"])
            convert_window["-DELETE-"].update(disabled = False)
            convert_window["-TOPROTO-"].update(disabled = False)
            print(">> MYWIN/CONV list - folder:", selected_folder)
            print(">> MYWIN/CONV list - file:", selected_file)

        #delete selected file            
        if event in ("-DELETE-"):
            if selected_file == []:
                prompt_option_window("file!")
            else:
                print(">> MYWIN/CONV delete - folder:", selected_folder)
                print(">> MYWIN/CONV delete - file:", selected_file)
                if sg.popup_yes_no("Once deleted, the file can't be restored! Continue?", 
                                    text_color = ("red"), 
                                    no_titlebar = True, 
                                    modal = True, 
                                    keep_on_top = True) == "Yes":
                    os.remove(os.path.join(selected_folder, selected_file))
                    convert_window["-FILE_LIST-"].update(MyFunctions.extension_to_be_displayed(sg.user_settings_get_entry("-setdata-"), values["-PRO-"], values ["-DAT-"], values["-ALL-"]))
                    convert_window["-TOUT-"].update(" ")
                    convert_window["-TEXT-"].update(" ")
                    convert_window["-DELETE-"].update(disabled = True)
                    convert_window["-TOPROTO-"].update(disabled = True)

        #Convert .dat to proto
        if event in ("-TOPROTO-"):
            if selected_file == []:
                prompt_option_window("file!")
            else:
                #get tool path string and add converter exe line
                tool_path = sg.user_settings_get_entry("-settool-") + "\ConvertAirframeData"
                print(">> MYWIN/CONV - proto: tool path: ", tool_path)
                #get acdata path and step one folder up (sim folder)
                full_path = sg.user_settings_get_entry("-setdata-")
                data_path = str(Path(full_path).parents[0]) 
                print(">> MYWIN/CONV - proto: data path: ", data_path)
                #get use config path and add -a and the seleceted file
                config_path = sg.user_settings_get_entry("-setconfig-") + " -a " + selected_file
                print(">> MYWIN/CONV - proto: config path: ", config_path)
                #concatenate all in a string with full path to be used by ConvertAirframeData.exe
                converter_run = [tool_path,"-d", data_path,"-c", config_path]
                print (">> MYWIN/CONV - proto: run line: ", converter_run)
                
                #check if the proto file already exists
                if MyFunctions.verify_proto(selected_folder, selected_file) == True:
                    if sg.popup_yes_no("The file exists and will be overwritten! A backup file will be created. Continue?", 
                                        text_color = ("#ffffff"), 
                                        no_titlebar = True, 
                                        modal = True, 
                                        keep_on_top = True) == "Yes":
                                        MyFunctions.create_backup(selected_file)
                                        subprocess.run(converter_run)
                                        print(">> MYWIN/CONV - Convertion completed: ", selected_file)
                                        sg.popup_auto_close("Convertion Completed!",
                                                        auto_close = True,
                                                        auto_close_duration = 5,
                                                        text_color = ("#ffffff"), 
                                                        no_titlebar = True, 
                                                        modal = True, 
                                                        keep_on_top = True)
                else:
                     if sg.popup_yes_no("A new proto file will be created. Continue?", 
                                        text_color = ("#ffffff"), 
                                        no_titlebar = True, 
                                        modal = True, 
                                        keep_on_top = True) == "Yes":
                                        MyFunctions.create_backup(selected_file)
                                        subprocess.run(converter_run)
                                        print(">> MYWIN/CONV - Convertion completed: ", selected_file)
                                        sg.popup_auto_close("Convertion Completed!",
                                                        auto_close = True,
                                                        auto_close_duration = 5,
                                                        text_color = ("#ffffff"), 
                                                        no_titlebar = True, 
                                                        modal = True, 
                                                        keep_on_top = True)

        #Convert proto to .dat
        if event in ("-TODAT-"):
            pass
                    
    convert_window.close()
    return convert_window

# make setting window
def setting_window():
    setting_tooltips = ["List of installed BMS versions.", 
                        "Acdata folder location.", 
                        "Config folder location.", 
                        "Tool Converter location.", 
                        "Disable/Enable Debug Window.",
                        "Close Settings window."]
    installed_bms = MyFunctions.get_list_of_BMS()
    
    layout = [[sg.Push(),sg.Text("SETTINGS", text_color = "#ffffff", font = "_ 16"), sg.Push()],
                 [sg.Text("Select Falcon BMS version: ")],
                 [sg.Combo(values = installed_bms,
                           setting = sg.user_settings_get_entry(key = "-setbms-"),
                           size = (30,1), 
                           enable_events=True,
                           readonly = True,
                           tooltip = setting_tooltips[0],
                           key = "-BMS-"), sg.Text(" ", key = "-bmsver-")],
                 [sg.Text(" ")],
                 [sg.HorizontalSeparator()],
                 [sg.Text("Falcon BMS Acdata path: ")],
                 [sg.Text(text = sg.user_settings_get_entry("-setdata-"), 
                          text_color = "#ffffff", 
                          tooltip = setting_tooltips[1], 
                          key = "-data-"), sg.Text(" ", text_color = "#64778d", key = "-D-")],
                 [sg.Text("Falcon BMS Config path: ")],
                 [sg.Text(text = sg.user_settings_get_entry("-setconfig-"), 
                          text_color = "#ffffff", 
                          tooltip = setting_tooltips[2], 
                          key = "-config-"), sg.Text(" ", text_color = "#64778d", key = "-C-")],
                 [sg.Text("Falcon BMS Converter path: ")],
                 [sg.Text(text = sg.user_settings_get_entry("-settool-"), 
                          text_color = "#ffffff", 
                          tooltip = setting_tooltips[3], 
                          key = "-tool-"), sg.Text(" ", text_color = "#64778d", key = "-T-")],
                 [sg.Text(" ")],
                 [sg.HorizontalSeparator()],
                 [sg.Text("Debug Window: "), 
                  sg.Checkbox(" ",
                              default = False,
                               enable_events = True, 
                               key = "-DEBUG-", 
                               checkbox_color = "#ffffff", 
                               tooltip = setting_tooltips[4])], 
                 [sg.HorizontalSeparator()],
                 [sg.Push(),sg.Button(button_text = "CLOSE", key = "-CLOSE-", size = (12, 1), font = "_ 10", tooltip = setting_tooltips[5])],
                 [sg.StatusBar("BMS Script Generator version  " + __version__, text_color = "#ffffff")],]
    
    setting_window = sg.Window("BMS proto Converter v1.0 - Settings", 
                               layout, 
                               return_keyboard_events = False, 
                               finalize=True, 
                               resizable=True, 
                               keep_on_top = True, 
                               modal = True, 
                               size = (700, 500))

    #show text after verifing if folders and files do exist
    setting_window["-D-"].update(MyFunctions.check_folders(os.path.exists(sg.user_settings_get_entry("-setdata-")),"Acdata"))
    setting_window["-C-"].update(MyFunctions.check_folders(os.path.exists(sg.user_settings_get_entry("-setconfig-")),"Config"))
    setting_window["-T-"].update(MyFunctions.check_folders(os.path.exists(sg.user_settings_get_entry("-settool-")),"Tools"))
    MyFunctions.check_folders(os.path.exists(sg.user_settings_get_entry("-settool-") + "\ConvertAirframeData.exe"),"Converter")   
             
    while True:
        event, values = setting_window.read()
        print("** MYWIN/SETT events: ", event)
                
        if event in (sg.WIN_CLOSED, "-CLOSE-"):
            print("** MYWIN/SETT - closed")
            break
        
        if event == "-BMS-":
            #Choose BMS version and get path
            sg.user_settings_set_entry("-setbms-", values["-BMS-"])
            print(">> MYWIN/SETT - bmd version: ", values["-BMS-"])
            setting_window["-bmsver-"].update(values["-BMS-"])
            
            #Add Acdata folder to BMS path
            data_path = values["-BMS-"] + "\\Data\Sim\Acdata"
            check = os.path.exists(data_path)
            sg.user_settings_set_entry("-setdata-", data_path)
            print(">> MYWIN/SETT - data folder: ", data_path)
            setting_window["-data-"].update(data_path)
            setting_window["-D-"].update(MyFunctions.check_folders(os.path.exists(sg.user_settings_get_entry("-setdata-")),"Acdata"))
            
            #Add Config folder to BMS path
            config_path = values["-BMS-"] + "\\User\Config"
            sg.user_settings_set_entry("-setconfig-", config_path)
            print(">> MYWIN/SETT - config folder: ", config_path)
            setting_window["-config-"].update(config_path)
            setting_window["-C-"].update(MyFunctions.check_folders(os.path.exists(sg.user_settings_get_entry("-setconfig-")),"Config"))
            
            #Add Converter folder to BMS path
            tool_path = values["-BMS-"] + "\\Tools\ProtoConverters"
            sg.user_settings_set_entry("-settool-", tool_path)
            print(">> MYWIN/SETT - tool folder: ", tool_path)
            setting_window["-tool-"].update(tool_path)
            setting_window["-T-"].update(MyFunctions.check_folders(os.path.exists(sg.user_settings_get_entry("-settool-")),"Tools"))
        
        #Enable/disable debug window
        if event == "-DEBUG-":
            print(">> MYWIN/SETT - debug: ", values["-DEBUG-"])
            if values["-DEBUG-"] == True:
                setting_window["-DEBUG-"].update(text = "Enabled!")
                sg.Print("Symbol MODULE/SECTION - value: ", size = (150, 50), do_not_reroute_stdout = False)
            else:
                setting_window["-DEBUG-"].update(text = " ")
                sg.easy_print_close()
                   
    setting_window.close()
    return setting_window

# make start window for user
def open_window():
    open_tooltips = ["Convert dat to proto.", 
                     "Not implemented.", 
                     "Exit application.", 
                     "Show configuration options.", 
                     "Show original BMS README file."]
    
    image = sg.Image("Open_Image.png", subsample = 0)
       
    title_top = [[sg.Text("Welcome to BMS proto Converter.", font = "_ 22")],]
   
    left_col = sg.Column([[sg.Text(" ", text_color = "#ffffff", background_color = "#64778d")],
                          [sg.Button(button_text = " ", 
                                     button_color= "#64778d", 
                                     size = (16, 3), 
                                     enable_events = False, 
                                     border_width = 0,
                                     disabled = True)],
                          [sg.Button(button_text = "Convert File", 
                                     key = "-CONVERT-", 
                                     size = (16, 2), 
                                     font = "_ 14",
                                     tooltip = open_tooltips[0])],
                          [sg.Text(" ", background_color = "#64778d")],
                          [sg.Button(button_text = "to be implemented",
                                     disabled = True,
                                     key = "-TODO-", 
                                     size = (16, 2), 
                                     font = "_ 14",
                                     tooltip = open_tooltips[1])],
                          [sg.Text(" ", background_color = "#64778d")],
                          [sg.Button(button_text = "EXIT", 
                                     key = "-EXIT-", 
                                     size = (16, 2), 
                                     font = "_ 14",
                                     tooltip = open_tooltips[2])],
                          [sg.Button(button_text = " ", 
                                     button_color= "#64778d", 
                                     size = (24, 6), 
                                     enable_events = False, 
                                     border_width = 0, 
                                     disabled = True)],
                          [sg.Button(button_text = " ", 
                                     button_color= "#64778d", 
                                     size = (24, 2), 
                                     enable_events = False, 
                                     border_width = 0, 
                                     disabled = True)],
                          [sg.Button(button_text = "More Settings", 
                                     key = "-SET-", 
                                     size = (12, 4), 
                                     font = "_ 14",
                                     tooltip = open_tooltips[3])],
                          [sg.Text(" ", background_color = "#64778d")],           
                          [sg.Button(button_text = "Original Readme", 
                                     key = "-READ-", 
                                     size = (16, 2), 
                                     font = "_ 10",
                                     tooltip = open_tooltips[4])],
                          [sg.Button(button_text = " ", 
                                     button_color= "#64778d", 
                                     size = (24, 2), 
                                     enable_events = False, 
                                     border_width = 0, 
                                     disabled = True)],],
                         background_color = "#64778d", element_justification = "center" ,vertical_alignment = "top")
                          
    right_col = sg.Column([[sg.Graph((1279, 721), (0,0), (1291, 727), background_color='white', key = "-graph-")],
                           [sg.Text(" ")],
                           [sg.Text("Data Files (.dat) Location: ", 
                                    font = "_ 14"), 
                                    sg.Text(sg.user_settings_get_entry("-setdata-"),
                                    font = "_ 14", 
                                    text_color = "#ffffff", 
                                    key = "-data-")],
                           [sg.Text("Converter Tool Location: ", 
                                    font = "_ 14"), 
                                    sg.Text(sg.user_settings_get_entry("-settool-"),
                                    text_color = "#ffffff", 
                                    key = "-tool-")],],
                           vertical_alignment = "top") 
      

    layout = [[title_top], [left_col, right_col]]
                  
    open_window = sg.Window("BMS proto Converter.", layout, return_keyboard_events = False, finalize=True, resizable=True, size = (1600, 900))
    
    #update widgets over image
    open_window["-graph-"].draw_image(filename = "Open_Image.png", location = (0, 727))
    open_window["-graph-"].draw_rectangle((200,50), (1000, 200), fill_color = "#d4d7dd", line_color = "#B9BBBE")
    open_window["-graph-"].draw_text("Falcon BMS versions Detected:", (600, 180), font = "_ 12", color = "#000000")
    
    #update wigets with list of installed versions of BMS
    axis_x = 600
    axis_y = 140
    for path_ in MyFunctions.get_installed_BMS_path().values():
        print(">> MYWIN/OPEN - BMS path: ", path_)
        open_window["-graph-"].draw_text(text = path_, location = (axis_x, axis_y), font = "_ 16", color = "#64778d")
        axis_y = axis_y - 30
    
    while True:
        event, values = open_window.read()
        print("** MYWIN/OPEN - events: ", event)
        
        if event in (sg.WIN_CLOSED, "-EXIT-"):
            print("** MYWIN/OPEN - closed")
            break
        
        if event == "-CONVERT-":
            convert_window()
        
        if event == "-TODO-":
            pass

        if event == "-SET-":
            setting_window()
            open_window["-tool-"].update(sg.user_settings_get_entry("-settool-")) 
            open_window["-data-"].update(sg.user_settings_get_entry("-setdata-"))
            
        if event == "-READ-":
            readme_window()
         
    open_window.close()  
    return open_window

