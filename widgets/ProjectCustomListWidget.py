import PySide6.QtWidgets as QtWidgets
import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
from handlers.MiscHandlers import get_contrasting_color

import widgets.ProjectListWidget as ProjectListWidget


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