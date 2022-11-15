import pathlib
import PySide6.QtWidgets as QtWidgets


class NewProjectFromTemplateDialog(QtWidgets.QDialog):
    def __init__(self):
        super(NewProjectFromTemplateDialog, self).__init__()
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

        name_label = QtWidgets.QLabel("Project name")
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