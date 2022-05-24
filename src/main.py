from cgi import test
from cgitb import enable
from copy import deepcopy
from email.mime import image
from ensurepip import version
from faulthandler import disable
from hashlib import new
from operator import index
import os
from posixpath import split
from re import S
import sys
from tabnanny import check
from textwrap import fill
from time import sleep
import tkinter as tk
from tkinter import CENTER, FLAT, LEFT, SOLID, Image, Menu, Variable, ttk
from tkinter.tix import NoteBook
from tkinter import filedialog
from tkinter import messagebox
import glob
from turtle import bgcolor, left, right

from numpy import imag
from natsort import natsorted

import Variables_List as VL

############################## ######################################################################
#   Application Main Frame   # 
############################## ######################################################################

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        #Road Images
        for images in natsorted(glob.glob("img/*.png")):
            VL.word_img_list.append(tk.PhotoImage(file=images))

        master.title("CrissCrossMaker")

        menuBar = tk.Menu()
        self.master.config(menu=menuBar)

        fileMenu = tk.Menu(tearoff=0)
        fileMenu.add_command(label="保存", command=self.savefile)
        fileMenu.add_command(label="開く", command=self.loadfile)
        fileMenu.add_command(label="終了", command=self.onexit)
        
        editMenu = tk.Menu(tearoff=0)
        editMenu.add_command(label="やり直し")
        editMenu.add_command(label="元に戻す")
        editMenu.add_command(label="全黒塗り", command=self.allgridblack)

        tabMenu = tk.Menu(tearoff=0)
        tabMenu.add_command(label="タブを閉じる", command=self.deltab)

        menuBar.add_cascade(label="ファイル", menu=fileMenu)
        menuBar.add_cascade(label="編集", menu=editMenu)
        menuBar.add_cascade(label="タブ", menu=tabMenu)

        #New Notebooks commands
        newnotebookFlame = tk.LabelFrame(master, text="新規作成", width=540)

        GridSizeLabel = tk.Label(newnotebookFlame, text="大きさ：")
        self.GridSizeCombobox = ttk.Combobox(newnotebookFlame, width=2, height=1, values=VL.Grid_Size)
        self.GridSizeCombobox.current(0)
        TabNameLabel = tk.Label(newnotebookFlame, text="名前：")
        self.TabNameEntry = ttk.Entry(newnotebookFlame, width=60)
        self.EnterButton = ttk.Button(newnotebookFlame, text="作成", width=5, command=self.newnotebook_and_makebuttonactive)

        #.pack() New Notebooks commands
        GridSizeLabel.pack(side=tk.LEFT)
        self.GridSizeCombobox.pack(side=tk.LEFT)
        TabNameLabel.pack(side=tk.LEFT)
        self.TabNameEntry.pack(side=tk.LEFT)
        self.EnterButton.pack(side=tk.LEFT)
        newnotebookFlame.pack(side=tk.TOP, fill = tk.BOTH)

        #work flames
        MainWorkFlame = tk.LabelFrame(master, text="ワークスペース", width=540)
        self.Notebook = ttk.Notebook(MainWorkFlame)
        self.Notebook.bind("<Button-1>", self.selectnextnotebook)

        self.Notebook.pack(fill = tk.BOTH)
        MainWorkFlame.pack(side=tk.TOP, fill = tk.BOTH)

        #add words
        AddWordFlame = tk.LabelFrame(master, text="ワードの追加", width=540)
        AddWordLabel = tk.Label(AddWordFlame, text="ワード：",)
        self.AddWordEntry = ttk.Entry(AddWordFlame, width=60)
        AddWordButton = ttk.Button(AddWordFlame, text="追加", command=self.addword)
        self.SelectLabel = tk.Label(AddWordFlame, text="1, 1")
        self.SVSelectButton = ttk.Button(AddWordFlame, text="現在:横", command=self.switchSV)

        #.pack() add words
        AddWordLabel.pack(side=tk.LEFT)
        self.AddWordEntry.pack(side=tk.LEFT)
        AddWordButton.pack(side=tk.LEFT)
        self.SelectLabel.pack(side=tk.LEFT)
        self.SVSelectButton.pack(side=tk.LEFT)
        
        AddWordFlame.pack(side=tk.BOTTOM, fill=tk.BOTH)

        #Set window pos
        screen_W, screen_H = self.getscreencenter()

        master.geometry("+" + str(int(screen_W) - 370) + "+" + str(int(screen_H)))

        #variables
        self.LabelXY = [0, 0]
        self.NowNotebook = ""
        self.WordDirections = "side"

        #short cut binds
        self.master.bind("<Control-s>", self.savefile)
        self.master.bind("<Control-l>", self.loadfile)
        self.master.bind("<Control-b>", self.allgridblack)

        self.master.bind("<Control-n>", self.newnotebook_and_makebuttonactive)
        self.master.bind("<Shift-Key-Return>", self.addword)
        self.master.bind("<Control-d>", self.switchSV) 

        self.master.bind("<Control-w>", self.deltab)
        self.master.bind("<Control-e>", self.deleteword)
        #self.master.bind("<Button-1>", self.selectword)

