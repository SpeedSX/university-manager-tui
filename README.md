# University Manager TUI

[![Pylint](https://github.com/SpeedSX/university-manager-tui/actions/workflows/pylint.yml/badge.svg)](https://github.com/SpeedSX/university-manager-tui/actions/workflows/pylint.yml)

A Terminal-based User Interface (TUI) application for managing university data including students, teachers, and faculties. Built with Python and the Textual library.

## Features

- **Student Management**: Add, edit, delete, and search for students
- **Teacher Management**: Add, edit, delete, and search for teachers
- **Faculty Management**: Add, edit, delete, and search for faculty departments
- **Tab-based Navigation**: Easily switch between students, teachers, and faculties
- **Search Functionality**: Find specific entries across all data types
- **Data Persistence**: All data is stored in JSON files

## Screenshots

*[Add screenshots here if available]*

## Requirements

- Python 3.7+
- Textual 0.40.0+
- Rich 13.3.5+

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/SpeedSX/university-manager-tui
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Run the application using:

```bash
python app.py
```

## Keyboard Shortcuts

- `q`: Quit the application
- `a`: Add a new entry (student/teacher/faculty)
- `e`: Edit the selected entry
- `d`: Delete the selected entry
- `f`: Focus the search input
- `r`: Refresh the current list
- `1`: Switch to Students tab
- `2`: Switch to Teachers tab
- `3`: Switch to Faculties tab

## Data Structure

The application stores data in JSON files located in the `data/` directory:
- `students.json`: Student records
- `teachers.json`: Teacher records
- `faculties.json`: Faculty department records

## Building a Standalone Executable

You can build a standalone executable using cx_Freeze:

```bash
python setup.py build
```

The executable will be created in the `build/` directory.

## License

MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
