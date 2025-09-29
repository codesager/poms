# P.O.M.S - Portfolio and OMS System (Modular Structure)

A modularized Streamlit-based web application for portfolio management queries using LangChain and OpenAI.

## 📁 Project Structure

```
poms/
├── __init__.py                 # Package initialization
├── app.py                      # Main application logic
├── config.py                   # Configuration and constants
├── ui_components.py            # UI components and display functions
├── utils.py                    # Utility functions
├── pots_models.py              # Pydantic models and LangChain setup
├── streamlit_app.py            # App entry point
├── requirements.txt            # Dependencies
├── README.md                   # Main README
├── README_MODULAR.md           # This file
└── notebooks/
    └── pots.ipynb             # Development notebook for testing
```

## 🏗️ Modular Architecture

### Core Modules

1. **`app.py`** - Main application orchestrator
   - Coordinates all components
   - Handles the main application flow
   - Minimal, focused on application logic

2. **`config.py`** - Configuration management
   - Page configuration settings
   - Custom CSS styles
   - Example queries
   - UI text constants
   - Centralized configuration

3. **`ui_components.py`** - UI components
   - Header, sidebar, footer rendering
   - Query input components
   - Result display functions
   - Reusable UI elements

4. **`utils.py`** - Utility functions
   - Session state management
   - Query processing logic
   - Error handling
   - Helper functions

5. **`pots_models.py`** - Data models and LangChain
   - Pydantic models
   - LangChain setup
   - Example data
   - Processing pipelines

## 🚀 Running the Application

### Running the Application
```bash
streamlit run streamlit_app.py
```

## 🔧 Benefits of Modular Structure

### Maintainability
- **Separation of Concerns**: Each module has a single responsibility
- **Easy Updates**: Modify specific functionality without affecting others
- **Code Reusability**: Components can be reused across different parts

### Scalability
- **Easy Extension**: Add new features by creating new modules
- **Team Development**: Multiple developers can work on different modules
- **Testing**: Individual modules can be tested in isolation

### Organization
- **Clear Structure**: Easy to understand and navigate
- **Documentation**: Each module can have focused documentation
- **Version Control**: Better tracking of changes per module

## 📝 Module Responsibilities

### `config.py`
- All configuration constants
- UI styling and themes
- Example data
- Text constants

### `ui_components.py`
- All UI rendering functions
- Component-specific display logic
- User interaction handling
- Visual formatting

### `utils.py`
- Business logic utilities
- Data processing functions
- Error handling
- Session management

### `app.py`
- Application flow control
- Component coordination
- Main entry point logic

## 🧪 Testing Individual Modules

You can test individual modules by importing them:

```python
# Test configuration
from config import configure_page, EXAMPLE_QUERIES

# Test UI components
from ui_components import render_header, display_order_result

# Test utilities
from utils import process_query, initialize_session_state
```

## 🔄 Clean Architecture

The modular structure provides:

1. **Clean separation** of concerns
2. **Improved code organization** and maintainability
3. **Easier testing** and development
4. **Scalable architecture** for future enhancements

## 📈 Future Enhancements

With the modular structure, you can easily:

- Add new UI components in `ui_components.py`
- Extend configuration in `config.py`
- Add new utility functions in `utils.py`
- Create new data models in `pots_models.py`
- Add new application features in `app.py`

## 🛠️ Development Workflow

1. **Configuration Changes**: Update `config.py`
2. **UI Changes**: Modify `ui_components.py`
3. **Logic Changes**: Update `utils.py`
4. **New Features**: Extend `app.py`
5. **Data Models**: Update `pots_models.py`
