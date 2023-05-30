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

viewport_width = 1920
viewport_height = 1080

def print_me(sender):
    print(f"Menu Item: {sender}")

def refresh_info_pane(info):
    dpg.delete_item("Information Pane")
    dpg.add_text(info, tag="Information Pane", parent="Info Pane Window")


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
        refresh_info_pane("Analyzing..." + " " + dir)
        collection_creator.collection_from_folder(dir,True)
    else:
        refresh_info_pane("Scanning..." + " " + dir)
        collection_creator.collection_from_folder(dir,False)
    print(dir, analyze)
    refresh_collections_list()
    refresh_info_pane("Done...")
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
    #refresh_collections_list()

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
                        dpg.bind_item_font(dpg.last_item(), "proggyvec")

            
    #    for i in w:
    #        for j in h:
    #            dpg.add_table_column()
    #            dpg.add_text(tracks_info[j][info_
def init_collections_list():
    collections = collection_manager.get_collections()
    dpg.add_listbox(tag="Collections", parent="Collections Window",items=(collections), width=-1, num_items=100, callback=get_selected_collection)
    dpg.bind_item_font(dpg.last_item(), "roboto-condensed")

    
def refresh_collections_list():

    dpg.delete_item("Collections")
    init_collections_list()

def analyze_callback():
    collection = dpg.get_value("Collections")
    refresh_info_pane("Analyzing..." + " " + collection)
    tracks_info = collection_manager.get_tracks_by_collection_name(collection)
    collection_creator.analyze_tracks(tracks_info)
    dpg.delete_item("Collections Info" ,children_only=True)
    get_collection_info(collection)
    refresh_info_pane("Done...")

def remove_callback():
    collection_name = dpg.get_value("Collections")
    refresh_info_pane("Removing..." + " " + collection_name)
    collection_info = collection_manager.get_collection_by_name(collection_name)
    collection_id = collection_info[0]
    track_ids = collection_manager.get_track_ids_by_collection_id(collection_id)
    for track_id in track_ids:
        print(track_id[0])
        track_manager.delete_track(track_id[0])
    collection_manager.remove_collection(collection_info)
    collection_manager.remove_collection_relations(collection_info)
    refresh_collections_list()
    collection_name = dpg.get_value("Collections")
    get_collection_info(collection_name)
    refresh_info_pane("Done...") 

def print_me():
    print("STHING")

def initialize_gui_elements():
    with dpg.font_registry():
        robotofont = dpg.add_font("RobotoCondensed-Regular.ttf", 20, tag="roboto-condensed")
        progggyvec = dpg.add_font("ProggyVector Regular.otf", 16, tag="proggyvec")
    #Initialize Menu
    with dpg.menu_bar():
        with dpg.menu(label="File"):
            with dpg.menu(label="New"):
                dpg.add_menu_item(label="Collection from Folder", callback=lambda: dpg.show_item("file_dialog_id"))
            dpg.add_menu_item(label="Analyze", callback=analyze_callback)
            dpg.add_menu_item(label="Delete", callback=remove_callback)
            dpg.add_menu_item(label="Settings", callback=print_me)
            dpg.add_menu_item(label="Exit", callback=dpg.stop_dearpygui)
        dpg.add_menu_item(label="Help", callback=print_me)
    # Add collection button
    dpg.add_file_dialog(
    directory_selector=True, show=False, callback=callback, tag="file_dialog_id",
    cancel_callback=cancel_callback, width=700 ,height=400)
    dpg.bind_item_font(dpg.last_item(), "roboto-condensed")
    with dpg.group(horizontal=True, tag="button_group"):
        dpg.add_button(label='+',width=200, callback=lambda: dpg.show_item("file_dialog_id"))
        dpg.bind_item_font(dpg.last_item(), "roboto-condensed")
        dpg.add_spacer(width = 156)
        # Add image button
        dpg.add_image_button("texture_tag", callback=print_me, tag="image_button_id")
    # Initialize group container for collections listbox and information pane
    with dpg.group(horizontal=True):
        with dpg.child_window(tag="Collections Window", border=False, height=viewport_height*0.85, width=400):
            # Adding collection List
            init_collections_list()
        with dpg.child_window(width=-1, height=viewport_height*0.85, border=False):
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
                    dpg.bind_item_font(dpg.last_item(), "proggyvec")
            default_selected = dpg.get_value("Collections")
            get_collection_info(default_selected)
        # Create the Table
    with dpg.group():
        with dpg.child_window(parent="Primary Window",tag="Info Pane Window", width=-1, no_scrollbar=True, height=viewport_height*0.020, border=False):
            refresh_info_pane("Ready...")
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

#dpg.show_font_manager()

width, height, channels, data = dpg.load_image("threedots.png")

with dpg.texture_registry():
    dpg.add_static_texture(width=width, height=height, default_value=data, tag="texture_tag")


with dpg.window(tag="Primary Window", height=-1,no_scrollbar=True):
    # Initialize Gui
    initialize_gui_elements()

image_button_pos = dpg.get_item_pos("image_button_id")

with dpg.popup("image_button_id", mousebutton=dpg.mvMouseButton_Left, tag="poptag") as pop:
    #dpg.add_button(label="Add", width=100, callback=lambda: dpg.show_item("file_dialog_id"))
    dpg.add_button(label="Analyze", width=100, callback=analyze_callback)
    dpg.add_button(label="Delete", width=100, callback=remove_callback)

    print(image_button_pos)
dpg.configure_item(pop, min_size=[100,50])

dpg.set_primary_window("Primary Window", True)
dpg.create_viewport(title='Deck|Track')


viewport_width = dpg.get_viewport_client_width()
viewport_height = dpg.get_viewport_client_height()


dpg.setup_dearpygui()
dpg.maximize_viewport()
dpg.show_viewport()
dpg.start_dearpygui()

