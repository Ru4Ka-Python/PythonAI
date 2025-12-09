"""Stylesheet definitions for RoleAI application."""


class StyleSheet:
    """Application stylesheets."""
    
    DARK_THEME = """
        QMainWindow {
            background-color: #1a1a2e;
        }
        
        QWidget {
            background-color: #1a1a2e;
            color: #eaeaea;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        
        QFrame#sidebar {
            background-color: #16213e;
            border-right: 1px solid #0f3460;
        }
        
        QPushButton#navButton {
            background-color: transparent;
            color: #eaeaea;
            border: none;
            padding: 15px 20px;
            text-align: left;
            font-size: 14px;
            border-radius: 8px;
            margin: 2px 8px;
        }
        
        QPushButton#navButton:hover {
            background-color: #0f3460;
        }
        
        QPushButton#navButton:checked {
            background-color: #e94560;
            color: white;
        }
        
        QPushButton#primaryButton {
            background-color: #e94560;
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 8px;
        }
        
        QPushButton#primaryButton:hover {
            background-color: #ff6b6b;
        }
        
        QPushButton#primaryButton:disabled {
            background-color: #4a4a4a;
            color: #8a8a8a;
        }
        
        QPushButton#secondaryButton {
            background-color: #0f3460;
            color: white;
            border: 1px solid #e94560;
            padding: 10px 20px;
            font-size: 13px;
            border-radius: 6px;
        }
        
        QPushButton#secondaryButton:hover {
            background-color: #1a4a7a;
        }
        
        QLineEdit, QTextEdit, QPlainTextEdit {
            background-color: #16213e;
            color: #eaeaea;
            border: 2px solid #0f3460;
            border-radius: 8px;
            padding: 10px;
            font-size: 14px;
        }
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
            border-color: #e94560;
        }
        
        QComboBox {
            background-color: #16213e;
            color: #eaeaea;
            border: 2px solid #0f3460;
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 13px;
            min-width: 150px;
        }
        
        QComboBox:hover {
            border-color: #e94560;
        }
        
        QComboBox::drop-down {
            border: none;
            padding-right: 10px;
        }
        
        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 6px solid #e94560;
            margin-right: 10px;
        }
        
        QComboBox QAbstractItemView {
            background-color: #16213e;
            color: #eaeaea;
            selection-background-color: #e94560;
            border: 1px solid #0f3460;
        }
        
        QScrollArea {
            background-color: transparent;
            border: none;
        }
        
        QScrollBar:vertical {
            background-color: #16213e;
            width: 10px;
            border-radius: 5px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #0f3460;
            border-radius: 5px;
            min-height: 30px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #e94560;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        
        QLabel#titleLabel {
            font-size: 24px;
            font-weight: bold;
            color: #e94560;
        }
        
        QLabel#subtitleLabel {
            font-size: 14px;
            color: #8a8a8a;
        }
        
        QFrame#chatBubbleUser {
            background-color: #e94560;
            border-radius: 15px;
            padding: 12px;
        }
        
        QFrame#chatBubbleAI {
            background-color: #0f3460;
            border-radius: 15px;
            padding: 12px;
        }
        
        QSlider::groove:horizontal {
            background-color: #0f3460;
            height: 6px;
            border-radius: 3px;
        }
        
        QSlider::handle:horizontal {
            background-color: #e94560;
            width: 18px;
            height: 18px;
            margin: -6px 0;
            border-radius: 9px;
        }
        
        QSlider::sub-page:horizontal {
            background-color: #e94560;
            border-radius: 3px;
        }
        
        QSpinBox, QDoubleSpinBox {
            background-color: #16213e;
            color: #eaeaea;
            border: 2px solid #0f3460;
            border-radius: 6px;
            padding: 6px;
        }
        
        QSpinBox:focus, QDoubleSpinBox:focus {
            border-color: #e94560;
        }
        
        QCheckBox {
            color: #eaeaea;
            spacing: 8px;
        }
        
        QCheckBox::indicator {
            width: 20px;
            height: 20px;
            border-radius: 4px;
            border: 2px solid #0f3460;
            background-color: #16213e;
        }
        
        QCheckBox::indicator:checked {
            background-color: #e94560;
            border-color: #e94560;
        }
        
        QGroupBox {
            font-weight: bold;
            border: 2px solid #0f3460;
            border-radius: 8px;
            margin-top: 12px;
            padding-top: 10px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 15px;
            padding: 0 5px;
            color: #e94560;
        }
        
        QProgressBar {
            background-color: #16213e;
            border: none;
            border-radius: 8px;
            height: 20px;
            text-align: center;
        }
        
        QProgressBar::chunk {
            background-color: #e94560;
            border-radius: 8px;
        }
        
        QTabWidget::pane {
            border: 1px solid #0f3460;
            border-radius: 8px;
            background-color: #1a1a2e;
        }
        
        QTabBar::tab {
            background-color: #16213e;
            color: #8a8a8a;
            padding: 10px 20px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
        }
        
        QTabBar::tab:selected {
            background-color: #e94560;
            color: white;
        }
    """
    
    LIGHT_THEME = """
        QMainWindow {
            background-color: #f5f5f5;
        }
        
        QWidget {
            background-color: #f5f5f5;
            color: #333333;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        
        QFrame#sidebar {
            background-color: #ffffff;
            border-right: 1px solid #e0e0e0;
        }
        
        QPushButton#navButton {
            background-color: transparent;
            color: #333333;
            border: none;
            padding: 15px 20px;
            text-align: left;
            font-size: 14px;
            border-radius: 8px;
            margin: 2px 8px;
        }
        
        QPushButton#navButton:hover {
            background-color: #e8e8e8;
        }
        
        QPushButton#navButton:checked {
            background-color: #e94560;
            color: white;
        }
        
        QPushButton#primaryButton {
            background-color: #e94560;
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 8px;
        }
        
        QPushButton#primaryButton:hover {
            background-color: #d63050;
        }
        
        QPushButton#primaryButton:disabled {
            background-color: #cccccc;
            color: #888888;
        }
        
        QPushButton#secondaryButton {
            background-color: #ffffff;
            color: #e94560;
            border: 2px solid #e94560;
            padding: 10px 20px;
            font-size: 13px;
            border-radius: 6px;
        }
        
        QPushButton#secondaryButton:hover {
            background-color: #fff0f3;
        }
        
        QLineEdit, QTextEdit, QPlainTextEdit {
            background-color: #ffffff;
            color: #333333;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 10px;
            font-size: 14px;
        }
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
            border-color: #e94560;
        }
        
        QComboBox {
            background-color: #ffffff;
            color: #333333;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 13px;
            min-width: 150px;
        }
        
        QComboBox:hover {
            border-color: #e94560;
        }
        
        QComboBox::drop-down {
            border: none;
            padding-right: 10px;
        }
        
        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 6px solid #e94560;
            margin-right: 10px;
        }
        
        QComboBox QAbstractItemView {
            background-color: #ffffff;
            color: #333333;
            selection-background-color: #e94560;
            selection-color: white;
            border: 1px solid #e0e0e0;
        }
        
        QScrollBar:vertical {
            background-color: #f0f0f0;
            width: 10px;
            border-radius: 5px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #c0c0c0;
            border-radius: 5px;
            min-height: 30px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #e94560;
        }
        
        QLabel#titleLabel {
            font-size: 24px;
            font-weight: bold;
            color: #e94560;
        }
        
        QLabel#subtitleLabel {
            font-size: 14px;
            color: #666666;
        }
        
        QFrame#chatBubbleUser {
            background-color: #e94560;
            border-radius: 15px;
            padding: 12px;
        }
        
        QFrame#chatBubbleAI {
            background-color: #e8e8e8;
            border-radius: 15px;
            padding: 12px;
        }
    """
    
    @classmethod
    def get_theme(cls, theme_name: str) -> str:
        """Get stylesheet by theme name."""
        if theme_name == "light":
            return cls.LIGHT_THEME
        return cls.DARK_THEME
