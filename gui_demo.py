import dearpygui.dearpygui as dpg

def print_me(sender):
    print(f"Menu Item: {sender}")

dpg.create_context()

with dpg.window(tag="Primary Window"):
    
    # Create a horizontal layout to hold the ListBox and Table
    with dpg.group(horizontal=True):

        # Create the ListBox
        dpg.add_listbox(items=(["Item 1", "Item 2", "Item 3"]), width=400)
        # Create the Table
        with dpg.table():
            
            # Add some columns to the table
            for i in range(0, 9):
                dpg.add_table_column(label="Thing")
            
            # Add some rows to the table
            for i in range(0, 3):
                with dpg.table_row():
                    for j in range(0, 9):
                        dpg.add_text(f"Row{i} Column{j}")

dpg.set_primary_window("Primary Window", True)
dpg.create_viewport(title='Deck|Track', width=1536, height=864)
dpg.setup_dearpygui()
dpg.maximize_viewport()
dpg.show_viewport()
dpg.start_dearpygui()
