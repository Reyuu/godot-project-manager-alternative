import PySide6.QtCore as QtCore
import PySide6.QtWidgets as QtWidgets


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
