import dearpygui.dearpygui as dpg
from track_manager import TrackManager
from collection_manager import CollectionManager
from collection_creator import CollectionCreator
from track import Track
from collection import Collection
import db
import os
import link_importer
from gui_relay import InfoPane
track_manager = TrackManager()  
collection_manager = CollectionManager()
collection_creator = CollectionCreator()
from configparser import ConfigParser
import config_writer
from threading import Thread

config = ConfigParser()
config.read("dtconfig.ini")

music_directory = config["DEFAULT"]["Music Library"]
spotify_client_id = config["DEFAULT"]["Spotify Client ID"]
spotify_client_secret = config["DEFAULT"]["Spotify Client Secret"]

list_items= 55
info_columns = ["Title", "Artist", "Duration", "Key", "BPM", "Loudness", "Danceability", "Energy", "Quality"]

def threadedscan():
    dir_location = str(dpg.get_value("dir_location"))
    dirs = collection_creator.get_all_folders(dir_location)
    dirnum = 0
    for dir in dirs:
        dirnum += 1
        print("Scanning..." + dir + " " + str(dirnum) + "/" + str(len(dirs)))
        collection_creator.collection_from_folder(dir,False)
        refresh_collections_list()

thscan = Thread(target=threadedscan)


def scan_all_folders(sender):
    thscan.start()




def modify_setting(sender):
    new_music_directory = dpg.get_value("dir_location")
    new_spotify_client_id = dpg.get_value("sp_client_id")
    new_spotify_client_secret = dpg.get_value("sp_client_secret")
    config_writer.modify_config("Music Library", new_music_directory)
    config_writer.modify_config("Spotify Client ID", new_spotify_client_id)
    config_writer.modify_config("Spotify Client Secret", new_spotify_client_secret)
    print("Config file modified.")

def link_callback(sender):
    link = dpg.get_value("input_text")
    dpg.delete_item("link_box")
    #print(link)
    link_importer.prompter(link)
    refresh_collections_list()


def sort_callback(sender, sort_specs):

    # sort_specs scenarios:
    #   1. no sorting -> sort_specs == None
    #   2. single sorting -> sort_specs == [[column_id, direction]]
    #   3. multi sorting -> sort_specs == [[column_id, direction], [column_id, direction], ...]
    #
    # notes:
    #   1. direction is ascending if == 1
    #   2. direction is ascending if == -1

    # no sorting case
    if sort_specs is None: return

    rows = dpg.get_item_children(sender, 1)

    # create a list that can be sorted based on first cell
    # value, keeping track of row and value used to sort
    sortable_list = []
    for row in rows:
        first_cell = dpg.get_item_children(row, 1)[0]
        sortable_list.append([row, dpg.get_value(first_cell)])

    def _sorter(e):
        return e[1]

    sortable_list.sort(key=_sorter, reverse=sort_specs[0][1] < 0)

    # create list of just sorted row ids
    new_order = []
    for pair in sortable_list:
        new_order.append(pair[0])

    dpg.reorder_items(sender, 1, new_order)


def print_me(sender):
    print(f"Menu Item: {sender}")