###############################     
#   Add Word Frame Commands   #     
###############################     

    def addword(self, *event):
        add_word = self.AddWordEntry.get()
        words = list(self.AddWordEntry.get())
        words_id = []
        word_start_pos_adddata = self.LabelXY.copy()
        word_test_pos_range = self.LabelXY.copy()
        word_test_pos_end = self.LabelXY.copy()
        word_test_pos2 = self.LabelXY.copy()
        word_test_pos3 = self.LabelXY.copy()
        word_start_pos = self.LabelXY.copy()

        all_check = False
        stay_word = []
        range_check = False
        s_just_end = False
        v_just_end = False
        checks_list = [True, True, True, True, True]
        
        for w in words:
            words_id.append(VL.word_id_list.index(w) + 2)
        
        for tabs_data in VL.TabsList:
            if tabs_data[0] == self.Notebook.select():
                list_box = tabs_data[6]
                grid_size = int(tabs_data[2])
                grid_word_list = tabs_data[3]
                grid_id_list = tabs_data[4]
                listbox_data_list = tabs_data[7]
                break
        ###########################
        #長さの確認
        if self.WordDirections == "side":
            print(len(words) + word_test_pos_range[0], grid_size)
            if int(len(words) + word_test_pos_range[0] - 1) <= grid_size:
                if int(len(words) + word_test_pos_range[0]) == grid_size:
                    s_just_end = True
                range_check = True
        elif self.WordDirections == "vertical":
            if int(len(words) + word_test_pos_range[1]) <= grid_size:
                if int(len(words) + word_test_pos_range[1]) == grid_size:
                    v_just_end = True
                range_check = True

        if range_check == True:
            ###########################
            #同じワードの確認
            for in_list_word in listbox_data_list:
                if add_word == in_list_word[0]:
                    checks_list[3] = False
            ###########################
            #終端先の確認
            word_end_pos = [0, 0]
            S_count = 0
            V_count = 0
            if self.WordDirections == "side":
                    S_count = 1
            elif self.WordDirections == "vertical":
                    V_count = 1
            ###########################
            #白マスor黒マスの確認
            for word_id_2 in words_id:
                if word_id_2 != grid_word_list[word_test_pos2[1]][word_test_pos2[0]]:
                    if (grid_word_list[word_test_pos2[1]][word_test_pos2[0]] != 0) and (grid_word_list[word_test_pos2[1]][word_test_pos2[0]] != 1):
                        checks_list[2] = False

                if self.WordDirections == "side":
                    word_test_pos2[0] += 1
                elif self.WordDirections == "vertical":
                    word_test_pos2[1] += 1
            ###########################
            #縦横・終端の確認
            if self.WordDirections == "side":
                if word_test_pos3[1] != 0:
                    if (grid_word_list[word_test_pos3[1]][word_test_pos3[0]-1] != 0) and (grid_word_list[word_test_pos3[1]][word_test_pos3[0]-1] != 1):
                        checks_list[4] = False
                        print("1")
            if self.WordDirections == "vertical":
                if word_test_pos3[0] != 0:
                    if (grid_word_list[word_test_pos3[1]-1][word_test_pos3[0]] != 0) and (grid_word_list[word_test_pos3[1]-1][word_test_pos3[0]] != 1):
                        checks_list[4] = False
                        print("2")

            if self.WordDirections == "side":
                if word_test_pos3[0] <= grid_size-1:
                    if (grid_word_list[word_test_pos3[1]][word_test_pos3[0]+1] != 0) and (grid_word_list[word_test_pos3[1]][word_test_pos3[0]+1] != 1):
                        checks_list[4] = False
                        print("C1")
            if self.WordDirections == "vertical":
                if word_test_pos3[1] <= grid_size-1:
                    if (grid_word_list[word_test_pos3[1]+1][word_test_pos3[0]] != 0) and (grid_word_list[word_test_pos3[1]+1][word_test_pos3[0]] != 1):
                        checks_list[4] = False
                        print("C2")

            for word_id_2 in words_id:
                if word_id_2 != grid_word_list[word_test_pos3[1]][word_test_pos3[0]]:
                    if (grid_word_list[word_test_pos3[1]][word_test_pos3[0]] == 0) or (grid_word_list[word_test_pos3[1]][word_test_pos3[0]] == 1):
                        if self.WordDirections == "side":
                            if word_test_pos3[1] != 0:
                                up = grid_word_list[word_test_pos3[1]-1][word_test_pos3[0]]
                                if (up != 0) and (up != 1):
                                    checks_list[4] = False
                                    print("A1")
                            if word_test_pos3[1] != grid_size-1:
                                under = grid_word_list[word_test_pos3[1]+1][word_test_pos3[0]]
                                if (under != 0) and (under != 1):
                                    checks_list[4] = False
                                    print("A2")

                        elif self.WordDirections == "vertical":
                            if word_test_pos3[0] != 0:
                                left = grid_word_list[word_test_pos3[1]][word_test_pos3[0]-1]
                                if (left != 0) and (left != 1):
                                    checks_list[4] = False
                                    print("B1")
                            if word_test_pos3[0] != grid_size-1:
                                right = grid_word_list[word_test_pos3[1]][word_test_pos3[0]+1]
                                if (right != 0) and (right != 1):
                                    checks_list[4] = False
                                    print("B2")

                if self.WordDirections == "side":
                    word_test_pos3[0] += 1
                elif self.WordDirections == "vertical":
                    word_test_pos3[1] += 1
            ###########################
            #1文字かどうかの確認
            if len(words) == 1:
                checks_list[0] = False
            ###########################
            if False in checks_list:
                all_check = False
            else:
                all_check = True
            ###########################
            if all_check == False:
                if checks_list[0] == False:
                    error_type1 = tk.messagebox.showerror('注意', '1文字です。')
                elif checks_list[3] == False:
                    error_typr2 = tk.messagebox.showerror('注意', '既出のワードです。')
                elif checks_list[4] == False:
                    error_type3 = tk.messagebox.showerror('注意', 'ルール上配置できません。')
                else:
                    error_type4 = tk.messagebox.showerror('注意', '配置先に重ならない別のワードがあります。')

            elif all_check == True:
                for word_id_2 in words_id:
                    grid_word_list[word_start_pos[1]][word_start_pos[0]] = word_id_2
                    grid_id_list[word_start_pos[1]][word_start_pos[0]].config(image=VL.word_img_list[word_id_2])
                    if self.WordDirections == "side":
                        word_start_pos[0] += 1
                    if self.WordDirections == "vertical":
                        word_start_pos[1] += 1

                append_listbox_data = [add_word, len(words), self.WordDirections, word_start_pos_adddata[0], word_start_pos_adddata[1]]
                listbox_data_list.append(append_listbox_data)

                list_box.insert(0, add_word)


        
        elif range_check == False:
            error_type5 = tk.messagebox.showerror('注意', 'ワードがマスに収まりません。')

    def switchSV(self, *event):
        if self.WordDirections == "side":
            self.WordDirections = "vertical"
            self.SVSelectButton.config(text="現在:縦")
        elif self.WordDirections == "vertical":
            self.WordDirections = "side"
            self.SVSelectButton.config(text="現在:横")

