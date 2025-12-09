# RoleAI (PythonAI) - PyQt5 Edition

A modern Python desktop application that integrates OpenAI and LumaAI APIs for AI chat, AI-to-AI conversations, image generation, and video generation.

## Features

- **💬 Chat with AI** - Have conversations with OpenAI's GPT models
- **🤖 AI-to-AI Chat** - Watch two AI assistants have conversations with each other
- **🖼️ Image Generator** - Generate images using DALL-E 3
- **🎬 Video Generator** - Create videos using LumaAI
- **⚙️ Settings** - Configure API keys, models, and preferences
- **📝 Feedback** - Submit feedback and bug reports
- **🔄 Update Checker** - Keep the application up to date

## Requirements

- Python 3.8+
- PyQt5
- OpenAI API key (for chat, AI-to-AI, and image generation)
- LumaAI API key (for video generation)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Ru4Ka-Python/PythonAI.git
   cd PythonAI
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Configuration

On first launch, go to **Settings** and configure your API keys:

1. **OpenAI API Key** - Required for Chat, AI-to-AI, and Image Generation features
2. **LumaAI API Key** - Required for Video Generation feature

## Screenshots

### Chat with AI Mode
![Chat with AI](https://github.com/Ru4Ka-Python/PythonAI/blob/main/Chat%20with%20AI.png)

### AI-to-AI Mode
![AI-to-AI Chat](https://github.com/Ru4Ka-Python/PythonAI/blob/main/AI-to-AI%20Chat.png)

### Image Generator Mode
![Image Generator](https://github.com/Ru4Ka-Python/PythonAI/blob/main/Image%20Generator.png)

### Video Generator Mode
![Video Generator](https://github.com/Ru4Ka-Python/PythonAI/blob/main/Video%20Generator.png)

### Settings
![Settings](https://github.com/Ru4Ka-Python/PythonAI/blob/main/Settings.png)

### Feedback
![Feedback](https://github.com/Ru4Ka-Python/PythonAI/blob/main/Feedback.png)

### Check for Updates
![Check for Updates](https://github.com/Ru4Ka-Python/PythonAI/blob/main/Check%20for%20updates.png)

## Project Structure

```
PythonAI/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── src/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── api/
│   │   ├── __init__.py
│   │   ├── openai_client.py   # OpenAI API wrapper
│   │   └── lumaai_client.py   # LumaAI API wrapper
│   └── ui/
│       ├── __init__.py
│       ├── main_window.py     # Main application window
│       ├── styles.py          # Stylesheet definitions
│       ├── config.py          # UI config exports
│       ├── widgets/
│       │   ├── __init__.py
│       │   ├── chat_widget.py # Chat display widget
│       │   └── sidebar.py     # Navigation sidebar
│       └── pages/
│           ├── __init__.py
│           ├── base_page.py       # Base page class
│           ├── chat_page.py       # Chat with AI page
│           ├── ai_to_ai_page.py   # AI-to-AI chat page
│           ├── image_page.py      # Image generator page
│           ├── video_page.py      # Video generator page
│           ├── settings_page.py   # Settings page
│           ├── feedback_page.py   # Feedback page
│           └── updates_page.py    # Update checker page
```

## Version History

### v1.6.0-beta (PyQt5 Edition)
- Complete rewrite using PyQt5 for modern, cross-platform UI
- Clean, modular code architecture
- Improved error handling and user feedback
- Streaming responses for chat
- Dark and light theme support
- Automatic update checking

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue on GitHub.
