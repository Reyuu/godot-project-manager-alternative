import pathlib
import json
import re
import subprocess
import random
import MainWindow
import ProjectListWidget
import sys
import os
import shutil
import qdarktheme
from PySide6 import QtWidgets, QtCore, QtGui
from rich.pretty import pprint

##################
# Debug functions
##################
DEBUG = False
def print_debug(*args, **kwargs):
    if DEBUG:
        print("[DEBUG] ", end="")
        print(*args, **kwargs)

def pprint_debug(*args, **kwargs):
    if DEBUG:
        print("[DEBUG]:")
        pprint(*args, **kwargs)
##################


##################
# Utility functions
##################
def _parse_project_godot(s):
    main_regex = r"config\/name=\"(.*?)\""
    result = re.findall(main_regex, s)
    if len(result) > 0:
        return result[0]
    else:
        return "N/A"

def get_contrasting_color(color):
    color = color[1:]
    color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
    d = 0
    luminance = (0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2])/255
    if luminance > 0.5:
        d = 0
    else:
        d = 255
    return "#{0:02x}{1:02x}{2:02x}".format(d,d,d)
##################

##################
# Main data handler class
##################
class ProjectHandler:
    def __init__(self):
        self.categories = {}
        self.selected_categories = []
        #load config
        self._config = self.config_load(pathlib.Path("./config.json"))
        self.projects_dir = pathlib.Path(self._config["projectsDir"])
        #check if projects.json is not generated
        project_json_dir = pathlib.Path(self._config["saveProjectsDir"])
        self.project_data = {}
        if project_json_dir.exists():
            ##load json
            with open(project_json_dir, "r", encoding="utf-8") as f:
                self.project_data = json.loads(f.read())
            #load categories
            self.selected_categories = self.project_data["last_categories"]
            self.categories = self.project_data["definitions"]["categories"]
            missing_projects = set(self._get_valid_projects()) - set(list(self.project_data["projects"].keys()))
            for project in missing_projects:
                self.project_data["projects"].update({
                    project: {
                        "categories": [],
                        "favorite": False
                    }
                })
            self.save_projects_json()
        else:
            self.project_data = self.create_first_json(self._get_valid_projects())
        invalid_keys = []
        for key in self.project_data["projects"].keys():
            tmp_val = ""
            path = pathlib.Path(key)
            if path.exists():
                with open(key, "r", encoding="utf-8") as f:
                    tmp_val = _parse_project_godot(f.read())
                self.project_data["projects"][key].update({"name": tmp_val})
            else:
                invalid_keys += [key]
        #delete invalid keys - probably deleted from drive
        for key in invalid_keys:
            self.project_data["projects"].pop(key)
        pprint_debug(self.project_data)

    def _get_valid_projects(self):
        valid_projects = self.projects_dir.glob("*/project.godot")
        valid_projects = [str(project) for project in valid_projects]
        return valid_projects

    def config_load(self, path):
        data = ""
        with open(path, "r", encoding="utf-8") as f:
            data = f.read()
        return json.loads(data)

    def save_projects_json(self):
        self.project_data["definitions"]["categories"] = self.categories
        self.project_data["last_categories"] = self.selected_categories
        with open(self._config["saveProjectsDir"], "w", encoding="utf-8") as f:
            f.write(json.dumps(self.project_data, indent=4))

    def create_first_json(self, valid_projects):
        output_dict = {}
        for project in valid_projects:
            output_dict.update({
                project: {
                    "categories": [],
                    "favorite": False
                }
            })
        output_dict = {
            "last_categories": [],
            "definitions": {
                "categories": {},
            },
            "projects": output_dict
        }
        pprint_debug(output_dict)
        with open(self._config["saveProjectsDir"], "w", encoding="utf-8") as f:
            f.write(json.dumps(output_dict, indent=4))
        return output_dict

    def get_filtered_projects(self, categories):
        tmp_projects = {}
        if len(categories) == 0:
            return self.project_data["projects"]
        for key in self.project_data["projects"].keys():
            item = self.project_data["projects"][key]
            if not(set(categories) <= set(item["categories"])):
                continue
            tmp_projects.update({key: item})
        return tmp_projects
##################