#########################
#   NoteBook Commnads   #
#########################

    def deleteword(self, *event):
        for tabs_data in VL.TabsList:
            if tabs_data[0] == self.Notebook.select():
                list_box = tabs_data[6]
                grid_size = int(tabs_data[2])
                grid_word_list = tabs_data[3]
                grid_id_list = tabs_data[4]
                listbox_data_list = tabs_data[7]
                break

        now_select_word = list_box.get(tk.ACTIVE)
        for data in listbox_data_list:
            if data[0] == now_select_word:
                del_word_data = data
                break
        data_index = listbox_data_list.index(del_word_data)

        for i in range(del_word_data[1]):
            side_vert_checks = [True, True, True, True]
            side_share = False
            vert_share = False
            if del_word_data[4] == 0:
                side_vert_checks[0] = False
            elif del_word_data[4] == grid_size - 1:
                side_vert_checks[1] = False
            elif del_word_data[3] == 0:
                side_vert_checks[2] = False
            elif del_word_data[3] == grid_size - 1:
                side_vert_checks[3] = False

            if del_word_data[2] == "side":
                if side_vert_checks[0] == True:
                    if grid_word_list[del_word_data[4] - 1][del_word_data[3]] != 0 and grid_word_list[del_word_data[4] - 1][del_word_data[3]] != 1:
                        side_share = True
                if side_vert_checks[1] == True:
                    if grid_word_list[del_word_data[4] + 1][del_word_data[3]] != 0 and grid_word_list[del_word_data[4] + 1][del_word_data[3]] != 1:
                        side_share = True
            if del_word_data[2] == "vertical":
                if side_vert_checks[2] == True:
                    if grid_word_list[del_word_data[4]][del_word_data[3] - 1] != 0 and grid_word_list[del_word_data[4]][del_word_data[3] - 1] != 1:
                        vert_share = True
                if side_vert_checks[3] == True:
                    if grid_word_list[del_word_data[4]][del_word_data[3] + 1] != 0 and grid_word_list[del_word_data[4]][del_word_data[3] + 1] != 1:
                        vert_share = True

            if del_word_data[2] == "side":
                if side_share != True:
                    grid_word_list[del_word_data[4]][del_word_data[3]] = 0
                    grid_id_list[del_word_data[4]][del_word_data[3]].config(image=VL.word_img_list[0])
            if del_word_data[2] == "vertical":
                if vert_share != True:
                    grid_word_list[del_word_data[4]][del_word_data[3]] = 0
                    grid_id_list[del_word_data[4]][del_word_data[3]].config(image=VL.word_img_list[0])

            if del_word_data[2] == "side":
                del_word_data[3] += 1
            if del_word_data[2] == "vertical":
                del_word_data[4] += 1

        list_box.delete(tk.ACTIVE)
        listbox_data_list.pop(data_index)

    def selectword(self, *event):
        for tabs_data in VL.TabsList:
            if tabs_data[0] == self.Notebook.select():
                list_box = tabs_data[6]
                grid_id_list = tabs_data[4]
                listbox_data_list = tabs_data[7]
                break
        if list_box.size() > 0:
            now_select_word = list_box.get(tk.ACTIVE)
            for data in listbox_data_list:
                if data[0] == now_select_word:
                    select_word_data = data.copy()
                    break

            for labels in grid_id_list:
                for label in labels:
                    label.config(bg="#404040")

            for i in range(select_word_data[1]):
                grid_id_list[select_word_data[4]][select_word_data[3]].config(bg="#00ff00")
                if select_word_data[2] == "side":
                    select_word_data[3] += 1
                if select_word_data[2] == "vertical":
                    select_word_data[4] += 1

    def selectnextnotebook(self, event):
        self.LabelXY = []
        self.SelectLabel.config(text="")
        self.NowNotebook = self.Notebook.select()

    def labelblack(self, event):
        label_id = event.widget
        for tabs_data in VL.TabsList:
            if tabs_data[0] == self.Notebook.select():
                label_id_list = tabs_data[4]
                grid_word_list = tabs_data[3]
                break

        for labels in label_id_list:
            if label_id in labels:
                x_pos = labels.index(label_id)
                y_pos = label_id_list.index(labels)
                break

        if grid_word_list[y_pos][x_pos] == 0:
            grid_word_list[y_pos][x_pos] = 1
            label_id.config(image=VL.word_img_list[1])
        elif grid_word_list[y_pos][x_pos] == 1:
            grid_word_list[y_pos][x_pos] = 0
            label_id.config(image=VL.word_img_list[0])



    def labelposget(self, event):
        label_id = event.widget
        label_id.config(bg="red")
        for tabs_data in VL.TabsList:
            if tabs_data[0] == self.Notebook.select():
                label_id_list = tabs_data[4]
                break
        
        #Return white
        for labels in label_id_list:
            for label in labels:
                label.config(bg="#404040")

        for labels in label_id_list:
            if label_id in labels:
                x_pos = labels.index(label_id)
                y_pos = label_id_list.index(labels)
                break

        self.LabelXY = [x_pos, y_pos]
        label_id.config(bg="red")
        self.SelectLabel.config(text=str(self.LabelXY[0] + 1) + ", " + str(self.LabelXY[1] + 1))

    def getscreencenter(self):
        scr_W = self.winfo_screenwidth()/2
        scr_H = self.winfo_screenheight()/4

        return scr_W, scr_H

    def getwindowcenter(self):
        win_W = self.master.winfo_geometry()

    def deltab(self, *event):
        for tab_data_list in VL.TabsList:
            if tab_data_list[0] == self.Notebook.select():
                VL.TabsList.remove(tab_data_list)
        self.Notebook.forget(self.Notebook.select())

