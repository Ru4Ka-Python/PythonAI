"""Feedback page."""

import webbrowser

from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTextEdit, QLineEdit, QComboBox, QGroupBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from .base_page import BasePage


class FeedbackPage(BasePage):
    """Page for submitting feedback."""
    
    FEEDBACK_TYPES = [
        "Bug Report",
        "Feature Request",
        "General Feedback",
        "Question",
        "Other"
    ]
    
    GITHUB_ISSUES_URL = "https://github.com/Ru4Ka-Python/PythonAI/issues/new"
    
    def __init__(self, parent=None):
        super().__init__(
            title="Feedback",
            subtitle="Help us improve RoleAI by sharing your feedback",
            parent=parent
        )
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        header = self.create_header()
        layout.addLayout(header)
        
        info_label = QLabel(
            "Your feedback helps us make RoleAI better. You can submit feedback "
            "directly through GitHub Issues or use the form below to compose your message."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #8a8a8a; font-size: 13px;")
        layout.addWidget(info_label)
        
        form_group = QGroupBox("Compose Feedback")
        form_layout = QVBoxLayout(form_group)
        form_layout.setSpacing(15)
        
        type_layout = QHBoxLayout()
        type_label = QLabel("Feedback Type:")
        type_label.setMinimumWidth(120)
        self.type_combo = QComboBox()
        self.type_combo.addItems(self.FEEDBACK_TYPES)
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_combo, 1)
        form_layout.addLayout(type_layout)
        
        subject_layout = QHBoxLayout()
        subject_label = QLabel("Subject:")
        subject_label.setMinimumWidth(120)
        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("Brief description of your feedback")
        subject_layout.addWidget(subject_label)
        subject_layout.addWidget(self.subject_input, 1)
        form_layout.addLayout(subject_layout)
        
        description_label = QLabel("Description:")
        form_layout.addWidget(description_label)
        
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText(
            "Please provide detailed information about your feedback...\n\n"
            "For bug reports, include:\n"
            "- Steps to reproduce\n"
            "- Expected behavior\n"
            "- Actual behavior\n"
            "- Screenshots (if applicable)"
        )
        self.description_input.setMinimumHeight(200)
        form_layout.addWidget(self.description_input)
        
        layout.addWidget(form_group, 1)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.github_button = QPushButton("Open GitHub Issues")
        self.github_button.setObjectName("primaryButton")
        self.github_button.setCursor(Qt.PointingHandCursor)
        self.github_button.clicked.connect(self.open_github_issues)
        button_layout.addWidget(self.github_button)
        
        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.setObjectName("secondaryButton")
        self.copy_button.setCursor(Qt.PointingHandCursor)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        button_layout.addWidget(self.copy_button)
        
        self.clear_button = QPushButton("Clear Form")
        self.clear_button.setObjectName("secondaryButton")
        self.clear_button.setCursor(Qt.PointingHandCursor)
        self.clear_button.clicked.connect(self.clear_form)
        button_layout.addWidget(self.clear_button)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #8a8a8a;")
        layout.addWidget(self.status_label)
        
        links_layout = QHBoxLayout()
        links_layout.setSpacing(20)
        
        github_link = QLabel('<a href="https://github.com/Ru4Ka-Python/PythonAI" style="color: #e94560;">GitHub Repository</a>')
        github_link.setOpenExternalLinks(True)
        links_layout.addWidget(github_link)
        
        links_layout.addStretch()
        layout.addLayout(links_layout)
    
    def compose_feedback(self) -> str:
        """Compose feedback text from form fields."""
        feedback_type = self.type_combo.currentText()
        subject = self.subject_input.text().strip()
        description = self.description_input.toPlainText().strip()
        
        lines = [
            f"**Type:** {feedback_type}",
            f"**Subject:** {subject}",
            "",
            "**Description:**",
            description,
            "",
            "---",
            "*Submitted via RoleAI Feedback Form*"
        ]
        
        return "\n".join(lines)
    
    def open_github_issues(self):
        """Open GitHub Issues in browser."""
        feedback_type = self.type_combo.currentText()
        subject = self.subject_input.text().strip()
        
        url = self.GITHUB_ISSUES_URL
        if subject:
            import urllib.parse
            title = urllib.parse.quote(f"[{feedback_type}] {subject}")
            body = urllib.parse.quote(self.compose_feedback())
            url = f"{self.GITHUB_ISSUES_URL}?title={title}&body={body}"
        
        webbrowser.open(url)
        self.status_label.setText("Opened GitHub Issues in browser")
    
    def copy_to_clipboard(self):
        """Copy feedback to clipboard."""
        from PyQt5.QtWidgets import QApplication
        
        feedback = self.compose_feedback()
        clipboard = QApplication.clipboard()
        clipboard.setText(feedback)
        
        self.status_label.setText("Feedback copied to clipboard!")
        self.show_info("Copied", "Feedback has been copied to clipboard.")
    
    def clear_form(self):
        """Clear the feedback form."""
        self.type_combo.setCurrentIndex(0)
        self.subject_input.clear()
        self.description_input.clear()
        self.status_label.setText("Form cleared")
