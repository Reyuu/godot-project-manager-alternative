from PySide6 import QtWidgets


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