##################
# Widgets and Dialogs definitions
##################
class ProjectCustomListWidget(QtWidgets.QWidget, ProjectListWidget.Ui_widgetMain):
    def __init__(self, key, name, categories, parent, tag_color="#710073", is_favorite=False):
        super(ProjectCustomListWidget, self).__init__()
        self.setupUi(self)

        self.is_favorite = is_favorite
        self.key = key

        self.projectNameLabel.setText(name)
 
        bold_font = QtGui.QFont()
        bold_font.setBold(True)
        for key in categories.keys():
            tmp_label = QtWidgets.QLabel(categories[key]["name"])
            tmp_label.setFont(bold_font)
            if key in parent.color_categories.keys():
                tag_color = parent.color_categories[key]
            tmp_label.setStyleSheet(
            "QLabel{"
            f"    background-color: {tag_color};"
            f"    color: {get_contrasting_color(tag_color)};"
            "    padding: 5px;"
            "    border-radius: 10px;"
            "}")
            tmp_label.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
            self.tagLayout.addWidget(tmp_label)
        icon = QtGui.QIcon()
        icon.addFile(u"icons/plus.svg", QtCore.QSize(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.plus_button = QtWidgets.QPushButton(icon, "")
        self.plus_button.setIconSize(QtCore.QSize(16, 16))
        self.plus_button.setFlat(True)
        self.tagLayout.addWidget(self.plus_button)
        self.tagLayout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        if self.is_favorite:
            icon = QtGui.QIcon()
            icon.addFile(u"icons/star-filled.svg", QtCore.QSize(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.favButton.setIcon(icon)

        #https://stackoverflow.com/questions/18994733/pyside-signals-slots-with-iterative-loops
        if parent:
            self.plus_button.pressed.connect(lambda: parent.handle_assign_category(self))
            self.favButton.pressed.connect(lambda: parent.handle_favorite_project(self))
        
        self.setStyle

class CategoryInputDialog(QtWidgets.QDialog):
    def __init__(self, parent, categories, selected_categories):
        super(CategoryInputDialog, self).__init__(parent)
        self.setWindowTitle("Choose a category")
        submit_buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel

        self.button_box = QtWidgets.QDialogButtonBox(submit_buttons)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.cattegory_listview = QtWidgets.QListWidget()
        for category in categories.keys():
            tmp_list_item = QtWidgets.QListWidgetItem(categories[category]["name"])
            tmp_list_item.setData(QtCore.Qt.UserRole, category)
            tmp_list_item.setCheckState(QtCore.Qt.CheckState.Checked)
            if category in selected_categories:
                tmp_list_item.setCheckState(QtCore.Qt.CheckState.Checked)
            else:
                tmp_list_item.setCheckState(QtCore.Qt.CheckState.Unchecked)
            self.cattegory_listview.addItem(tmp_list_item)
        self.main_layout.addWidget(self.cattegory_listview)
        self.main_layout.addWidget(self.button_box)
        self.setLayout(self.main_layout)

    def get_selected(self):
        selected = []
        for i in range(self.cattegory_listview.count()):
            if self.cattegory_listview.item(i).checkState() == QtCore.Qt.CheckState.Checked:
                selected += [self.cattegory_listview.item(i).data(QtCore.Qt.UserRole)]
        return selected

class CategoryEditDialog(QtWidgets.QDialog):
    def __init__(self, current_state = None):
        super(CategoryEditDialog, self).__init__()
        if current_state:
            self.setWindowTitle("Edit a category")
        else:
            self.setWindowTitle("Create a new category")

        self.main_layout = QtWidgets.QFormLayout()

        id_label = QtWidgets.QLabel("Unique ID")
        self.id_line_edit = QtWidgets.QLineEdit()

        name_label = QtWidgets.QLabel("Name")
        self.name_line_edit = QtWidgets.QLineEdit()

        description_label = QtWidgets.QLabel("Description")
        self.description_text_edit = QtWidgets.QTextEdit()

        if current_state:
            key = list(current_state.keys())[0]
            self.id_line_edit.setText(key)
            self.name_line_edit.setText(current_state[key]["name"])
            self.description_text_edit.setText(current_state[key]["description"])
        else:
            rand_string = [chr(random.randint(97, 122)) for _ in range(0, 12)]
            rand_string2 = [chr(random.randint(48, 57)) for _ in range(0, 12)]
            rand_string = "_".join(["".join(rand_string), "".join(rand_string2)])
            self.id_line_edit.setText(rand_string)

        submit_buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        self.button_box = QtWidgets.QDialogButtonBox(submit_buttons)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.main_layout.addWidget(id_label)
        self.main_layout.addWidget(self.id_line_edit)
        self.main_layout.addWidget(name_label)
        self.main_layout.addWidget(self.name_line_edit)
        self.main_layout.addWidget(description_label)
        self.main_layout.addWidget(self.description_text_edit)
        self.main_layout.addWidget(self.button_box)

        self.setLayout(self.main_layout)

    def get_values(self):
        return {
            self.id_line_edit.text(): {
                "name": self.name_line_edit.text(),
                "description": self.description_text_edit.toPlainText()
            }
        }

class NewProjectFromTemplate(QtWidgets.QDialog):
    def __init__(self):
        super(NewProjectFromTemplate, self).__init__()
        self.setWindowTitle("New project from template")
        submit_buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel

        self.button_box = QtWidgets.QDialogButtonBox(submit_buttons)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.main_layout = QtWidgets.QFormLayout()

        explanation_label = QtWidgets.QLabel("Create a new project from a template in a projects directory.")

        templates_label = QtWidgets.QLabel("Template")
        self.templates_combobox = QtWidgets.QComboBox()
        for p in pathlib.Path("./templates").glob("*"):
            self.templates_combobox.addItem(str(p), userData=p)

        name_label = QtWidgets.QLabel("Projct name")
        self.name_line_edit = QtWidgets.QLineEdit("")

        self.main_layout.addWidget(explanation_label)
        self.main_layout.addWidget(templates_label)
        self.main_layout.addWidget(self.templates_combobox)
        self.main_layout.addWidget(name_label)
        self.main_layout.addWidget(self.name_line_edit)
        self.main_layout.addWidget(self.button_box)
        self.setLayout(self.main_layout)

    def get_values(self):
        return {
            "chosen_template": self.templates_combobox.currentData(),
            "project_name": self.name_line_edit.text()
        }

class RenameProjectDialog(QtWidgets.QDialog):
    def __init__(self, current_name):
        super(RenameProjectDialog, self).__init__()
        self.setWindowTitle("Rename selected project")

        submit_buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel

        self.button_box = QtWidgets.QDialogButtonBox(submit_buttons)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.main_layout = QtWidgets.QFormLayout()

        project_name_label = QtWidgets.QLabel("Project name")
        self.project_name_line_edit = QtWidgets.QLineEdit(current_name)

        self.main_layout.addWidget(project_name_label)
        self.main_layout.addWidget(self.project_name_line_edit)
        self.main_layout.addWidget(self.button_box)

        self.setLayout(self.main_layout)

    def get_value(self):
        return self.project_name_line_edit.text()
##################

##################
# Main application class
##################
class MainAppWindow(QtWidgets.QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self):
        super(MainAppWindow, self).__init__()
        self.setupUi(self)

        self.setWindowTitle("GBPM")

        self.ph = ProjectHandler()
        self.color_categories = self.generate_colors()

        self.fill_categories()

        for i in range(self.categoriesListView.count()):
            print_debug(f"{self.categoriesListView.item(i).data(QtCore.Qt.UserRole)} in {self.ph.selected_categories} = " +
                        f"{self.categoriesListView.item(i).data(QtCore.Qt.UserRole) in self.ph.selected_categories}")
            if self.categoriesListView.item(i).data(QtCore.Qt.UserRole) in self.ph.selected_categories:
                self.categoriesListView.item(i).setCheckState(QtCore.Qt.CheckState.Checked)
        self.fill_projects(self.ph.get_filtered_projects(self.ph.selected_categories))

        # connect events
        self.categoriesListView.itemChanged.connect(self.handle_categories)
        self.projectsListView.itemDoubleClicked.connect(self.handle_projects)

        self.addCategoryButton.pressed.connect(self.handle_adding_category)
        self.removeCategoryButton.pressed.connect(self.handle_removing_category)
        self.renameCategoryButton.pressed.connect(self.handle_renaming_category)

        self.actionNew_from_template.triggered.connect(self.handle_new_project_from_template)
        self.actionRename_selected_project.triggered.connect(self.handle_rename_project)
        self.actionRemove_selected_project.triggered.connect(self.handle_remove_project)
        self.actionExit.triggered.connect(self.close)

    def generate_colors(self):
        tmp_colors = {}
        i = 0
        for category in self.ph.project_data["definitions"]["categories"]:
            tmp_colors.update({category: self.ph._config["colorPresets"][i%len(self.ph._config["colorPresets"])]})
            i += 1
        return tmp_colors

    def closeEvent(self, event):
        self.ph.save_projects_json()

    def fill_projects(self, data):
        self.projectsListView.clear()
        last_favorite_inserted_index = 0
        current_index = 0
        for key in data.keys():
            project_name = data[key]["name"]
            categories = data[key]["categories"]
            is_favorite = data[key]["favorite"]
            categories_dict = {}
            for category in categories:
                categories_dict.update({category: self.ph.categories[category]})
            tmp_custom_item = ProjectCustomListWidget(key, project_name, categories_dict, parent=self, is_favorite=is_favorite)
            tmp_list_item = QtWidgets.QListWidgetItem()
            tmp_list_item.setData(QtCore.Qt.UserRole, key)
            tmp_list_item.setSizeHint(tmp_custom_item.sizeHint())
            if is_favorite:
                self.projectsListView.insertItem(last_favorite_inserted_index, tmp_list_item)
                last_favorite_inserted_index = last_favorite_inserted_index + 1
            else:
                self.projectsListView.insertItem(current_index, tmp_list_item)
            self.projectsListView.setItemWidget(tmp_list_item, tmp_custom_item)
            current_index += 1

    def fill_categories(self, preserve_checks = False):
        if preserve_checks:
            previously_checked = self.get_enabled_categories()
        self.categoriesListView.clear()
        for key in self.ph.categories.keys():
            tmp_item = QtWidgets.QListWidgetItem()
            tmp_item.setText(self.ph.categories[key]["name"])
            tmp_item.setCheckState(QtCore.Qt.CheckState.Checked)
            if preserve_checks:
                if key in previously_checked:
                    tmp_item.setCheckState(QtCore.Qt.CheckState.Checked)
                else:
                    tmp_item.setCheckState(QtCore.Qt.CheckState.Unchecked)
            else:
                tmp_item.setCheckState(QtCore.Qt.CheckState.Unchecked)
            tmp_item.setData(QtCore.Qt.UserRole, key)
            self.categoriesListView.addItem(tmp_item)

    def get_enabled_categories(self):
        enabled_categories = []
        for i in range(self.categoriesListView.count()):
            if self.categoriesListView.item(i).checkState() == QtCore.Qt.CheckState.Checked:
                enabled_categories += [self.categoriesListView.item(i).data(QtCore.Qt.UserRole)]
        return enabled_categories

    def reload_all(self):
        self.ph = ProjectHandler()
        self.color_categories = self.generate_colors()
        self.fill_categories()
        self.fill_projects(self.ph.get_filtered_projects(self.ph.selected_categories))

    ####################
    # Handler functions
    ####################

    def handle_projects(self, item):
        if item:
            print_debug(f"{item.text()} {item.data(QtCore.Qt.UserRole)}")
        if os.name == "nt":
            subprocess.Popen([self.ph._config["godotLocation"], item.data(QtCore.Qt.UserRole)], creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
        if os.name == "posix":
            subprocess.Popen([self.ph._config["godotLocation"], item.data(QtCore.Qt.UserRole)], preexec_fn=os.setpgrp)
        else:
            #have fun with launcher that hangs lol
            subprocess.Popen([self.ph._config["godotLocation"], item.data(QtCore.Qt.UserRole)])

    def handle_categories(self, item):
        if item:
            print_debug(f"{item.text()} {item.data(QtCore.Qt.UserRole)}")
        enabled_categories = self.get_enabled_categories()
        self.ph.selected_categories = enabled_categories
        self.fill_projects(self.ph.get_filtered_projects(enabled_categories))

    def handle_assign_category(self, parent):
        categories = {}
        for key in self.ph.categories:
            categories.update({key: self.ph.project_data["definitions"]["categories"][key]["name"]})
        dlg = CategoryInputDialog(None, self.ph.categories, self.ph.project_data["projects"][parent.key]["categories"])
        if dlg.exec():
            print_debug(dlg.get_selected())
            self.ph.project_data["projects"][parent.key]["categories"] = dlg.get_selected()
            self.handle_categories(None)

    def handle_favorite_project(self, parent):
        self.ph.project_data["projects"][parent.key]["favorite"] = not(parent.is_favorite)
        self.fill_projects(self.ph.get_filtered_projects(self.ph.selected_categories))
        self.ph.save_projects_json()

    def handle_adding_category(self):
        dlg = CategoryEditDialog()
        if dlg.exec():
            pprint_debug(dlg.get_values())
            data_from_dialog = dlg.get_values()
            if len(list(data_from_dialog.values())[0]["name"]) == 0:
                QtWidgets.QMessageBox.critical(self, "Category name empty", "The category name is empty.")
                return
            key = list(data_from_dialog.keys())[0]
            if (key in self.ph.project_data["definitions"]["categories"]):
                exisiting_category_name = self.ph.project_data["definitions"]["categories"][key]["name"]
                QtWidgets.QMessageBox.critical(self, "ID is not unique", f"ID \"{key}\" is already in use by \"{exisiting_category_name}\" category.")
                return
            self.ph.project_data["definitions"]["categories"].update(dlg.get_values())
            self.color_categories = self.generate_colors()
            self.fill_categories(preserve_checks=True)
        self.ph.save_projects_json()

    def handle_renaming_category(self):
        try:
            selected_item = list(self.categoriesListView.selectedItems())[0]
        except IndexError:
            return
        selected_item_data = selected_item.data(QtCore.Qt.UserRole)
        dlg = CategoryEditDialog(current_state={selected_item_data: self.ph.project_data["definitions"]["categories"][selected_item_data]})
        if dlg.exec():
            pprint_debug(dlg.get_values())
            data_from_dialog = dlg.get_values()
            key = list(data_from_dialog.keys())[0]
            self.ph.project_data["definitions"]["categories"].update(dlg.get_values())
            self.fill_categories(preserve_checks=True)
        self.ph.save_projects_json()

    def handle_removing_category(self):
        try:
            selected_item = list(self.categoriesListView.selectedItems())[0]
        except IndexError:
            return
        selected_item_data = selected_item.data(QtCore.Qt.UserRole)
        self.ph.project_data["definitions"]["categories"].pop(selected_item_data)
        if selected_item_data in self.ph.selected_categories:
            self.ph.selected_categories.remove(selected_item_data)
        for key in self.ph.project_data["projects"].keys():
            if selected_item_data in self.ph.project_data["projects"][key]["categories"]:
                self.ph.project_data["projects"][key]["categories"].remove(selected_item_data)
        self.fill_categories(preserve_checks=True)
        self.fill_projects(self.ph.get_filtered_projects(self.ph.selected_categories))
        self.ph.save_projects_json()

    def handle_new_project_from_template(self):
        dlg = NewProjectFromTemplate()
        if dlg.exec():
            values = dlg.get_values()
            if len(values["project_name"]) == 0:
                QtWidgets.QMessageBox.critical(self, "Empty project name", "The project name is empty.")
                return
            filename = values["project_name"].replace(" ", "_")
            path_to = self.ph.projects_dir / filename
            if path_to.exists():
                QtWidgets.QMessageBox.critical(self, "Path already in use", f"The path \"{str(path_to)}\" already exists. Please change the project name.")
                return
            #path_to.mkdir()
            path_from = values["chosen_template"]
            shutil.copytree(path_from, path_to)
            project_godot = ""
            with open(path_to / "project.godot", "r", encoding="utf-8") as f:
                project_godot = f.read()
            project_godot = re.sub(r"config\/name=\"(.*?)\"", f"config/name=\"{values['project_name']}\"", project_godot)
            with open(path_to / "project.godot", "w", encoding="utf-8") as f:
                f.write(project_godot)

            #Reload all.
            self.reload_all()

    def handle_rename_project(self):
        try:
            selected_item = self.projectsListView.selectedItems()[0]
        except IndexError:
            return
        selected_item_data = selected_item.data(QtCore.Qt.UserRole)
        current_name = self.ph.project_data["projects"][selected_item_data]["name"]
        dlg = RenameProjectDialog(current_name)
        if dlg.exec():
            value = dlg.get_value()
            if len(value) == 0:
                QtWidgets.QMessageBox.critical(self, "Project name empty", "The project name is empty. Cannot rename to empty string.")
                return
            path_to = pathlib.Path(selected_item_data)
            with open(path_to, "r", encoding="utf-8") as f:
                project_godot = f.read()
            project_godot = re.sub(r"config\/name=\"(.*?)\"", f"config/name=\"{value}\"", project_godot)
            with open(path_to, "w", encoding="utf-8") as f:
                f.write(project_godot)

            self.reload_all()

    def handle_remove_project(self):
        dlg = QtWidgets.QMessageBox()
        dlg.setWindowTitle("Remove project")
        dlg.setText("This will remove the project <span style=\"color: red\"><b>pernamently<b></span>.<br />Are you sure?")
        dlg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        dlg.setIcon(QtWidgets.QMessageBox.Warning)
        if dlg.exec() == QtWidgets.QMessageBox.Yes:
            try:
                selected_item = self.projectsListView.selectedItems()[0]
            except IndexError:
                return
            selected_item_data = selected_item.data(QtCore.Qt.UserRole)
            selected_item_data = pathlib.Path(selected_item_data)
            selected_item_data = selected_item_data.parent
            shutil.rmtree(selected_item_data)

            self.reload_all()
##################

if __name__ == "__main__":
    DEBUG = False
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet())
    window = MainAppWindow()
    window.show()
    app.exec()
