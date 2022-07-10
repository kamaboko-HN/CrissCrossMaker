from cgi import test
from cgitb import enable, text
from copy import deepcopy
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
from tkinter import CENTER, FLAT, LEFT, SOLID, Variable, ttk
from tkinter.tix import NoteBook
from tkinter import filedialog
from tkinter import messagebox
import glob
from turtle import bgcolor, left, right

from numpy import imag
from natsort import natsorted

import Variables_List as VL
import Listbox_Sort as LS
import save_and_load as SaL
import Pull_tabs_data as Ptd
import OutputExcel as OpE

############################## ######################################################################
#   Application Main Frame   # 
############################## ######################################################################

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        #Load Images
        for images in natsorted(glob.glob("img/*.png")):
            VL.word_img_list.append(tk.PhotoImage(file=images))

        master.title("CrissCrossMaker")

        menuBar = tk.Menu()
        self.master.config(menu=menuBar)

        fileMenu = tk.Menu(tearoff=0)
        fileMenu.add_command(label="保存", command=self.savefile)
        fileMenu.add_command(label="開く", command=self.loadfile)
        fileMenu.add_separator()
        fileMenu.add_command(label="出力", command=self.output)
        fileMenu.add_separator()
        fileMenu.add_command(label="終了", command=self.onexit)
        
        editMenu = tk.Menu(tearoff=0)
        editMenu.add_command(label="元に戻す")
        editMenu.add_command(label="やり直し")
        editMenu.add_separator()
        editMenu.add_command(label="全黒塗り", command=self.allgridblack)

        menuBar.add_cascade(label="ファイル", menu=fileMenu)
        menuBar.add_cascade(label="編集", menu=editMenu)

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
        AddWordLabel = tk.Label(AddWordFlame, text="ワード：")
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
        self.master.bind("<Control-o>", self.output)
        self.master.bind("<Control-b>", self.allgridblack)

        self.master.bind("<Control-n>", self.newnotebook_and_makebuttonactive)
        self.master.bind("<Shift-Key-Return>", self.addword)
        self.master.bind("<Control-d>", self.switchSV) 

        self.master.bind("<Control-w>", self.deltab)
        self.master.bind("<Control-e>", self.deleteword)
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
        
        list_box = Ptd.pulltabsdata(self.Notebook.select())[6]
        grid_size = int(Ptd.pulltabsdata(self.Notebook.select())[2])
        grid_word_list = Ptd.pulltabsdata(self.Notebook.select())[3]
        grid_id_list = Ptd.pulltabsdata(self.Notebook.select())[4]
        listbox_data_list = Ptd.pulltabsdata(self.Notebook.select())[7]
        sort_rule = Ptd.pulltabsdata(self.Notebook.select())[8]
        Buttons = Ptd.pulltabsdata(self.Notebook.select())[9]
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
                LS.CCMsort(Listboxobject=list_box, sort_type=sort_rule[0], up_or_down=sort_rule[1])


        
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
#   Listbox Commands    #
#########################
    def deleteword(self, *event):
        list_box = Ptd.pulltabsdata(self.Notebook.select())[6]
        grid_size = int(Ptd.pulltabsdata(self.Notebook.select())[2])
        grid_word_list = Ptd.pulltabsdata(self.Notebook.select())[3]
        grid_id_list = Ptd.pulltabsdata(self.Notebook.select())[4]
        listbox_data_list = Ptd.pulltabsdata(self.Notebook.select())[7]

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

    def switchAS(self):
        list_box = Ptd.pulltabsdata(self.Notebook.select())[6]
        sort_rule = Ptd.pulltabsdata(self.Notebook.select())[8]
        Buttons = Ptd.pulltabsdata(self.Notebook.select())[9]
        
        if sort_rule[0] == "alphabetical":
            sort_rule[0] = "stroke"
            Buttons[0].config(text="音順")
        elif sort_rule[0] == "stroke":
            sort_rule[0] = "alphabetical"
            Buttons[0].config(text="文字数順")

        LS.CCMsort(Listboxobject=list_box, sort_type=sort_rule[0], up_or_down=sort_rule[1])

    def switchUPDOWN(self):
        list_box = Ptd.pulltabsdata(self.Notebook.select())[6]
        sort_rule = Ptd.pulltabsdata(self.Notebook.select())[8]
        Buttons = Ptd.pulltabsdata(self.Notebook.select())[9]
        
        if sort_rule[1] == False:
            sort_rule[1] = True
            Buttons[1].config(text="降")
        elif sort_rule[1] == True:
            sort_rule[1] = False
            Buttons[1].config(text="昇")
        
        LS.CCMsort(Listboxobject=list_box, sort_type=sort_rule[0], up_or_down=sort_rule[1])

