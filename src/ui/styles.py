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
            font-family: 'FONT_FAMILY_PLACEHOLDER', Arial, sans-serif;
        }
        
        /* TopBar Styles */
        QFrame#topbar {
            background-color: #16213e;
            border-bottom: 1px solid #0f3460;
            min-height: 60px;
        }
        
        QPushButton#topBarButton {
            background-color: transparent;
            color: #eaeaea;
            border: none;
            padding: 8px 16px;
            font-size: 14px;
            border-radius: 6px;
            margin: 4px;
            font-weight: bold;
        }
        
        QPushButton#topBarButton:hover {
            background-color: #0f3460;
        }
        
        QPushButton#topBarButton:checked {
            background-color: #e94560;
            color: white;
        }
        
        /* Sidebar/History Styles */
        QFrame#historySidebar {
            background-color: #16213e;
            border-right: 1px solid #0f3460;
            min-width: 250px;
            max-width: 300px;
        }
        
        QLabel#sectionTitle {
            color: #8a8a8a;
            font-weight: bold;
            padding: 10px;
            font-size: 12px;
            text-transform: uppercase;
        }

        QPushButton#historyItem {
            background-color: transparent;
            color: #b0b0b0;
            border: none;
            padding: 8px 12px;
            text-align: left;
            border-radius: 4px;
            margin: 2px 5px;
        }
        
        QPushButton#historyItem:hover {
            background-color: #0f3460;
            color: #eaeaea;
        }
        
        QPushButton#historyItem:checked {
            background-color: #0f3460;
            color: #e94560;
            font-weight: bold;
        }
        
        /* Settings Button in Sidebar */
        QPushButton#settingsButton {
            background-color: transparent;
            color: #eaeaea;
            border: none;
            padding: 12px;
            text-align: left;
            font-size: 14px;
            border-top: 1px solid #0f3460;
        }
        
        QPushButton#settingsButton:hover {
            background-color: #0f3460;
        }

        /* Common Button Styles */
        QPushButton#primaryButton {
            background-color: #e94560;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 6px;
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
            padding: 8px 16px;
            font-size: 13px;
            border-radius: 6px;
        }
        
        QPushButton#secondaryButton:hover {
            background-color: #1a4a7a;
        }
        
        QPushButton#iconButton {
            background-color: transparent;
            border: none;
            border-radius: 4px;
            padding: 4px;
        }
        
        QPushButton#iconButton:hover {
            background-color: #0f3460;
        }
        
        /* Inputs */
        QLineEdit, QTextEdit, QPlainTextEdit {
            background-color: #16213e;
            color: #eaeaea;
            border: 1px solid #0f3460;
            border-radius: 6px;
            padding: 8px;
            font-size: 14px;
        }
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
            border: 1px solid #e94560;
        }
        
        QComboBox {
            background-color: #16213e;
            color: #eaeaea;
            border: 1px solid #0f3460;
            border-radius: 6px;
            padding: 6px 10px;
            font-size: 13px;
            min-width: 100px;
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
        
        /* ScrollBar - Themed */
        QScrollBar:vertical {
            background-color: #16213e;
            width: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #2e3b55;
            border-radius: 6px;
            min-height: 30px;
            margin: 2px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #e94560;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }

        QScrollBar:horizontal {
            background-color: #16213e;
            height: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:horizontal {
            background-color: #2e3b55;
            border-radius: 6px;
            min-width: 30px;
            margin: 2px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background-color: #e94560;
        }
        
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            width: 0px;
        }
        
        /* Labels */
        QLabel#titleLabel {
            font-size: 24px;
            font-weight: bold;
            color: #e94560;
        }
        
        QLabel#subtitleLabel {
            font-size: 14px;
            color: #8a8a8a;
        }
        
        /* Chat Bubbles */
        QFrame#chatBubbleUser {
            background-color: #e94560;
            border-radius: 12px;
            border-top-right-radius: 2px;
            padding: 12px;
        }
        
        QFrame#chatBubbleAI {
            background-color: #1f2a48;
            border-radius: 12px;
            border-top-left-radius: 2px;
            padding: 12px;
            border: 1px solid #0f3460;
        }
        
        /* Other Widgets */
        QGroupBox {
            font-weight: bold;
            border: 1px solid #0f3460;
            border-radius: 8px;
            margin-top: 12px;
            padding-top: 10px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
            color: #e94560;
        }
        
        QTabWidget::pane {
            border: 1px solid #0f3460;
            border-radius: 8px;
            background-color: #1a1a2e;
        }
        
        QTabBar::tab {
            background-color: #16213e;
            color: #8a8a8a;
            padding: 8px 16px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
        }
        
        QTabBar::tab:selected {
            background-color: #e94560;
            color: white;
        }
    """
    
    LIGHT_THEME = """
        QMainWindow {
            background-color: #ffffff;
        }
        
        QWidget {
            background-color: #ffffff;
            color: #2d3436;
            font-family: 'FONT_FAMILY_PLACEHOLDER', Arial, sans-serif;
        }
        
        /* TopBar Styles */
        QFrame#topbar {
            background-color: #f8f9fa;
            border-bottom: 1px solid #e0e0e0;
            min-height: 60px;
        }
        
        QPushButton#topBarButton {
            background-color: transparent;
            color: #2d3436;
            border: none;
            padding: 8px 16px;
            font-size: 14px;
            border-radius: 6px;
            margin: 4px;
            font-weight: bold;
        }
        
        QPushButton#topBarButton:hover {
            background-color: #e0e0e0;
        }
        
        QPushButton#topBarButton:checked {
            background-color: #e94560;
            color: white;
        }
        
        /* Sidebar/History Styles */
        QFrame#historySidebar {
            background-color: #f8f9fa;
            border-right: 1px solid #e0e0e0;
            min-width: 250px;
            max-width: 300px;
        }
        
        QLabel#sectionTitle {
            color: #636e72;
            font-weight: bold;
            padding: 10px;
            font-size: 12px;
            text-transform: uppercase;
        }

        QPushButton#historyItem {
            background-color: transparent;
            color: #636e72;
            border: none;
            padding: 8px 12px;
            text-align: left;
            border-radius: 4px;
            margin: 2px 5px;
        }
        
        QPushButton#historyItem:hover {
            background-color: #e0e0e0;
            color: #2d3436;
        }
        
        QPushButton#historyItem:checked {
            background-color: #e0e0e0;
            color: #e94560;
            font-weight: bold;
        }
        
        /* Settings Button in Sidebar */
        QPushButton#settingsButton {
            background-color: transparent;
            color: #2d3436;
            border: none;
            padding: 12px;
            text-align: left;
            font-size: 14px;
            border-top: 1px solid #e0e0e0;
        }
        
        QPushButton#settingsButton:hover {
            background-color: #e0e0e0;
        }

        /* Common Button Styles */
        QPushButton#primaryButton {
            background-color: #e94560;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 6px;
        }
        
        QPushButton#primaryButton:hover {
            background-color: #d63050;
        }
        
        QPushButton#primaryButton:disabled {
            background-color: #dfe6e9;
            color: #b2bec3;
        }
        
        QPushButton#secondaryButton {
            background-color: #ffffff;
            color: #e94560;
            border: 1px solid #e94560;
            padding: 8px 16px;
            font-size: 13px;
            border-radius: 6px;
        }
        
        QPushButton#secondaryButton:hover {
            background-color: #fff0f3;
        }
        
        QPushButton#iconButton {
            background-color: transparent;
            border: none;
            border-radius: 4px;
            padding: 4px;
        }
        
        QPushButton#iconButton:hover {
            background-color: #e0e0e0;
        }
        
        /* Inputs */
        QLineEdit, QTextEdit, QPlainTextEdit {
            background-color: #ffffff;
            color: #2d3436;
            border: 1px solid #dfe6e9;
            border-radius: 6px;
            padding: 8px;
            font-size: 14px;
        }
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
            border: 1px solid #e94560;
        }
        
        QComboBox {
            background-color: #ffffff;
            color: #2d3436;
            border: 1px solid #dfe6e9;
            border-radius: 6px;
            padding: 6px 10px;
            font-size: 13px;
            min-width: 100px;
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
            color: #2d3436;
            selection-background-color: #e94560;
            selection-color: white;
            border: 1px solid #dfe6e9;
        }
        
        /* ScrollBar - Themed */
        QScrollBar:vertical {
            background-color: #f1f2f6;
            width: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #ced6e0;
            border-radius: 6px;
            min-height: 30px;
            margin: 2px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #e94560;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }

        QScrollBar:horizontal {
            background-color: #f1f2f6;
            height: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:horizontal {
            background-color: #ced6e0;
            border-radius: 6px;
            min-width: 30px;
            margin: 2px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background-color: #e94560;
        }
        
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            width: 0px;
        }
        
        /* Labels */
        QLabel#titleLabel {
            font-size: 24px;
            font-weight: bold;
            color: #e94560;
        }
        
        QLabel#subtitleLabel {
            font-size: 14px;
            color: #636e72;
        }
        
        /* Chat Bubbles */
        QFrame#chatBubbleUser {
            background-color: #e94560;
            border-radius: 12px;
            border-top-right-radius: 2px;
            padding: 12px;
            color: white;
        }
        
        QFrame#chatBubbleAI {
            background-color: #f1f2f6;
            border-radius: 12px;
            border-top-left-radius: 2px;
            padding: 12px;
            border: 1px solid #dfe6e9;
        }
        
        /* Other Widgets */
        QGroupBox {
            font-weight: bold;
            border: 1px solid #dfe6e9;
            border-radius: 8px;
            margin-top: 12px;
            padding-top: 10px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
            color: #e94560;
        }
        
        QTabWidget::pane {
            border: 1px solid #dfe6e9;
            border-radius: 8px;
            background-color: #ffffff;
        }
        
        QTabBar::tab {
            background-color: #f1f2f6;
            color: #636e72;
            padding: 8px 16px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
        }
        
        QTabBar::tab:selected {
            background-color: #e94560;
            color: white;
        }
    """
    
    @classmethod
    def get_theme(cls, theme_name: str, font_family: str = "Segoe UI") -> str:
        """Get stylesheet by theme name."""
        if theme_name == "light":
            return cls.LIGHT_THEME.replace("FONT_FAMILY_PLACEHOLDER", font_family)
        return cls.DARK_THEME.replace("FONT_FAMILY_PLACEHOLDER", font_family)