##################################
#   Make New Notebook Commands   #
##################################
    def newnotebook_and_makebuttonactive(self, *event):
        gridsize = int(self.GridSizeCombobox.get())
        self.newnotebook(new_tab_name=self.TabNameEntry.get()+" "+str(gridsize)+"x"+str(gridsize), grid_size=gridsize, ifload=False)
        self.makebuttonactive()

    def newnotebook(self, new_tab_name, grid_size, ifload, *l_grid_list, **l_listbox_data_list):

        #Make grid state list and listbox wordlist
        if (grid_size == 7):
            if (ifload == False):
                grid_list = deepcopy(VL.Grid_List_Original_7)
            grid_id_list = deepcopy(VL.Grid_Id_List_7)
        elif (grid_size == 12):
            if (ifload == False):
                grid_list = deepcopy(VL.Grid_List_Original_12)
            grid_id_list = deepcopy(VL.Grid_Id_List_12)
        elif (grid_size == 13):
            if (ifload == False):
                grid_list = deepcopy(VL.Grid_List_Original_13)
            grid_id_list = deepcopy(VL.Grid_Id_List_13)
        elif (grid_size == 20):
            if (ifload == False):
                grid_list = deepcopy(VL.Grid_List_Original_20)
            grid_id_list = deepcopy(VL.Grid_Id_List_20)
        S_Frame_list = deepcopy(VL.Side_Frame_list)

        new_tab_lists = [grid_list, grid_id_list, S_Frame_list]

        if (ifload == True):
            grid_list = l_grid_list
            new_listbox_data = l_listbox_data_list
        elif (ifload == False):
            new_listbox_data = []
        
        #grid_size = int(self.GridSizeCombobox.get())
        NewFrame = tk.Frame(self.Notebook)
        NewGridFrame = tk.Frame(NewFrame, width=(int(grid_size)+2)*25, height=(int(grid_size)+2)*25)
        SideOptionsFrame = tk.Frame(NewFrame)
        ListboxFrame = tk.Frame(SideOptionsFrame)
        ListboxOptionsFrame = tk.Frame(SideOptionsFrame)
        NewListbox = tk.Listbox(ListboxFrame, width=30, height=20)
        NewListbox.bind("<<ListboxSelect>>", self.selectword)
        ListboxYBar = tk.Scrollbar(ListboxFrame, orient=tk.VERTICAL)
        NewListbox['yscrollcommand'] = ListboxYBar.set
        ListboxXBar = tk.Scrollbar(ListboxFrame, orient=tk.HORIZONTAL)
        NewListbox['xscrollcommand'] = ListboxXBar.set
        ListboxWordDelButton = ttk.Button(ListboxOptionsFrame, text="削除", command=self.deleteword)
        ListboxWordSortButton = ttk.Button(ListboxOptionsFrame, text="音順:降")
        #deltabButton = ttk.Button(SideOptionsFrame, text="閉じる", command=self.deltab)

        #Make new grid  

        for gridsize_v in range(grid_size):
            #frame
            S_Frame_list.append(tk.Frame(NewGridFrame))
            for gridsize_s in range(grid_size):
                #grids
                ##print(grid_list[gridsize_v][gridsize_s])
                load_img = VL.word_img_list[grid_list[gridsize_v][gridsize_s]]
                grid_id_list[gridsize_v].append(tk.Label(S_Frame_list[gridsize_v], image=load_img, bg="#404040"))
                grid_id_list[gridsize_v][-1].bind("<Button-1>", self.labelposget)
                grid_id_list[gridsize_v][-1].bind("<Button-3>", self.labelblack, "+")
                grid_id_list[gridsize_v][-1].pack(side=tk.LEFT)
            S_Frame_list[-1].pack(side=tk.TOP)

        ListboxYBar.pack(side=tk.RIGHT, fill=tk.Y)
        ListboxYBar.config(command=NewListbox.yview)

        NewListbox.pack(side=tk.TOP, fill=tk.Y)

        ListboxXBar.pack(side=tk.TOP, fill=tk.X)
        ListboxXBar.config(command=NewListbox.xview)

        ListboxFrame.pack(side=tk.TOP)
        ListboxWordSortButton.pack(side=tk.LEFT)
        ListboxWordDelButton.pack(side=tk.RIGHT)
        ListboxOptionsFrame.pack(side=tk.TOP, fill=tk.X)
        #deltabButton.pack(side=tk.BOTTOM, anchor=tk.E)
        NewGridFrame.pack(side=tk.LEFT, anchor=tk.N)
        SideOptionsFrame.pack(side=tk.LEFT, anchor=tk.N)

        #Add Tab
        self.Notebook.add(NewFrame, text=new_tab_name)
        VL.TabsList.append(
            [
                self.Notebook.tabs()[-1], #[0] Notebook id
                new_tab_name, #[1]
                grid_size, #[2]
                new_tab_lists[0], #[3] Grid list
                new_tab_lists[1], #[4] Grid ID list
                new_tab_lists[2], #[5] Frame list
                NewListbox, #[6]
                new_listbox_data #[7]
            ]
        )
        self.Notebook.select(self.Notebook.tabs()[-1])

    def makebuttonactive(self):
        self.EnterButton.config(state=tk.NORMAL)

