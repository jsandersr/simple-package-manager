import dearpygui.dearpygui as dpg
from enum import Enum

class Package(Enum):
    ARGPARSE = 1
    SPDLOG = 2
    CATCH2 = 3

packages_data = {
    Package.ARGPARSE: {"DisplayName": "p-ranav/argparse", "GitHubURL": "https://github.com/p-ranav/argparse.git"},
    Package.SPDLOG: {"DisplayName": "gabime/spdlog", "GitHubURL": "https://github.com/gabime/spdlog.git"},
    Package.CATCH2: {"DisplayName": "catchorg/Catch2", "GitHubURL": "https://github.com/catchorg/Catch2.git"}
}

class SolutionNameMissingException(Exception):
    def __init__(self, message="Solution name cannot be empty"):
        self.message = message
        super().__init__(self.message)


class PackageSelectorGUI:
    def __init__(self):
        self.selected_packages = set()
        self.solution_name = ""
        self.checkboxes = {}
        self.window_id = None  # Initialize window_id
        self.create_gui()


    def create_gui(self):
        # Create the window and get the ID
        self.window_id = dpg.add_window(label="Package Selector", no_scrollbar=True,
                                        menubar=False, no_resize=True, no_move=True)
        
        with dpg.window(id=self.window_id):

            # input text
            self.solution_name_id = dpg.add_input_text(hint="Enter Solution Name")

            # Checkbox group
            for package in Package:
                checkbox_id = dpg.add_checkbox(label=packages_data[package]['DisplayName'],
                                            callback=self.on_checkbox_checked, user_data=package)
                self.checkboxes[checkbox_id] = package

            # Button
            self.generate_button_id = dpg.add_button(label="Generate", callback=self.on_generate_clicked)

            dpg.set_item_callback(self.solution_name_id, self.on_solution_text_changed)
            dpg.set_item_user_data(self.solution_name_id, self.generate_button_id)

            # Disable until minimum config is setup.
            dpg.disable_item(self.generate_button_id)


    def on_checkbox_checked(self, sender, app_data, user_data):
        package = user_data
        if app_data:
            self.selected_packages.add(package)
        else:
            self.selected_packages.discard(package)


    def on_generate_clicked(self, sender, app_data, user_data):
        self.solution_name = dpg.get_value(self.solution_name_id)
        try:
            if not self.solution_name.strip():
                raise SolutionNameMissingException
        
        except SolutionNameMissingException as e:
            print(e)
        for package in self.selected_packages:
            data = packages_data[package]
            print(f"{data['DisplayName']}: {data['GitHubURL']}")


    def on_solution_text_changed(self, sender, app_data, user_data):
        self.solution_name = dpg.get_value(sender)
        if self.solution_name.strip():
            dpg.enable_item(user_data)
        else:
            dpg.disable_item(user_data)


def main():
    dpg.create_context()
    gui = PackageSelectorGUI()

    dpg.create_viewport(title='Package Selector', width=600, height=300)
    dpg.setup_dearpygui()

    if gui.window_id is not None:
        dpg.set_primary_window(gui.window_id, True)

    disabled_color = (0.50 * 255, 0.50 * 255, 0.50 * 255, 1.00 * 255)
    disabled_button_color = (45, 45, 48)
    disabled_button_hover_color = (45, 45, 48)
    disabled_button_active_color = (45, 45, 48)

    with dpg.theme() as disabled_theme:
        with dpg.theme_component(dpg.mvButton, enabled_state=False):
            dpg.add_theme_color(dpg.mvThemeCol_Text, disabled_color, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Button, disabled_button_color, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, disabled_button_hover_color, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, disabled_button_active_color, category=dpg.mvThemeCat_Core)

        dpg.bind_theme(disabled_theme)

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    main()
