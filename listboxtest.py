import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title='Custom Title', width=600, height=300)

with dpg.window(label="Example Window", height=300):
    dpg.add_button(label="test")
    dpg.add_input_text(default_value='test')

    with dpg.child_window(border=False, height=-1, width=-1):
        dpg.add_listbox([str(i) for i in range(100)], width=-1, num_items=100)

    dpg.add_button(label="test")
    dpg.add_button(label="test")
    dpg.add_input_text(default_value='test')
    dpg.add_input_text(default_value='test')


#dpg.set_primary_window("Example Window", True)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()