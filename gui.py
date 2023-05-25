import dearpygui.dearpygui as dpg
from track_manager import TrackManager
from collection_manager import CollectionManager
from collection_creator import CollectionCreator
from track import Track
from collection import Collection
import db


track_manager = TrackManager()  
collection_manager = CollectionManager()
collection_creator = CollectionCreator()

list_items= 55
info_columns = ["Title", "Artist", "Duration", "Key", "BPM", "Loudness", "Danceability", "Energy", "Quality"]

def print_me(sender):
    print(f"Menu Item: {sender}")

def get_selected_collection(sender, collection_name):
    #print(collection_name)
    get_collection_info(collection_name)

def get_collection_info(collection_name):
    dpg.delete_item("Collections Info" ,children_only=True)
    tracks_info = collection_manager.get_tracks_by_collection_name(collection_name)
    w = len(info_columns)
    h = len(tracks_info)
    table_matrix = [[0 for x in range(w)] for y in range(h)]
    
    for column in range(w):
             for row in range(h):
                table_matrix[row][column] = tracks_info[row][column]
    #print(table_matrix)
    update_table(w, h, table_matrix)

def callback(sender, app_data):
    print('OK was clicked.')
    print("Sender: ", sender)
    print("App Data: ", app_data)
    dir = app_data['file_path_name']
    collection_creator.collection_from_folder(dir,False)
    refresh_collections_list()

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
                        #print(row, column)
                        dpg.add_button(label= str(table_matrix[row][column]), width=-1)

            
    #    for i in w:
    #        for j in h:
    #            dpg.add_table_column()
    #            dpg.add_text(tracks_info[j][info_
def init_collections_list():
    collections = collection_manager.get_collections()
    dpg.add_listbox(tag="Collections", parent="Collections Window",items=(collections), width=-1, num_items=100, callback=get_selected_collection)
    
def refresh_collections_list():

    dpg.delete_item("Collections")
    init_collections_list()
     

def initialize_gui_elements():
    #Initialize Menu
    with dpg.menu_bar():
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="New", callback=print_me)
            dpg.add_menu_item(label="Save", callback=print_me)
            dpg.add_menu_item(label="Save As", callback=print_me)

            with dpg.menu(label="Settings"):
                dpg.add_menu_item(label="Setting 1", callback=print_me, check=True)
                dpg.add_menu_item(label="Setting 2", callback=print_me)
        dpg.add_menu_item(label="Help", callback=print_me)
    # Add collection button
    dpg.add_file_dialog(
    directory_selector=True, show=False, callback=callback, tag="file_dialog_id",
    cancel_callback=cancel_callback, width=700 ,height=400)
    dpg.add_button(label='+',width=200, callback=lambda: dpg.show_item("file_dialog_id"))
    # Initialize group container for collections listbox and information pane
    with dpg.group(horizontal=True):
        with dpg.child_window(tag="Collections Window", border=False, height=-1, width=400):
            # Adding collection List
            init_collections_list()
        with dpg.child_window(width=-1, height=-1, border=False):
            with dpg.table(        
                tag="Collections Info",  
                borders_outerV=True,
                borders_outerH=True,
                borders_innerV=True,
                borders_innerH=True,
                scrollY=True,
                freeze_rows=1,
                height=-1,) as table:
                # Add some columns to the table
                for column in info_columns:
                    dpg.add_table_column(label=column)
            default_selected = dpg.get_value("Collections")
            get_collection_info(default_selected)
        # Create the Table

"""         with dpg.table(
            borders_outerV=True,
            borders_outerH=True,
            borders_innerV=True,
            borders_innerH=True,
            scrollY=True,
            freeze_rows=1,
            height=-1,
        ):
                
                # Add some columns to the table
            for column in info_columns:
                dpg.add_table_column(label= column)
                
                # Add some rows to the table
            for i in range(0, 3):
                with dpg.table_row():
                    for j in range(0, 9):
                        dpg.add_text(f"Row{i} Column{j}") """

dpg.create_context()

with dpg.window(tag="Primary Window"):
    # Initialize Gui
    initialize_gui_elements()

dpg.set_primary_window("Primary Window", True)
dpg.create_viewport(title='Deck|Track')

viewport_width = dpg.get_viewport_client_width()
viewport_height = dpg.get_viewport_client_height()

dpg.setup_dearpygui()
dpg.maximize_viewport()
dpg.show_viewport()
dpg.start_dearpygui()

