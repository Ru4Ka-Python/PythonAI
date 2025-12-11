"""Sidebar history widget."""

from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QPushButton, QLabel, QScrollArea,
    QWidget, QMenu, QInputDialog, QLineEdit
)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont


class HistorySidebar(QFrame):
    """Sidebar history widget."""
    
    item_clicked = pyqtSignal(str)  # Returns item ID
    item_renamed = pyqtSignal(str, str)  # ID, new name
    item_deleted = pyqtSignal(str)  # ID
    settings_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("historySidebar")
        self.setFixedWidth(260)
        self.current_mode = 0
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # History Section Title
        self.title_label = QLabel("HISTORY")
        self.title_label.setObjectName("sectionTitle")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)
        
        # Scroll Area for History Items
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background: transparent; border: none;")
        
        self.history_container = QWidget()
        self.history_layout = QVBoxLayout(self.history_container)
        self.history_layout.setContentsMargins(5, 5, 5, 5)
        self.history_layout.setSpacing(2)
        self.history_layout.addStretch()
        
        self.scroll_area.setWidget(self.history_container)
        layout.addWidget(self.scroll_area)
        
        # Settings Button at the Bottom
        self.settings_btn = QPushButton("⚙️ Settings")
        self.settings_btn.setObjectName("settingsButton")
        self.settings_btn.setCursor(Qt.PointingHandCursor)
        self.settings_btn.clicked.connect(self.settings_clicked.emit)
        layout.addWidget(self.settings_btn)
        
    def update_history(self, mode_name: str, items: list):
        """Update history items for the current mode.
        items: list of dicts {'id': str, 'name': str}
        """
        self.title_label.setText(f"{mode_name} HISTORY")
        
        # Clear existing items
        while self.history_layout.count() > 1:  # Keep the stretch
            item = self.history_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        # Add new items
        for item in items:
            btn = QPushButton(item['name'])
            btn.setObjectName("historyItem")
            btn.setCursor(Qt.PointingHandCursor)
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            
            # Context Menu
            btn.setContextMenuPolicy(Qt.CustomContextMenu)
            btn.customContextMenuRequested.connect(
                lambda pos, b=btn, i=item: self.show_context_menu(pos, b, i)
            )
            
            btn.clicked.connect(lambda checked, i=item: self.item_clicked.emit(i['id']))
            self.history_layout.insertWidget(self.history_layout.count() - 1, btn)
            
    def show_context_menu(self, pos, button, item):
        """Show context menu for history item."""
        menu = QMenu(self)
        rename_action = menu.addAction("Rename")
        delete_action = menu.addAction("Delete")
        
        action = menu.exec_(button.mapToGlobal(pos))
        
        if action == rename_action:
            new_name, ok = QInputDialog.getText(
                self, "Rename", "Enter new name:", 
                QLineEdit.Normal, item['name']
            )
            if ok and new_name:
                self.item_renamed.emit(item['id'], new_name)
                button.setText(new_name)
                
        elif action == delete_action:
            self.item_deleted.emit(item['id'])