#########################
#   NoteBook Commands   #
#########################

    def selectword(self, *event):
        list_box = Ptd.pulltabsdata(self.Notebook.select())[6]
        grid_id_list = Ptd.pulltabsdata(self.Notebook.select())[4]
        listbox_data_list = Ptd.pulltabsdata(self.Notebook.select())[7]
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

    def labelposget(self, event):
        label_id = event.widget
        label_id.config(bg="red")
        label_id_list = Ptd.pulltabsdata(self.Notebook.select())[4]
        
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
        VL.TabsList.remove(Ptd.pulltabsdata(self.Notebook.select())[-1])
        self.Notebook.forget(self.Notebook.select())

##################################
#   Make New Notebook Commands   #
##################################
    def newnotebook_and_makebuttonactive(self, *event):
        gridsize = int(self.GridSizeCombobox.get())

        #Make grid state list and listbox wordlist
        if (gridsize == 7):
            new_grid_list = deepcopy(VL.Grid_List_Original_7)
        elif (gridsize == 12):
            new_grid_list = deepcopy(VL.Grid_List_Original_12)
        elif (gridsize == 13):
            new_grid_list = deepcopy(VL.Grid_List_Original_13)
        elif (gridsize == 20):
            new_grid_list = deepcopy(VL.Grid_List_Original_20)

        new_listbox_data = []

        self.newnotebook(
            new_tab_name=self.TabNameEntry.get()+" "+str(gridsize)+"x"+str(gridsize),
            grid_size=gridsize, grid_list=new_grid_list, listbox_data=new_listbox_data)

        self.makebuttonactive()

    def newnotebook(self, new_tab_name, grid_size, grid_list, listbox_data):
        if (grid_size == 7):
            grid_id_list = deepcopy(VL.Grid_Id_List_7)
        elif (grid_size == 12):
            grid_id_list = deepcopy(VL.Grid_Id_List_12)
        elif (grid_size == 13):
            grid_id_list = deepcopy(VL.Grid_Id_List_13)
        elif (grid_size == 20):
            grid_id_list = deepcopy(VL.Grid_Id_List_20)

        S_Frame_list = deepcopy(VL.Side_Frame_list)
            
        new_tab_lists = [grid_list, grid_id_list, S_Frame_list]
        
        #grid_size = int(self.GridSizeCombobox.get())
        NewFrame = tk.Frame(self.Notebook, bd=1)

        NewGridFrame = tk.Frame(NewFrame, width=(int(grid_size)+2)*25, height=(int(grid_size)+2)*25, bd=1)


        NewGridOptionsFrame = tk.Frame(NewFrame)

        NewListboxFrame = tk.Frame(NewGridOptionsFrame, height=(int(grid_size)+2)*25, bd=1)
        NewListbox = tk.Listbox(NewListboxFrame, width=30, height=20)
        NewListbox.bind("<<ListboxSelect>>", self.selectword)
        ListboxYBar = tk.Scrollbar(NewListboxFrame, orient=tk.VERTICAL, command=NewListbox.yview)
        NewListbox["yscrollcommand"] = ListboxYBar.set
        ListboxXBar = tk.Scrollbar(NewListboxFrame, orient=tk.HORIZONTAL, command=NewListbox.xview)
        NewListbox["xscrollcommand"] = ListboxXBar.set

        ListboxOptionsFrame = tk.Frame(NewGridOptionsFrame, bd=1)
        ListboxSortbutton = ttk.Button(ListboxOptionsFrame, text="音順", command=self.switchAS)
        ListboxSortbutton_2 = ttk.Button(ListboxOptionsFrame, text="降", width=3, command=self.switchUPDOWN)
        ListboxWordDelButton = ttk.Button(ListboxOptionsFrame, text="削除", command=self.deleteword)

        TabOptionsFrame = tk.Frame(NewGridOptionsFrame)
        deltabButton = ttk.Button(TabOptionsFrame, text="閉じる", command=self.deltab)

        #Make new grid  

        for gridsize_v in range(grid_size):
            #frame
            S_Frame_list.append(tk.Frame(NewGridFrame))
            for gridsize_s in range(grid_size):
                #grids
                ##print(grid_list[gridsize_v][gridsize_s])
                print(str(gridsize_v) + "," + str(gridsize_s))
                print(grid_list[gridsize_v][gridsize_s])
                load_img = VL.word_img_list[grid_list[gridsize_v][gridsize_s]]
                grid_id_list[gridsize_v].append(tk.Label(S_Frame_list[gridsize_v], image=load_img, bg="#404040"))
                grid_id_list[gridsize_v][-1].bind("<Button-1>", self.labelposget)
                grid_id_list[gridsize_v][-1].pack(side=tk.LEFT)
            S_Frame_list[-1].pack(side=tk.TOP)

        ListboxYBar.pack(side=tk.RIGHT, fill=tk.Y)
        NewListbox.pack(side=tk.TOP, fill=tk.Y)
        ListboxXBar.pack(side=tk.TOP, fill=tk.X)
        NewListboxFrame.pack(side=tk.TOP)

        ListboxSortbutton.pack(side=tk.LEFT)
        ListboxSortbutton_2.pack(side=tk.LEFT)
        ListboxWordDelButton.pack(side=tk.RIGHT)
        ListboxOptionsFrame.pack(side=tk.TOP,fill=tk.X)

        deltabButton.pack(side=tk.RIGHT)
        TabOptionsFrame.pack(side=tk.BOTTOM, fill=tk.X)

        NewGridFrame.pack(side=tk.LEFT, anchor=tk.N)
        NewGridOptionsFrame.pack(side=tk.LEFT, anchor=tk.N, fill=tk.Y)
        
        if listbox_data != []:
            for data in listbox_data:
                NewListbox.insert(0, data[0])

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
                listbox_data, #[7]
                VL.default_sort_rule.copy(), #[8]
                [ListboxSortbutton, ListboxSortbutton_2] #[9] [0 : alp or str][1 : up or down]
            ]
        )
        self.Notebook.select(self.Notebook.tabs()[-1])
        return self.Notebook.tabs()[-1]

    def makebuttonactive(self):
        self.EnterButton.config(state=tk.NORMAL)

#########################
#   MenuBar Commands    #
#########################

    def onexit(self):
        self.quit()

    def savefile(self, *event):
        SaL.CCM_save(self.Notebook.select())
            
    def loadfile(self, *event):
        ntl = SaL.CCM_load()
        nowmake = self.newnotebook(new_tab_name=ntl[0], grid_size=ntl[1], grid_list=ntl[2], listbox_data=ntl[3])

    def output(self):
        opwindow = OpE.outputshow()

    def savingwindowshow(self):
        Swin = tk.Tk()
        Sapp = SavingWindow(master=Swin)
        Sapp.mainloop()

    def allgridblack(self, *event):
        grid_word_list = Ptd.pulltabsdata(self.Notebook.select())[3]
        grid_id_list = Ptd.pulltabsdata(self.Notebook.select())[4]

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