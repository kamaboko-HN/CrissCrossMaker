from tkinter import filedialog
import tkinter as tk
import datetime as dt

import Variables_List as VL

def CCM_save(select_Notebook, *event):
    for tab_data_list in VL.TabsList:
        if tab_data_list[0] == select_Notebook:
            TAB_DATA = tab_data_list.copy()

    dt_now = dt.datetime.now()
    dt_str = str(dt_now.year) + str(dt_now.month) + str(dt_now.day) + str(dt_now.hour) + str(dt_now.minute)
    tab_name = TAB_DATA[1] + "  " + dt_str
        
    filename = filedialog.asksaveasfilename(defaultextension="txt", filetypes=[('Text', '*.txt')], initialfile=tab_name)

    if (filename != ""):
        #self.savingwindowshow()
        #self.Sapp

        with open(filename, mode="w", encoding="utf-8") as to_save:
            to_save.write("CrissCrossMaker Save Text File" + "\n")
            to_save.write(TAB_DATA[1] + "\n") #project name
            to_save.write(str(TAB_DATA[2]) + "\n") #grid size
            to_save.write("grid_list_data\n")
                
            #grid datas
            for grid_datas in TAB_DATA[3]:
                for grid_data in grid_datas:
                    to_save.write(str(grid_data) + ",")
                to_save.write("\n")

            to_save.write("\nlist_data\n")
            for list_datas in TAB_DATA[7]:
                 to_save.write(list_datas[0] + "," + str(list_datas[1]) + "," + list_datas[2] + "," + str(list_datas[3]) + "," + str(list_datas[4]) + "\n")
        #savingwindowdestroy()

def CCM_load():
    filename = filedialog.askopenfilename(defaultextension="txt", filetypes=[('Text', '*.txt')])
    if (filename != ""):
        with open(filename, mode="r") as load_file:
            loadfiledata_original = load_file.readlines()
        if loadfiledata_original[0] == "CrissCrossMaker Save Text File\n":
            load_file_data = []
            load_grid_list = []
            load_listbox_data_list = []
            listboxword_list = []
            count = 0
            gld = False
            ld = False
            for data in loadfiledata_original:
                data_sd = data.strip("\n")
                print(data_sd)
                if data_sd != "":
                    if (count == 1):
                        load_file_data.append(data_sd)

                    elif (count == 2):
                        load_file_data.append(data_sd)

                    elif data_sd == "grid_list_data":
                        gld = True
                        ld = False
                    elif data_sd == "list_data":
                        ld = True
                        gld = False

                    elif gld == True and ld == False:
                        data_sd_2 = data_sd.split(",")
                        data_sd_2.pop()
                        data_sd = [int(s) for s in data_sd_2]
                        load_grid_list.append(data_sd)

                    elif ld == True and gld == False:
                        data_sd_2 = data_sd.split(",")
                        data_sd_2[1] = int(data_sd_2[1])
                        data_sd_2[3] = int(data_sd_2[3])
                        data_sd_2[4] = int(data_sd_2[4])
                        load_listbox_data_list.append(data_sd_2)


                count += 1

            for data in load_listbox_data_list:
                listboxword_list.append(data)
        
        return_list = [load_file_data[0], int(load_file_data[1]), load_grid_list, load_listbox_data_list, listboxword_list]
        return return_list