#########################
#   MenuBar Commands    #
#########################

    def onexit(self):
        self.quit()

    def savefile(self, *event):
        now_select_tab = self.Notebook.select()
        for tab_data_list in VL.TabsList:
            if tab_data_list[0] == now_select_tab:
                TAB_DATA = tab_data_list.copy()

        tab_name = TAB_DATA[1]
        
        filename = filedialog.asksaveasfilename(defaultextension="txt", filetypes=[('Text', '*.txt')], initialfile=tab_name)

        if (filename != ""):
            #self.savingwindowshow()
            #self.Sapp

            with open(filename, mode="w", encoding="utf-8") as to_save:
                to_save.write(tab_name + "\n") #project name
                to_save.write(str(TAB_DATA[2]) + "\n") #grid size
                
                #grid datas
                for grid_datas in TAB_DATA[3]:
                    for grid_data in grid_datas:
                        to_save.write(str(grid_data) + ",")
                    to_save.write("\n")

                to_save.write("\nlist_data\n")
                for list_datas in TAB_DATA[7]:
                    to_save.write(list_datas[0] + "," + str(list_datas[1]) + "," + list_datas[2] + "," + str(list_datas[3]) + "," + str(list_datas[4]) + "\n")
            #savingwindowdestroy()
            
    def loadfile(self, *event):
        filename = filedialog.askopenfilename(defaultextension="txt", filetypes=[('Text', '*.txt')])
        if (filename != ""):
            with open(filename, mode="r") as load_file:
                loadfiledata_original = load_file.readlines()
            load_file_data = []
            load_grid_list = []
            count = 0
            for data in loadfiledata_original:
                data_s = data.strip("\n")
                if (count == 0):
                    load_file_data.append(data_s)

                elif (count == 1):
                    load_file_data.append(data_s)

                elif (count > 1):
                    data_s_2 = data_s.split(",")
                    data_s_2.pop()
                    data_s = [int(s) for s in data_s_2]
                    load_grid_list.append(data_s)

                count += 1
            self.newnotebook(new_tab_name=load_file_data[0], grid_size=int(load_file_data[1]), ifload=True, l_grid_list=load_grid_list)

    def savingwindowshow(self):
        Swin = tk.Tk()
        Sapp = SavingWindow(master=Swin)
        Sapp.mainloop()

    def allgridblack(self, *event):
        for tabs_data in VL.TabsList:
            if tabs_data[0] == self.Notebook.select():
                grid_word_list = tabs_data[3]
                grid_id_list = tabs_data[4]
                break
        x_count = 0
        y_count = 0
        for y_grid_word_list in grid_word_list:
            x_count = 0
            for grid_word in y_grid_word_list:
                if (grid_word == 0):
                    grid_word_list[y_count][x_count] = 1
                    grid_id_list[y_count][x_count].config(image=VL.word_img_list[1])
                x_count += 1
            y_count += 1

##################### ################################################################################
#   Saving Window   # NOT WORKING NOW!!!
##################### ################################################################################

class SavingWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        master.title("保存中")

        self.saveLabelFrame = tk.LabelFrame(master, text="保存中です。触らないでください。", width=200, height=50)
        self.saveProgressbar = ttk.Progressbar(self.saveLabelFrame, maximum=100, mode="determinate", length=200)

        self.saveProgressbar.pack()
        self.saveLabelFrame.pack()

    def stepprogressbar(self):
        self.saveProgressbar.step(10)

######################## ################################################################################
#   Done Application   # 
######################## ################################################################################

def main():
    win = tk.Tk()
    app = Application(master=win)
    app.mainloop()

if __name__ == "__main__":
    main()