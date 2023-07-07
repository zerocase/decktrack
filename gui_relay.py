import dearpygui.dearpygui as dpg



class InfoPane:
    def refresh_info_pane(self):
        dpg.delete_item("Info Pane Window")
        with dpg.child_window(parent="button_group",tag="Info Pane Window", width=-1, height=23, border=False):
            dpg.add_text(self, tag="Information Pane")
        #with dpg.group(horizontal=True, tag="Pane Group"):
            #collection = dpg.get_value("Collections")
            #dpg.add_text("thing", tag="collinfo", parent="Info Pane Window")