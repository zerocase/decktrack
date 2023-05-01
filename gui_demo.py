import dearpygui.dearpygui as dpg

dpg.create_context()

with dpg.window(tag="Primary Window"):
    with dpg.table(header_row=False, resizable=True, policy=dpg.mvTable_SizingStretchProp,
                   borders_outerH=True, borders_innerV=True, borders_innerH=True, borders_outerV=True):

        dpg.add_table_column(label="Header 1")
        dpg.add_table_column(label="Header 2")
        dpg.add_table_column(label="Header 3")

        # once it reaches the end of the columns
        for i in range(0, 4):
            with dpg.table_row():
                for j in range(0, 3):
                    with dpg.table_cell():
                        dpg.add_text(label=f"Row{i} Column{j} a")
                        dpg.add_text(label=f"Row{i} Column{j} b")

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()