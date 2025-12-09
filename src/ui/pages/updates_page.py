"""Updates checker page."""

import webbrowser

from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QGroupBox, QProgressBar, QFrame
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

import requests

from .base_page import BasePage
from ...config import APP_VERSION, GITHUB_REPO_URL


class UpdateCheckerWorker(QThread):
    """Worker thread for checking updates."""
    
    update_found = pyqtSignal(str, str, str)
    no_update = pyqtSignal()
    error_occurred = pyqtSignal(str)
    
    def run(self):
        """Check for updates."""
        try:
            response = requests.get(GITHUB_REPO_URL, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                latest_version = data.get("tag_name", "")
                release_notes = data.get("body", "No release notes available.")
                download_url = data.get("html_url", "")
                
                current_clean = APP_VERSION.replace("-", "").replace("beta", "").replace("alpha", "")
                latest_clean = latest_version.replace("-", "").replace("Beta", "").replace("Alpha", "").replace("v", "")
                
                if latest_clean > current_clean:
                    self.update_found.emit(latest_version, release_notes, download_url)
                else:
                    self.no_update.emit()
            else:
                self.error_occurred.emit(f"HTTP Error: {response.status_code}")
                
        except requests.exceptions.Timeout:
            self.error_occurred.emit("Connection timed out. Please check your internet connection.")
        except requests.exceptions.RequestException as e:
            self.error_occurred.emit(f"Network error: {str(e)}")
        except Exception as e:
            self.error_occurred.emit(f"Error checking for updates: {str(e)}")


class UpdatesPage(BasePage):
    """Page for checking application updates."""
    
    RELEASES_URL = "https://github.com/Ru4Ka-Python/PythonAI/releases"
    
    def __init__(self, parent=None):
        super().__init__(
            title="Check for Updates",
            subtitle="Keep RoleAI up to date",
            parent=parent
        )
        self.update_worker = None
        self.download_url = ""
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        header = self.create_header()
        layout.addLayout(header)
        
        version_frame = QFrame()
        version_frame.setStyleSheet("""
            QFrame {
                background-color: #16213e;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        version_layout = QVBoxLayout(version_frame)
        version_layout.setSpacing(10)
        
        current_label = QLabel("Current Version")
        current_label.setFont(QFont("Segoe UI", 12))
        current_label.setStyleSheet("color: #8a8a8a;")
        version_layout.addWidget(current_label)
        
        version_value = QLabel(APP_VERSION)
        version_value.setFont(QFont("Segoe UI", 28, QFont.Bold))
        version_value.setStyleSheet("color: #e94560;")
        version_layout.addWidget(version_value)
        
        layout.addWidget(version_frame)
        
        self.check_button = QPushButton("Check for Updates")
        self.check_button.setObjectName("primaryButton")
        self.check_button.setCursor(Qt.PointingHandCursor)
        self.check_button.clicked.connect(self.check_updates)
        layout.addWidget(self.check_button)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.result_group = QGroupBox("Update Status")
        result_layout = QVBoxLayout(self.result_group)
        result_layout.setSpacing(15)
        
        self.status_icon = QLabel("🔄")
        self.status_icon.setFont(QFont("Segoe UI", 48))
        self.status_icon.setAlignment(Qt.AlignCenter)
        result_layout.addWidget(self.status_icon)
        
        self.status_text = QLabel("Click 'Check for Updates' to see if a new version is available.")
        self.status_text.setWordWrap(True)
        self.status_text.setAlignment(Qt.AlignCenter)
        self.status_text.setFont(QFont("Segoe UI", 12))
        result_layout.addWidget(self.status_text)
        
        self.release_notes = QLabel("")
        self.release_notes.setWordWrap(True)
        self.release_notes.setStyleSheet("color: #8a8a8a; font-size: 11px;")
        self.release_notes.setAlignment(Qt.AlignCenter)
        self.release_notes.setVisible(False)
        result_layout.addWidget(self.release_notes)
        
        self.download_button = QPushButton("Download Update")
        self.download_button.setObjectName("primaryButton")
        self.download_button.setCursor(Qt.PointingHandCursor)
        self.download_button.clicked.connect(self.download_update)
        self.download_button.setVisible(False)
        result_layout.addWidget(self.download_button)
        
        layout.addWidget(self.result_group, 1)
        
        links_layout = QHBoxLayout()
        
        releases_link = QLabel(f'<a href="{self.RELEASES_URL}" style="color: #e94560;">View All Releases</a>')
        releases_link.setOpenExternalLinks(True)
        links_layout.addWidget(releases_link)
        
        links_layout.addStretch()
        
        changelog_label = QLabel('<a href="https://github.com/Ru4Ka-Python/PythonAI/blob/main/CHANGELOG.md" style="color: #e94560;">Changelog</a>')
        changelog_label.setOpenExternalLinks(True)
        links_layout.addWidget(changelog_label)
        
        layout.addLayout(links_layout)
    
    def check_updates(self):
        """Start checking for updates."""
        self.check_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.status_icon.setText("🔄")
        self.status_text.setText("Checking for updates...")
        self.release_notes.setVisible(False)
        self.download_button.setVisible(False)
        
        self.update_worker = UpdateCheckerWorker()
        self.update_worker.update_found.connect(self.on_update_found)
        self.update_worker.no_update.connect(self.on_no_update)
        self.update_worker.error_occurred.connect(self.on_error)
        self.update_worker.start()
    
    def on_update_found(self, version: str, notes: str, url: str):
        """Handle update found."""
        self.check_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        self.status_icon.setText("🎉")
        self.status_text.setText(f"New version available: {version}")
        
        if notes:
            truncated_notes = notes[:500] + "..." if len(notes) > 500 else notes
            self.release_notes.setText(f"Release Notes:\n{truncated_notes}")
            self.release_notes.setVisible(True)
        
        self.download_url = url
        self.download_button.setVisible(True)
    
    def on_no_update(self):
        """Handle no update available."""
        self.check_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        self.status_icon.setText("✅")
        self.status_text.setText("You're running the latest version!")
    
    def on_error(self, error_message: str):
        """Handle error."""
        self.check_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        self.status_icon.setText("❌")
        self.status_text.setText(f"Error: {error_message}")
    
    def download_update(self):
        """Open download page in browser."""
        if self.download_url:
            webbrowser.open(self.download_url)
        else:
            webbrowser.open(self.RELEASES_URL)
