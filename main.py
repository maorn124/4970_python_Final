import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QLineEdit, QListWidget, QInputDialog, QDialog


class TeamMemberEditorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Team Member Editor')
        layout = QVBoxLayout()

        self.member_list = QListWidget()
        layout.addWidget(self.member_list)

        self.add_button = QPushButton("Add Member")
        self.add_button.clicked.connect(self.add_member)
        layout.addWidget(self.add_button)

        self.update_button = QPushButton("Update Member")
        self.update_button.clicked.connect(self.update_member)
        layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Delete Member")
        self.delete_button.clicked.connect(self.delete_member)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)

    def add_member(self):
        member_name, ok = QInputDialog.getText(self, 'Add Member', 'Enter member name:')
        if ok and member_name:
            member_email, ok = QInputDialog.getText(self, 'Add Member', 'Enter member email:')
            if ok and member_email:
                self.member_list.addItem(f"{member_name} ({member_email})")

    def update_member(self):
        current_item = self.member_list.currentItem()
        if current_item:
            member_name, ok = QInputDialog.getText(self, 'Update Member', 'Enter new member name:', text=current_item.text().split()[0])
            if ok and member_name:
                member_email, ok = QInputDialog.getText(self, 'Update Member', 'Enter new member email:', text=current_item.text().split()[1][1:-1])
                if ok and member_email:
                    current_item.setText(f"{member_name} ({member_email})")

    def delete_member(self):
        current_item = self.member_list.currentItem()
        if current_item:
            self.member_list.takeItem(self.member_list.row(current_item))


class TeamEditorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Team Editor')
        layout = QVBoxLayout()

        self.team_list = QListWidget()
        layout.addWidget(self.team_list)

        self.add_button = QPushButton("Add Team")
        self.add_button.clicked.connect(self.add_team)
        layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Edit Team")
        self.edit_button.clicked.connect(self.edit_team)
        layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Delete Team")
        self.delete_button.clicked.connect(self.delete_team)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)

        self.team_member_editor_dialog = TeamMemberEditorDialog(self)

    def add_team(self):
        team_name, ok = QInputDialog.getText(self, 'Add Team', 'Enter team name:')
        if ok and team_name:
            self.team_list.addItem(team_name)

    def edit_team(self):
        current_item = self.team_list.currentItem()
        if current_item:
            new_team_name, ok = QInputDialog.getText(self, 'Edit Team', 'Enter new team name:', text=current_item.text())
            if ok and new_team_name:
                current_item.setText(new_team_name)

                # Open team member editor dialog
                self.team_member_editor_dialog.exec_()

    def delete_team(self):
        current_item = self.team_list.currentItem()
        if current_item:
            self.team_list.takeItem(self.team_list.row(current_item))


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Curling Manager')
        self.setGeometry(500, 250, 500, 500)  # x-position, y-position, width, height

        layout = QVBoxLayout()

        self.load_button = QPushButton("Load")
        self.load_button.clicked.connect(self.load_file)
        layout.addWidget(self.load_button)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_file)
        layout.addWidget(self.save_button)

        self.delete_league_button = QPushButton("Delete League")
        self.delete_league_button.clicked.connect(self.delete_league)
        layout.addWidget(self.delete_league_button)

        self.add_league_button = QPushButton("Add League")
        self.add_league_button.clicked.connect(self.add_league)
        layout.addWidget(self.add_league_button)

        self.edit_league_button = QPushButton("Edit League")
        self.edit_league_button.clicked.connect(self.edit_league)
        layout.addWidget(self.edit_league_button)

        self.league_name_input = QLineEdit()
        layout.addWidget(self.league_name_input)

        self.league_list = QListWidget()
        layout.addWidget(self.league_list)

        self.team_editor_dialog = TeamEditorDialog(self)

        self.setLayout(layout)

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open File', '.', 'Text Files (*.txt)')
        if file_path:
            with open(file_path, 'r') as file:
                data = file.read().splitlines()
                self.league_list.addItems(data)

    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save File', '.', 'Text Files (*.txt)')
        if file_path:
            with open(file_path, 'w') as file:
                for index in range(self.league_list.count()):
                    file.write(self.league_list.item(index).text() + '\n')

    def delete_league(self):
        selected_items = self.league_list.selectedItems()
        if selected_items:
            for item in selected_items:
                self.league_list.takeItem(self.league_list.row(item))
            QMessageBox.information(self, 'Delete League', 'League deleted.')
        else:
            QMessageBox.warning(self, 'Delete League', 'Please select a league to delete.')

    def add_league(self):
        league_name = self.league_name_input.text()
        if league_name:
            self.league_list.addItem(league_name)
            QMessageBox.information(self, 'Add League', f'League {league_name} added.')
        else:
            QMessageBox.warning(self, 'Add League', 'Please enter a league name.')

    def edit_league(self):
        selected_items = self.league_list.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            new_name, ok = QInputDialog.getText(self, 'Edit League', 'Enter new league name:', text=selected_item.text())
            if ok:
                selected_item.setText(new_name)
                QMessageBox.information(self, 'Edit League', 'League edited.')
                self.team_editor_dialog.exec_()  # Open the team editor dialog
        else:
            QMessageBox.warning(self, 'Edit League', 'Please select a league to edit.')

    def closeEvent(self, event):
        self.team_editor_dialog.close()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
