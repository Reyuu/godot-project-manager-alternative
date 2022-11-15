import random
import PySide6.QtWidgets as QtWidgets

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