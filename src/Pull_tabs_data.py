import Variables_List as VL

def pulltabsdata(now_select):
    for tabs_data in VL.TabsList:
        if tabs_data[0] == now_select:
            Notebook_id = tabs_data[0]      #Notebook id    [0]
            Tab_name = tabs_data[1]         #Notebook name  [1]
            Grid_size = tabs_data[2]        #Grid size      [2]
            Grid_list = tabs_data[3]        #Grid list      [3]
            Grid_id_list = tabs_data[4]     #Grid ID list   [4]
            Frame_id_list = tabs_data[5]    #Frame list     [5]
            Listbox = tabs_data[6]          #Listbox widget [6]
            Listbox_data = tabs_data[7]     #Listbox data   [7]
            Sort_rule = tabs_data[8]        #Sort rule      [8]
            ListboxSortButtons = tabs_data[9]   # [0 : alp or str] [1 : up or down] [9]
            break
    
    returnlist = [Notebook_id, Tab_name, Grid_size, Grid_list, Grid_id_list, Frame_id_list, Listbox, Listbox_data, Sort_rule, ListboxSortButtons, tabs_data]
    return returnlist

def pulltabsdata2(now_select):
    for tabs_data in VL.TabsList:
        if tabs_data[1] == now_select:
            Notebook_id = tabs_data[0]      #Notebook id    [0]
            Tab_name = tabs_data[1]         #Notebook name  [1]
            Grid_size = tabs_data[2]        #Grid size      [2]
            Grid_list = tabs_data[3]        #Grid list      [3]
            Grid_id_list = tabs_data[4]     #Grid ID list   [4]
            Frame_id_list = tabs_data[5]    #Frame list     [5]
            Listbox = tabs_data[6]          #Listbox widget [6]
            Listbox_data = tabs_data[7]     #Listbox data   [7]
            Sort_rule = tabs_data[8]        #Sort rule      [8]
            ListboxSortButtons = tabs_data[9]   # [0 : alp or str] [1 : up or down] [9]
            break
    
    returnlist = [Notebook_id, Tab_name, Grid_size, Grid_list, Grid_id_list, Frame_id_list, Listbox, Listbox_data, Sort_rule, ListboxSortButtons, tabs_data]
    return returnlist

def gettabsname():
    names = []
    for tab_data in VL.TabsList:
        names.append(tab_data[1])

    return names