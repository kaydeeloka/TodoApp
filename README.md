# TODO APP

Simple Todo App where you can add, update, and delete your todos.

## Directory Structure
<pre>
  /todo_app/
├── app.py # Flask application entry point
├── requirements.txt # Python dependencies
├── static/
│   └── style.css # CSS styling for the app
│ 
├── templates/
│ ├── base.html # Base HTML template
│ └── index.html # Main UI for managing todos
</pre>

## Installation

1. **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv  # Or use your preferred environment manager
    ```

2. **Activate the virtual environment**:
    - On Linux/macOS:
      ```bash
      source venv/bin/activate
      ```
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Flask application**:
    ```bash
    python app.py
    ```

2. **Open your browser and navigate to**:
    ```
    http://127.0.0.1:5000
    ```

3. **Manage your todos**:
   - Add new todo items.
   - Edit existing todos.
   - Delete todos you no longer need.

## Features

- Add new tasks with a single input.
- Update existing todos by clicking edit.
- Delete tasks easily with a button.
- Responsive UI with simple styling.