def settings_window(sender):
    with dpg.mutex():

        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()

        
        with dpg.window(label="Settings", show=True, tag="settings_id", modal=True, no_title_bar=True, width=400, height=350, no_resize=True) as settings_id:
            dpg.add_text("Settings")
            dpg.bind_item_font(dpg.last_item(), "roboto-condensed-36")
            dpg.add_spacer()
            dpg.add_text("Music Directory")
            with dpg.group(horizontal=True) as group:
                dpg.add_input_text(default_value=music_directory, tag="dir_location")
                dpg.add_button(label="Browse")
            dpg.add_button(label="Scan Folders", callback=scan_all_folders)
            dpg.add_separator()
            dpg.add_spacer()
            dpg.add_text("Spotify Client ID")
            dpg.add_input_text(default_value=spotify_client_id, tag="sp_client_id")
            dpg.add_text("Spotify Client Secret")
            dpg.add_input_text(default_value=spotify_client_secret, password=True, tag="sp_client_secret")
            dpg.add_spacer()
            with dpg.group(horizontal=True):
                dpg.add_button(label="Close", width=75, callback= lambda: dpg.delete_item(settings_id) )
                dpg.add_button(label="Save", width=75, callback=modify_setting)
    
    dpg.split_frame()
    width = dpg.get_item_width(settings_id)
    height = dpg.get_item_height(settings_id)
    dpg.set_item_pos(settings_id, [viewport_width // 2 - width // 2, viewport_height // 2 - height // 2])   

def collection_from_link(sender):
    with dpg.mutex():

        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()

        
        with dpg.window(label="Insert Link", show=True, tag="link_box", width=600, height=120) as link_box:
            dpg.add_text("Insert your link:")
            dpg.add_separator()
            dpg.add_input_text(tag="input_text", width=-1)
            with dpg.group(horizontal=True):
                dpg.add_button(label="Add", width=75, callback=link_callback)
                dpg.add_button(label="Cancel", width=75, callback= lambda: dpg.delete_item(link_box) )
    
    dpg.split_frame()
    width = dpg.get_item_width(link_box)
    height = dpg.get_item_height(link_box)
    dpg.set_item_pos(link_box, [viewport_width // 2 - width // 2, viewport_height // 2 - height // 2])   



def get_selected_collection(sender, collection_name):
    #print(collection_name)
    get_collection_info(collection_name)

def create_matrix(tracks_info):
    w = len(info_columns)
    h = len(tracks_info)
    table_matrix = [[0 for x in range(w)] for y in range(h)]
    return table_matrix, w, h


def get_collection_info(collection_name):
    dpg.delete_item("Collections Info" ,children_only=True)
    tracks_info = collection_manager.get_tracks_by_collection_name(collection_name)
    table_matrix, w, h = create_matrix(tracks_info)
    for column in range(w):
        for row in range(h):
            table_matrix[row][column] = tracks_info[row][column]
    #print(table_matrix)
    update_table(w, h, table_matrix)

def prompt_callback(sender, dir, analyze):
    dpg.delete_item("modal_id")
    if (analyze == True):
        InfoPane.refresh_info_pane("Analyzing..." + " " + dir)
        collection_creator.collection_from_folder(dir,True)
    else:
        InfoPane.refresh_info_pane("Scanning..." + " " + dir)
        collection_creator.collection_from_folder(dir,False)
    #print(dir, analyze)
    sel_row = dpg.get_value("Collections")
    get_collection_info(sel_row)
    refresh_collections_list()
    InfoPane.refresh_info_pane("Done...")
    #collection_creator.collection_from_folder(dir,True)


def show_info(app_data):
    dir = app_data['file_path_name']
    print(dir)
    with dpg.mutex():

        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()

        with dpg.window(label="Delete Files", modal=True, show=True, tag="modal_id", no_title_bar=True) as modal_id:
            dpg.add_text("Do you want to analyze the tracks?")
            dpg.add_separator()
            #dpg.add_checkbox(label="Don't ask me next time")
            with dpg.group(horizontal=True):
                dpg.add_button(label="Yes", width=75, callback=lambda x: prompt_callback(x, dir, True))
                dpg.add_button(label="No", width=75, callback=lambda x: prompt_callback(x, dir, False))
    dpg.split_frame()
    width = dpg.get_item_width(modal_id)
    height = dpg.get_item_height(modal_id)
    dpg.set_item_pos(modal_id, [viewport_width // 2 - width // 2, viewport_height // 2 - height // 2])




def callback(sender, app_data):
    print('OK was clicked.')
    print("Sender: ", sender)
    print("App Data: ", app_data)
    
    show_info(app_data)
    #collection_creator.collection_from_folder(dir,False)

def cancel_callback(sender, app_data):
    print('Cancel was clicked.')
    print("Sender: ", sender)
    print("App Data: ", app_data)


def update_table(w, h, table_matrix):
            for column in info_columns:
                dpg.add_table_column(label=column, parent="Collections Info", width_stretch=True)
            for row in range(h):
                with dpg.table_row(parent="Collections Info"):
                    for column in range(w):
                        match column:
                            case 0:
                                if table_matrix[row][column] is None:
                                    dpg.add_selectable(label=" - ", span_columns=True, height=20)
                                    dpg.bind_item_font(dpg.last_item(), "proggyvec-18")
                                else:
                                    dpg.add_selectable(label=str(table_matrix[row][column]), span_columns=True, height=20)
                                    dpg.bind_item_font(dpg.last_item(), "proggyvec-18")
                            case 1:
                                if table_matrix[row][column] is None:
                                    dpg.add_selectable(label="-", span_columns=True, height=20)
                                    dpg.bind_item_font(dpg.last_item(), "proggyvec-18")
                                else:
                                    dpg.add_selectable(label=str(table_matrix[row][column]), span_columns=True, height=20)
                                    dpg.bind_item_font(dpg.last_item(), "proggyvec-18")
                            case 2:
                                if table_matrix[row][column] is None:
                                    dpg.add_selectable(label="-", span_columns=True)
                                    dpg.bind_item_font(dpg.last_item(), "proggyvec-18")
                                else:
                                    duration_s = int(table_matrix[row][column])
                                    duration_m = duration_s // 60
                                    duration_s = duration_s % 60
                                    dpg.add_selectable(label=str(duration_m) + "m " + str(duration_s) + "s", span_columns=True)
                                    dpg.bind_item_font(dpg.last_item(), "proggyvec-18")
                            case 3:
                                if table_matrix[row][column] is None:
                                    dpg.add_selectable(label="-", span_columns=True)
                                    dpg.bind_item_font(dpg.last_item(), "proggyvec-18")
                                else:
                                    dpg.add_selectable(label=str(table_matrix[row][column]), span_columns=True)
                                    dpg.bind_item_font(dpg.last_item(), "proggyvec-18")
                            case 4:
                                if table_matrix[row][column] is None:
                                    dpg.add_selectable(label="-", span_columns=True)
                                    dpg.bind_item_font(dpg.last_item(), "proggyvec-18")
                                else:
                                    rounded_bpm = round(table_matrix[row][column], 2)
                                    dpg.add_selectable(label=str(rounded_bpm), span_columns=True)
                                    dpg.bind_item_font(dpg.last_item(), "proggyvec-18")
                            case 5:
                                if table_matrix[row][column] is None:
                                    dpg.add_selectable(label="-", span_columns=True)
                                    dpg.bind_item_font(dpg.last_item(), "proggyvec-18")
                                else:
                                    rounded_loudness = round(table_matrix[row][column], 2)
                                    dpg.add_selectable(label=str(rounded_loudness), span_columns=True)
                                    dpg.bind_item_font(dpg.last_item(), "proggyvec-18")
                            case 6:
                                if table_matrix[row][column] is None:
                                    dpg.add_selectable(label="-", span_columns=True)
                                    dpg.bind_item_font(dpg.last_item(), "proggyvec-18")
                                else:
                                    dpg.add_selectable(label=str(table_matrix[row][column]), span_columns=True)
                                    dpg.bind_item_font(dpg.last_item(), "proggyvec-18")
                            case 7:
                                if table_matrix[row][column] is None:
                                    dpg.add_selectable(label="-", span_columns=True)
                                    dpg.bind_item_font(dpg.last_item(), "proggyvec-18")
                                else:
                                    pertcentage = (table_matrix[row][column] * 100)
                                    intified = int(pertcentage)
                                    dpg.add_selectable(label=str(intified), span_columns=True)
                                    dpg.bind_item_font(dpg.last_item(), "proggyvec-18")
                            case 8:
                                if table_matrix[row][column] is None:
                                    dpg.add_selectable(label="-", span_columns=True)
                                    dpg.bind_item_font(dpg.last_item(), "proggyvec-18")
                                else:
                                    dpg.add_selectable(label=str(table_matrix[row][column]), span_columns=True)
                                    dpg.bind_item_font(dpg.last_item(), "proggyvec-18")

                            


def init_collections_list():
    collections = collection_manager.get_collections()
    dpg.add_listbox(tag="Collections", parent="Collections Window",items=[c[1] for c in collections], width=-1, num_items=(viewport_height/20)-1, callback=get_selected_collection)
    dpg.bind_item_font(dpg.last_item(), "roboto-condensed-22")

    
def refresh_collections_list():

    dpg.delete_item("Collections")
    init_collections_list()

def analyze_callback():
    collection_name = dpg.get_value("Collections")
    tracks_info = collection_manager.get_tracks_by_collection_name(collection_name)
    collection_creator.analyze_tracks(tracks_info, collection_name)
    dpg.delete_item("Collections Info" ,children_only=True)
    get_collection_info(collection_name)
    InfoPane.refresh_info_pane("Done...")

def remove_callback():
    collection_name = dpg.get_value("Collections")
    InfoPane.refresh_info_pane("Removing..." + " " + collection_name)
    collection_info = collection_manager.get_collection_by_name(collection_name)
    collection_id = collection_info[0]
    track_ids = collection_manager.get_track_ids_by_collection_id(collection_id)
    for track_id in track_ids:
        print(track_id[0])
        track_manager.delete_track(track_id[0])
    collection_manager.remove_collection(collection_info)
    collection_manager.remove_collection_relations(collection_info)
    refresh_collections_list()
    InfoPane.refresh_info_pane("Done...") 

def print_me():
    print("STHING")

def initialize_gui_elements():
    with dpg.font_registry():
        dpg.add_font("..\\res\\fonts\RobotoCondensed-Regular.ttf", 22, tag="roboto-condensed-22")
        dpg.add_font("..\\res\\fonts\ProggyVector Regular.otf", 18, tag="proggyvec-18")
        dpg.add_font("..\\res\\fonts\RobotoCondensed-Bold.ttf", 36, tag="roboto-condensed-36")
    #Initialize Menu
    with dpg.menu_bar():
        with dpg.menu(label="File"):
            with dpg.menu(label="New"):
                dpg.add_menu_item(label="Collection from Folder", callback=lambda: dpg.show_item("file_dialog_id"))
                dpg.add_menu_item(label="Collection from Link", callback=collection_from_link)
            dpg.add_menu_item(label="Settings", callback=settings_window)
            dpg.add_menu_item(label="Exit", callback=dpg.stop_dearpygui)
        with dpg.menu(label="Collection"):
            dpg.add_menu_item(label="Analyze", callback=analyze_callback)
            dpg.add_menu_item(label="Delete", callback=remove_callback)
        dpg.add_menu_item(label="Help", callback=print_me)
    # Add collection button
    dpg.add_file_dialog(
    directory_selector=True, show=False, callback=callback, tag="file_dialog_id",
    cancel_callback=cancel_callback, width=700 ,height=400)
    dpg.bind_item_font(dpg.last_item(), "roboto-condensed-22")
    
    

    # Initialize group container for collections listbox and information pane
    with dpg.group(tag="Main Ver"):
        with dpg.group(horizontal=True, tag="button_group"):
            dpg.add_button(label='+',width=200, callback=lambda: dpg.show_item("file_dialog_id"))
            dpg.bind_item_font(dpg.last_item(), "roboto-condensed-22")
            dpg.add_spacer(width = 156)
            # Add image button
            dpg.add_image_button("texture_tag", callback=print_me, tag="image_button_id")
            InfoPane.refresh_info_pane("Ready...")

        with dpg.group(horizontal=True):
            with dpg.child_window(tag="Collections Window", border=False, width=400, no_scrollbar=True):
                # Adding collection List
                init_collections_list()
            with dpg.child_window(width=-1, border=False):
                with dpg.table(        
                    tag="Collections Info",  
                    borders_outerV=True,
                    borders_outerH=True,
                    borders_innerV=True,
                    borders_innerH=True,
                    scrollY=True,
                    freeze_rows=1,
                    resizable=True,
                    height=-1,
                    sortable=True,
                    callback=sort_callback) as table:
                    # Add some columns to the table
                    for column in info_columns:
                        dpg.add_table_column(label=column, width_stretch=True)
                        dpg.bind_item_font(dpg.last_item(), "proggyvec-18")
                default_selected = dpg.get_value("Collections")
                get_collection_info(default_selected)        


dpg.create_context()

#dpg.show_font_manager()

width, height, channels, data = dpg.load_image("..\\res\\images\\threedots.png")

with dpg.texture_registry():
    dpg.add_static_texture(width=width, height=height, default_value=data, tag="texture_tag")


dpg.create_viewport(title='Deck|Track')
viewport_width = dpg.get_viewport_client_width()
viewport_height = dpg.get_viewport_client_height()


with dpg.window(tag="Primary Window", height=viewport_height, no_scrollbar=True): 
    # Initialize Gui
    initialize_gui_elements()

dpg.set_primary_window("Primary Window", True)


image_button_pos = dpg.get_item_pos("image_button_id")

with dpg.popup("image_button_id", mousebutton=dpg.mvMouseButton_Left, tag="poptag") as pop:
    #dpg.add_button(label="Add", width=100, callback=lambda: dpg.show_item("file_dialog_id"))
    dpg.add_button(label="Analyze", width=100, callback=analyze_callback)
    dpg.add_button(label="Delete", width=100, callback=remove_callback)

    print(image_button_pos)
dpg.configure_item(pop, min_size=[100,50])


dpg.setup_dearpygui()
dpg.maximize_viewport()
dpg.show_viewport()


while dpg.is_dearpygui_running():
    sel_row = dpg.get_value("Collections")
    dpg.render_dearpygui_frame()
    new_row = dpg.get_value("Collections")
    if new_row != sel_row:
        get_collection_info(new_row)


dpg.start_dearpygui()

