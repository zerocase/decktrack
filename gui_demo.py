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

def print_selected(sender, collection_name):
    track_list = collection_manager.get_tracks_by_collection_name(collection_name)
    print(track_list)



dpg.create_context()
with dpg.window(tag="Primary Window"):

    with dpg.menu_bar():
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="New", callback=print_me)
            dpg.add_menu_item(label="Save", callback=print_me)
            dpg.add_menu_item(label="Save As", callback=print_me)

            with dpg.menu(label="Settings"):
                dpg.add_menu_item(label="Setting 1", callback=print_me, check=True)
                dpg.add_menu_item(label="Setting 2", callback=print_me)
        dpg.add_menu_item(label="Help", callback=print_me)
    # Create a horizontal layout to hold the ListBox and Table
    dpg.add_button(label='+', callback=print_me, width=200)
    with dpg.group(horizontal=True):
            # Create the ListBox
        #with dpg.group(label='Collections'):
        #    dpg.add_button(label='+', callback=print_me, width=200)
        #    collection_list = dpg.add_listbox(items=(collection_manager.get_collections()),num_items=list_items, width=400, callback=print_selected)

        with dpg.child_window(border=False, height=-1, width=400):
            dpg.add_listbox(items=(collection_manager.get_collections()), width=-1, num_items=100, callback=print_selected)

        
        # Create the Table
        with dpg.table(
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
                        dpg.add_text(f"Row{i} Column{j}")

dpg.set_primary_window("Primary Window", True)
dpg.create_viewport(title='Deck|Track')

viewport_width = dpg.get_viewport_client_width()
viewport_height = dpg.get_viewport_client_height()

dpg.setup_dearpygui()
dpg.maximize_viewport()
dpg.show_viewport()
dpg.start_dearpygui()

