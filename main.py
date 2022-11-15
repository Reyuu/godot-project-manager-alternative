import pathlib
import json
import re
import subprocess
import random
import sys
import os
import shutil
import qdarktheme
#from PySide6 import QtWidgets, QtCore, QtGui
import PySide6.QtWidgets as QtWidgets
import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
from rich.pretty import pprint

import widgets.MainWindow as MainWindow
import widgets.ProjectListWidget as ProjectListWidget
from handlers.DebugHandlers import (print_debug, pprint_debug)
from handlers.ProjectHandler import ProjectHandler
from widgets.ProjectCustomListWidget import ProjectCustomListWidget
from dialogs.CategoryEditDialog import CategoryEditDialog
from dialogs.CategoryInputDialog import CategoryInputDialog
from dialogs.NewProjectFromTemplateDialog import NewProjectFromTemplateDialog
from dialogs.RenameProjectDialog import RenameProjectDialog


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
        placeholder_qpixmap = QtGui.QPixmap("icons/godot.png")
        for key in data.keys():
            project_name = data[key]["name"]
            categories = data[key]["categories"]
            is_favorite = data[key]["favorite"]
            icon_path = data[key]["icon"]
            categories_dict = {}
            for category in categories:
                categories_dict.update({category: self.ph.categories[category]})
            tmp_custom_item = ProjectCustomListWidget(key, project_name, categories_dict, parent=self, is_favorite=is_favorite)
            tmp_custom_item.icon.setFixedSize(tmp_custom_item.icon.maximumWidth(), tmp_custom_item.icon.maximumHeight())
            if icon_path:
                tmp_img = QtGui.QPixmap(icon_path)
                tmp_custom_item.icon.setPixmap(tmp_img.scaled(tmp_custom_item.icon.maximumWidth(), tmp_custom_item.icon.maximumHeight(), QtCore.Qt.KeepAspectRatio))
            else:
                tmp_custom_item.icon.setPixmap(placeholder_qpixmap.scaled(tmp_custom_item.icon.maximumWidth(), tmp_custom_item.icon.maximumHeight(), QtCore.Qt.KeepAspectRatio))
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


    def handle_projects(self, item):
        if item:
            print_debug(f"{item.text()} {item.data(QtCore.Qt.UserRole)}")
        if os.name == "nt":
            subprocess.Popen([self.ph._config["godotLocation"], item.data(QtCore.Qt.UserRole)], creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
        elif os.name == "posix":
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
        dlg = NewProjectFromTemplateDialog()
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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet())
    window = MainAppWindow()
    window.show()
    app.exec()
