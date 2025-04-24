from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Button, DataTable, Input, Label, Static
from textual.widgets.data_table import RowKey
from textual.screen import Screen, ModalScreen
from textual import on
from textual.binding import Binding

from models import Student
from data_manager import DataManager


# Define custom CSS for layout and styling
CUSTOM_CSS = """
Screen {
    layout: grid;
    grid-size: 1;
    padding: 0;
}

#main {
    layout: grid;
    grid-size: 1;
    grid-rows: 3 3 1fr 3;
    padding: 0 1;
    width: 100%;
    height: 100%;
    border: $accent;
}

#tabs-container {
    width: 100%;
    height: 3;
    align: center middle;
    background: $surface-darken-1;
}

.tab-button {
    width: 16;
    height: 3;
    content-align: center middle;
    background: $surface;
}

.tab-button.-active {
    background: $accent;
    text-style: bold;
}

#search-bar {
    width: 100%;
    height: 3;
    align: left middle;
    background: $surface-darken-1;
    padding: 0 1;
}

.data-table {
    width: 100%;
    height: 100%;
    margin: 0;
    min-height: 10;
    border: $accent;
    background: $surface;
}

#action-bar {
    width: 100%;
    height: 3;
    align: center middle;
    background: $surface-darken-1;
    padding: 0 1;
}

Button {
    margin: 0 1 0 0;
    min-width: 16;
    height: 3;
    padding: 0 1;
    content-align: center middle;
    text-style: bold;
}

Input {
    width: 1fr;
    margin: 0 1 0 0;
}

Label {
    width: auto;
    height: 1;
    padding: 0 1 0 0;
}

#dialog {
    padding: 1 2;
    width: 60;
    height: auto;
    border: $accent;
    background: $surface;
}

#dialog-title {
    text-style: bold;
    text-align: center;
    width: 100%;
}

#dialog-buttons {
    margin-top: 1;
    align: center middle;
}
"""

class AddEditStudentModal(ModalScreen):
    """Modal dialog for adding or editing a student."""

    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
        Binding("f1", "save", "Save"),
    ]
    
    def __init__(self, edit_student=None, on_save_callback=None):
        """Initialize the modal with optional student to edit."""
        super().__init__()
        self.edit_student = edit_student
        self.on_save_callback = on_save_callback
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the modal."""
        with Container(id="dialog"):
            yield Label(f"{'Edit' if self.edit_student else 'Add'} Student", id="dialog-title")
            
            yield Label("First Name:")
            yield Input(
                value=self.edit_student.first_name if self.edit_student else "",
                placeholder="Enter first name",
                id="first-name",
            )
            
            yield Label("Last Name:")
            yield Input(
                value=self.edit_student.last_name if self.edit_student else "",
                placeholder="Enter last name",
                id="last-name",
            )
            
            yield Label("Age:")
            yield Input(
                value=str(self.edit_student.age) if self.edit_student else "",
                placeholder="Enter age",
                id="age",
            )
            
            yield Label("Major:")
            yield Input(
                value=self.edit_student.major if self.edit_student else "",
                placeholder="Enter major",
                id="major",
            )
            
            yield Label("GPA:")
            yield Input(
                value=str(self.edit_student.gpa) if self.edit_student else "",
                placeholder="Enter GPA",
                id="gpa",
            )
            
            with Horizontal(id="dialog-buttons"):
                yield Button("Cancel", variant="error", id="cancel-button")
                yield Button("Save", variant="success", id="save-button")

    def action_cancel(self) -> None:
        """Cancel adding/editing student and close modal."""
        self.dismiss(None)
    
    def action_save(self) -> None:
        """Save the student data and close the modal."""
        self._save_student()
    
    def _save_student(self) -> None:
        """Save the student data."""
        first_name = self.query_one("#first-name", expect_type=Input).value
        last_name = self.query_one("#last-name", expect_type=Input).value
        age_text = self.query_one("#age", expect_type=Input).value
        major = self.query_one("#major", expect_type=Input).value
        gpa_text = self.query_one("#gpa", expect_type=Input).value
        
        # Basic validation
        if not all([first_name, last_name, age_text, major, gpa_text]):
            self.app.notify("All fields are required", severity="error")
            return
        
        try:
            age = int(age_text)
            gpa = float(gpa_text)
            
            if not (0 <= gpa <= 4.0):
                self.app.notify("GPA must be between 0.0 and 4.0", severity="error")
                return
            
            if not (16 <= age <= 99):
                self.app.notify("Age must be between 16 and 99", severity="error")
                return
                
        except ValueError:
            self.app.notify("Age must be an integer and GPA must be a number", severity="error")
            return
        
        # Create student object
        student = Student(
            id=self.edit_student.id if self.edit_student else None,
            first_name=first_name,
            last_name=last_name,
            age=age,
            major=major,
            gpa=gpa,
        )
        
        # Use the callback if provided
        if self.on_save_callback:
            self.on_save_callback(student)
            self.app.notify(f"Added student: {student.full_name()}")
        
        # Close the modal
        self.dismiss()
        
    @on(Button.Pressed, "#cancel-button")
    def on_cancel_pressed(self) -> None:
        """Handle the cancel button press."""
        self.action_cancel()
    
    @on(Button.Pressed, "#save-button")
    def on_save_pressed(self) -> None:
        """Handle the save button press."""
        self._save_student()


class DeleteConfirmationModal(ModalScreen):
    """Modal dialog for confirming student deletion."""
    
    BINDINGS = [Binding("escape", "cancel", "Cancel")]
    
    def __init__(self, student, on_confirm_callback=None):
        """Initialize with the student to delete."""
        super().__init__()
        self.student = student
        self.on_confirm_callback = on_confirm_callback
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the modal."""
        with Container(id="dialog"):
            yield Label("Confirm Delete", id="dialog-title")
            yield Static(f"Are you sure you want to delete {self.student.full_name()}?")
            
            with Horizontal(id="dialog-buttons"):
                yield Button("Cancel", variant="primary", id="cancel-button")
                yield Button("Delete", variant="error", id="delete-confirm-button")
    
    def action_cancel(self) -> None:
        """Cancel the deletion."""
        self.dismiss()
    
    def action_delete(self) -> None:
        """Delete the student and close modal."""
        if self.on_confirm_callback:
            self.on_confirm_callback(self.student)
        self.dismiss()
    
    @on(Button.Pressed, "#cancel-button")
    def on_cancel_pressed(self) -> None:
        """Handle the cancel button press."""
        self.action_cancel()
    
    @on(Button.Pressed, "#delete-confirm-button")
    def on_delete_pressed(self) -> None:
        """Handle the delete button press."""
        self.action_delete()


class AddEditTeacherModal(ModalScreen):
    """Modal dialog for adding or editing a teacher."""

    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
        Binding("f1", "save", "Save"),
    ]
    
    def __init__(self, edit_teacher=None, on_save_callback=None):
        """Initialize the modal with optional teacher to edit."""
        super().__init__()
        self.edit_teacher = edit_teacher
        self.on_save_callback = on_save_callback
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the modal."""
        with Container(id="dialog"):
            yield Label(f"{'Edit' if self.edit_teacher else 'Add'} Teacher", id="dialog-title")
            
            yield Label("First Name:")
            yield Input(
                value=self.edit_teacher.first_name if self.edit_teacher else "",
                placeholder="Enter first name",
                id="first-name",
            )
            
            yield Label("Last Name:")
            yield Input(
                value=self.edit_teacher.last_name if self.edit_teacher else "",
                placeholder="Enter last name",
                id="last-name",
            )
            
            yield Label("Age:")
            yield Input(
                value=str(self.edit_teacher.age) if self.edit_teacher else "",
                placeholder="Enter age",
                id="age",
            )
            
            yield Label("Department:")
            yield Input(
                value=self.edit_teacher.department if self.edit_teacher else "",
                placeholder="Enter department",
                id="department",
            )
            
            yield Label("Title:")
            yield Input(
                value=self.edit_teacher.title if self.edit_teacher else "",
                placeholder="Enter title (e.g., Professor)",
                id="title",
            )
            
            with Horizontal(id="dialog-buttons"):
                yield Button("Cancel", variant="error", id="cancel-button")
                yield Button("Save", variant="success", id="save-button")

    def action_cancel(self) -> None:
        """Cancel adding/editing teacher and close modal."""
        self.dismiss(None)
    
    def action_save(self) -> None:
        """Save the teacher data and close the modal."""
        self._save_teacher()
    
    def _save_teacher(self) -> None:
        """Save the teacher data."""
        first_name = self.query_one("#first-name", expect_type=Input).value
        last_name = self.query_one("#last-name", expect_type=Input).value
        age_text = self.query_one("#age", expect_type=Input).value
        department = self.query_one("#department", expect_type=Input).value
        title = self.query_one("#title", expect_type=Input).value
        
        # Basic validation
        if not all([first_name, last_name, age_text, department, title]):
            self.app.notify("All fields are required", severity="error")
            return
        
        try:
            age = int(age_text)
            
            if not (18 <= age <= 99):
                self.app.notify("Age must be between 18 and 99", severity="error")
                return
                
        except ValueError:
            self.app.notify("Age must be an integer", severity="error")
            return
        
        # Create teacher object
        from models import Teacher
        teacher = Teacher(
            id=self.edit_teacher.id if self.edit_teacher else None,
            first_name=first_name,
            last_name=last_name,
            age=age,
            department=department,
            title=title,
        )
        
        # Use the callback if provided
        if self.on_save_callback:
            self.on_save_callback(teacher)
            self.app.notify(f"{'Updated' if self.edit_teacher else 'Added'} teacher: {teacher.full_name()}")
        
        # Close the modal
        self.dismiss()
        
    @on(Button.Pressed, "#cancel-button")
    def on_cancel_pressed(self) -> None:
        """Handle the cancel button press."""
        self.action_cancel()
    
    @on(Button.Pressed, "#save-button")
    def on_save_pressed(self) -> None:
        """Handle the save button press."""
        self._save_teacher()


class AddEditFacultyModal(ModalScreen):
    """Modal dialog for adding or editing a faculty."""

    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
        Binding("f1", "save", "Save"),
    ]
    
    def __init__(self, edit_faculty=None, on_save_callback=None):
        """Initialize the modal with optional faculty to edit."""
        super().__init__()
        self.edit_faculty = edit_faculty
        self.on_save_callback = on_save_callback
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the modal."""
        with Container(id="dialog"):
            yield Label(f"{'Edit' if self.edit_faculty else 'Add'} Faculty", id="dialog-title")
            
            yield Label("Name:")
            yield Input(
                value=self.edit_faculty.name if self.edit_faculty else "",
                placeholder="Enter faculty name",
                id="name",
            )
            
            yield Label("Building:")
            yield Input(
                value=self.edit_faculty.building if self.edit_faculty else "",
                placeholder="Enter building",
                id="building",
            )
            
            yield Label("Head Name:")
            yield Input(
                value=self.edit_faculty.head_name if self.edit_faculty else "",
                placeholder="Enter head's name",
                id="head-name",
            )
            
            yield Label("Established Year:")
            yield Input(
                value=str(self.edit_faculty.established_year) if self.edit_faculty else "",
                placeholder="Enter established year",
                id="established-year",
            )
            
            yield Label("Number of Staff:")
            yield Input(
                value=str(self.edit_faculty.num_staff) if self.edit_faculty else "",
                placeholder="Enter number of staff",
                id="num-staff",
            )
            
            with Horizontal(id="dialog-buttons"):
                yield Button("Cancel", variant="error", id="cancel-button")
                yield Button("Save", variant="success", id="save-button")

    def action_cancel(self) -> None:
        """Cancel adding/editing faculty and close modal."""
        self.dismiss(None)
    
    def action_save(self) -> None:
        """Save the faculty data and close the modal."""
        self._save_faculty()
    
    def _save_faculty(self) -> None:
        """Save the faculty data."""
        name = self.query_one("#name", expect_type=Input).value
        building = self.query_one("#building", expect_type=Input).value
        head_name = self.query_one("#head-name", expect_type=Input).value
        established_year_text = self.query_one("#established-year", expect_type=Input).value
        num_staff_text = self.query_one("#num-staff", expect_type=Input).value
        
        # Basic validation
        if not all([name, building, head_name, established_year_text, num_staff_text]):
            self.app.notify("All fields are required", severity="error")
            return
        
        try:
            established_year = int(established_year_text)
            num_staff = int(num_staff_text)
            
            current_year = 2025  # Update this as needed
            if not (1500 <= established_year <= current_year):
                self.app.notify(f"Established year must be between 1500 and {current_year}", severity="error")
                return
                
            if num_staff <= 0:
                self.app.notify("Number of staff must be positive", severity="error")
                return
                
        except ValueError:
            self.app.notify("Year and number of staff must be integers", severity="error")
            return
        
        # Create faculty object
        from models import Faculty
        faculty = Faculty(
            id=self.edit_faculty.id if self.edit_faculty else None,
            name=name,
            building=building,
            head_name=head_name,
            established_year=established_year,
            num_staff=num_staff,
        )
        
        # Use the callback if provided
        if self.on_save_callback:
            self.on_save_callback(faculty)
            self.app.notify(f"{'Updated' if self.edit_faculty else 'Added'} faculty: {faculty.name}")
        
        # Close the modal
        self.dismiss()
        
    @on(Button.Pressed, "#cancel-button")
    def on_cancel_pressed(self) -> None:
        """Handle the cancel button press."""
        self.action_cancel()
    
    @on(Button.Pressed, "#save-button")
    def on_save_pressed(self) -> None:
        """Handle the save button press."""
        self._save_faculty()


class DeleteTeacherConfirmationModal(ModalScreen):
    """Modal dialog for confirming teacher deletion."""
    
    BINDINGS = [Binding("escape", "cancel", "Cancel")]
    
    def __init__(self, teacher, on_confirm_callback=None):
        """Initialize with the teacher to delete."""
        super().__init__()
        self.teacher = teacher
        self.on_confirm_callback = on_confirm_callback
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the modal."""
        with Container(id="dialog"):
            yield Label("Confirm Delete", id="dialog-title")
            yield Static(f"Are you sure you want to delete {self.teacher.full_name()}?")
            
            with Horizontal(id="dialog-buttons"):
                yield Button("Cancel", variant="primary", id="cancel-button")
                yield Button("Delete", variant="error", id="teacher-delete-confirm-button")
    
    def action_cancel(self) -> None:
        """Cancel the deletion."""
        self.dismiss()
    
    def action_delete(self) -> None:
        """Delete the teacher and close modal."""
        if self.on_confirm_callback:
            self.on_confirm_callback(self.teacher)
        self.dismiss()
    
    @on(Button.Pressed, "#cancel-button")
    def on_cancel_pressed(self) -> None:
        """Handle the cancel button press."""
        self.action_cancel()
    
    @on(Button.Pressed, "#teacher-delete-confirm-button")
    def on_delete_pressed(self) -> None:
        """Handle the delete button press."""
        self.action_delete()


class DeleteFacultyConfirmationModal(ModalScreen):
    """Modal dialog for confirming faculty deletion."""
    
    BINDINGS = [Binding("escape", "cancel", "Cancel")]
    
    def __init__(self, faculty, on_confirm_callback=None):
        """Initialize with the faculty to delete."""
        super().__init__()
        self.faculty = faculty
        self.on_confirm_callback = on_confirm_callback
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the modal."""
        with Container(id="dialog"):
            yield Label("Confirm Delete", id="dialog-title")
            yield Static(f"Are you sure you want to delete faculty: {self.faculty.name}?")
            
            with Horizontal(id="dialog-buttons"):
                yield Button("Cancel", variant="primary", id="cancel-button")
                yield Button("Delete", variant="error", id="faculty-delete-confirm-button")
    
    def action_cancel(self) -> None:
        """Cancel the deletion."""
        self.dismiss()
    
    def action_delete(self) -> None:
        """Delete the faculty and close modal."""
        if self.on_confirm_callback:
            self.on_confirm_callback(self.faculty)
        self.dismiss()
    
    @on(Button.Pressed, "#cancel-button")
    def on_cancel_pressed(self) -> None:
        """Handle the cancel button press."""
        self.action_cancel()
    
    @on(Button.Pressed, "#faculty-delete-confirm-button")
    def on_delete_pressed(self) -> None:
        """Handle the delete button press."""
        self.action_delete()


class StudentManagerApp(App):
    """Main application for managing university data."""
    
    TITLE = "University Manager"
    CSS_PATH = None
    CSS = CUSTOM_CSS
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("a", "add_entity", "Add"),
        Binding("e", "edit_entity", "Edit"),
        Binding("d", "delete_entity", "Delete"),
        Binding("f", "focus_search", "Search"),
        Binding("r", "refresh", "Refresh"),
        Binding("1", "show_students", "Students"),
        Binding("2", "show_teachers", "Teachers"), 
        Binding("3", "show_faculties", "Faculties"),
    ]
    
    def __init__(self):
        """Initialize the application."""
        super().__init__()
        self.data_manager = DataManager()
        self.deletion_in_progress = False
        self.current_tab = "students"  # Track active tab
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        
        with Container(id="main"):
            with Horizontal(id="tabs-container"):
                yield Button("Students", classes="tab-button -active", id="students-tab")
                yield Button("Teachers", classes="tab-button", id="teachers-tab")
                yield Button("Faculties", classes="tab-button", id="faculties-tab")
            
            with Horizontal(id="search-bar"):
                yield Label("Search:")
                yield Input(placeholder="Search by name or other fields", id="search-input")
                yield Button("Search", variant="primary", id="search-button")
            
            # Tables for each entity type - without visible parameter
            yield DataTable(id="students-table", classes="data-table")
            yield DataTable(id="teachers-table", classes="data-table")
            yield DataTable(id="faculties-table", classes="data-table")
            
            with Horizontal(id="action-bar"):
                yield Button("Add", variant="success", id="add-button")
                yield Button("Edit", variant="primary", id="edit-button")
                yield Button("Delete", variant="error", id="delete-button")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Set up the app after mounting."""
        self._setup_tables()
        
        # Initially hide teachers and faculties tables using display property instead of visible
        self.query_one("#teachers-table").display = False
        self.query_one("#faculties-table").display = False
        
        # Load student data
        self._load_students()
    
    def _setup_tables(self) -> None:
        """Setup data tables for all entity types."""
        # Set up students table
        students_table = self.query_one("#students-table", expect_type=DataTable)
        students_table.add_columns("Name", "Age", "Major", "GPA")
        students_table.cursor_type = "row"
        
        # Set up teachers table
        teachers_table = self.query_one("#teachers-table", expect_type=DataTable)
        teachers_table.add_columns("Name", "Age", "Department", "Title")
        teachers_table.cursor_type = "row"
        
        # Set up faculties table
        faculties_table = self.query_one("#faculties-table", expect_type=DataTable)
        faculties_table.add_columns("Name", "Building", "Head", "Est. Year", "Staff")
        faculties_table.cursor_type = "row"
    
    # Tab switching methods
    def action_show_students(self) -> None:
        """Switch to Students tab."""
        self._switch_tab("students")
        
    def action_show_teachers(self) -> None:
        """Switch to Teachers tab."""
        self._switch_tab("teachers")
        
    def action_show_faculties(self) -> None:
        """Switch to Faculties tab."""
        self._switch_tab("faculties")
    
    def _switch_tab(self, tab_name: str) -> None:
        """Switch between different tabs."""
        if self.current_tab == tab_name:
            return
            
        # Update tab buttons
        self.query_one(f"#{self.current_tab}-tab").remove_class("-active")
        self.query_one(f"#{tab_name}-tab").add_class("-active")
        
        # Hide/show tables using display property instead of visible
        self.query_one(f"#{self.current_tab}-table").display = False
        self.query_one(f"#{tab_name}-table").display = True
        
        # Update search placeholder
        search_input = self.query_one("#search-input", expect_type=Input)
        if tab_name == "students":
            search_input.placeholder = "Search students by name or major"
        elif tab_name == "teachers":
            search_input.placeholder = "Search teachers by name, department or title"
        else:
            search_input.placeholder = "Search faculties by name, building or head name"
        
        # Update current tab
        self.current_tab = tab_name
        
        # Load appropriate data
        if tab_name == "students":
            self._load_students()
        elif tab_name == "teachers":
            self._load_teachers()
        else:
            self._load_faculties()
    
    # Data loading methods
    def _load_students(self) -> None:
        """Load students into the table."""
        table = self.query_one("#students-table", expect_type=DataTable)
        table.clear()
        
        for student in self.data_manager.get_all_students():
            table.add_row(
                student.full_name(),
                str(student.age),
                student.major,
                f"{student.gpa:.2f}",
                key=student.id
            )
    
    def _load_teachers(self) -> None:
        """Load teachers into the table."""
        table = self.query_one("#teachers-table", expect_type=DataTable)
        table.clear()
        
        for teacher in self.data_manager.get_all_teachers():
            table.add_row(
                teacher.full_name(),
                str(teacher.age),
                teacher.department,
                teacher.title,
                key=teacher.id
            )
    
    def _load_faculties(self) -> None:
        """Load faculties into the table."""
        table = self.query_one("#faculties-table", expect_type=DataTable)
        table.clear()
        
        for faculty in self.data_manager.get_all_faculties():
            table.add_row(
                faculty.name,
                faculty.building,
                faculty.head_name,
                str(faculty.established_year),
                str(faculty.num_staff),
                key=faculty.id
            )
    
    # Selection methods
    def _get_selected_entity(self):
        """Get the currently selected entity based on current tab."""
        if self.current_tab == "students":
            return self._get_selected_student()
        elif self.current_tab == "teachers":
            return self._get_selected_teacher()
        else:
            return self._get_selected_faculty()
    
    def _get_selected_student(self):
        """Get the currently selected student."""
        table = self.query_one("#students-table", expect_type=DataTable)
        if table.cursor_row is None:
            self.notify("No student selected", severity="warning")
            return None
        
        try:
            row_index = table.cursor_row
            row_keys = list(table.rows.keys())
            
            if row_index < 0 or row_index >= len(row_keys):
                self.notify("Invalid row selection", severity="error")
                return None
                
            row_key = row_keys[row_index]
            return self.data_manager.get_student_by_id(row_key)
        except Exception as e:
            self.notify(f"Error getting selected student: {str(e)}", severity="error")
            return None
    
    def _get_selected_teacher(self):
        """Get the currently selected teacher."""
        table = self.query_one("#teachers-table", expect_type=DataTable)
        if table.cursor_row is None:
            self.notify("No teacher selected", severity="warning")
            return None
        
        try:
            row_index = table.cursor_row
            row_keys = list(table.rows.keys())
            
            if row_index < 0 or row_index >= len(row_keys):
                self.notify("Invalid row selection", severity="error")
                return None
                
            row_key = row_keys[row_index]
            return self.data_manager.get_teacher_by_id(row_key)
        except Exception as e:
            self.notify(f"Error getting selected teacher: {str(e)}", severity="error")
            return None
    
    def _get_selected_faculty(self):
        """Get the currently selected faculty."""
        table = self.query_one("#faculties-table", expect_type=DataTable)
        if table.cursor_row is None:
            self.notify("No faculty selected", severity="warning")
            return None
        
        try:
            row_index = table.cursor_row
            row_keys = list(table.rows.keys())
            
            if row_index < 0 or row_index >= len(row_keys):
                self.notify("Invalid row selection", severity="error")
                return None
                
            row_key = row_keys[row_index]
            return self.data_manager.get_faculty_by_id(row_key)
        except Exception as e:
            self.notify(f"Error getting selected faculty: {str(e)}", severity="error")
            return None
    
    # Action methods
    async def action_add_entity(self) -> None:
        """Add an entity based on current tab."""
        if self.current_tab == "students":
            await self._add_student()
        elif self.current_tab == "teachers":
            await self._add_teacher()
        else:
            await self._add_faculty()
    
    async def _add_student(self) -> None:
        """Show the add student modal."""
        def on_save_callback(student):
            self.data_manager.add_student(student)
            self._load_students()
        
        modal = AddEditStudentModal(on_save_callback=on_save_callback)
        await self.push_screen(modal)
    
    async def _add_teacher(self) -> None:
        """Show the add teacher modal."""
        def on_save_callback(teacher):
            self.data_manager.add_teacher(teacher)
            self._load_teachers()
        
        modal = AddEditTeacherModal(on_save_callback=on_save_callback)
        await self.push_screen(modal)
    
    async def _add_faculty(self) -> None:
        """Show the add faculty modal."""
        def on_save_callback(faculty):
            self.data_manager.add_faculty(faculty)
            self._load_faculties()
        
        modal = AddEditFacultyModal(on_save_callback=on_save_callback)
        await self.push_screen(modal)
    
    async def action_edit_entity(self) -> None:
        """Edit an entity based on current tab."""
        if self.current_tab == "students":
            await self._edit_student()
        elif self.current_tab == "teachers":
            await self._edit_teacher()
        else:
            await self._edit_faculty()
    
    async def _edit_student(self) -> None:
        """Show the edit student modal."""
        student = self._get_selected_student()
        if not student:
            return
        
        def on_save_callback(updated_student):
            self.data_manager.update_student(updated_student)
            self._load_students()
            self.notify(f"Updated student: {updated_student.full_name()}")
        
        modal = AddEditStudentModal(edit_student=student, on_save_callback=on_save_callback)
        await self.push_screen(modal)
    
    async def _edit_teacher(self) -> None:
        """Show the edit teacher modal."""
        teacher = self._get_selected_teacher()
        if not teacher:
            return
        
        def on_save_callback(updated_teacher):
            self.data_manager.update_teacher(updated_teacher)
            self._load_teachers()
            self.notify(f"Updated teacher: {updated_teacher.full_name()}")
        
        modal = AddEditTeacherModal(edit_teacher=teacher, on_save_callback=on_save_callback)
        await self.push_screen(modal)
    
    async def _edit_faculty(self) -> None:
        """Show the edit faculty modal."""
        faculty = self._get_selected_faculty()
        if not faculty:
            return
        
        def on_save_callback(updated_faculty):
            self.data_manager.update_faculty(updated_faculty)
            self._load_faculties()
            self.notify(f"Updated faculty: {updated_faculty.name}")
        
        modal = AddEditFacultyModal(edit_faculty=faculty, on_save_callback=on_save_callback)
        await self.push_screen(modal)
    
    async def action_delete_entity(self) -> None:
        """Delete an entity based on current tab."""
        if self.current_tab == "students":
            await self._delete_student()
        elif self.current_tab == "teachers":
            await self._delete_teacher()
        else:
            await self._delete_faculty()
    
    async def _delete_student(self) -> None:
        """Delete the selected student."""
        if self.deletion_in_progress:
            return
            
        student = self._get_selected_student()
        if not student:
            return
        
        self.deletion_in_progress = True
        
        def on_confirm_callback(student_to_delete):
            if self.data_manager.delete_student(student_to_delete.id):
                self._load_students()
                self.notify(f"Deleted student: {student_to_delete.full_name()}")
            else:
                self.notify("Failed to delete student", severity="error")
            self.deletion_in_progress = False
        
        def on_dismiss():
            self.deletion_in_progress = False
            
        modal = DeleteConfirmationModal(student, on_confirm_callback=on_confirm_callback)
        modal.on_dismiss = on_dismiss
        await self.push_screen(modal)
    
    async def _delete_teacher(self) -> None:
        """Delete the selected teacher."""
        if self.deletion_in_progress:
            return
            
        teacher = self._get_selected_teacher()
        if not teacher:
            return
        
        self.deletion_in_progress = True
        
        def on_confirm_callback(teacher_to_delete):
            if self.data_manager.delete_teacher(teacher_to_delete.id):
                self._load_teachers()
                self.notify(f"Deleted teacher: {teacher_to_delete.full_name()}")
            else:
                self.notify("Failed to delete teacher", severity="error")
            self.deletion_in_progress = False
            
        def on_dismiss():
            self.deletion_in_progress = False
            
        modal = DeleteTeacherConfirmationModal(teacher, on_confirm_callback=on_confirm_callback)
        modal.on_dismiss = on_dismiss
        await self.push_screen(modal)
    
    async def _delete_faculty(self) -> None:
        """Delete the selected faculty."""
        if self.deletion_in_progress:
            return
            
        faculty = self._get_selected_faculty()
        if not faculty:
            return
        
        self.deletion_in_progress = True
        
        def on_confirm_callback(faculty_to_delete):
            if self.data_manager.delete_faculty(faculty_to_delete.id):
                self._load_faculties()
                self.notify(f"Deleted faculty: {faculty_to_delete.name}")
            else:
                self.notify("Failed to delete faculty", severity="error")
            self.deletion_in_progress = False
            
        def on_dismiss():
            self.deletion_in_progress = False
            
        modal = DeleteFacultyConfirmationModal(faculty, on_confirm_callback=on_confirm_callback)
        modal.on_dismiss = on_dismiss
        await self.push_screen(modal)
    
    def action_focus_search(self) -> None:
        """Focus the search input."""
        self.query_one("#search-input", expect_type=Input).focus()
    
    def action_refresh(self) -> None:
        """Refresh the current entity list."""
        if self.current_tab == "students":
            self._load_students()
            self.notify("Refreshed student list")
        elif self.current_tab == "teachers":
            self._load_teachers()
            self.notify("Refreshed teacher list")
        else:
            self._load_faculties()
            self.notify("Refreshed faculty list")
    
    @on(Button.Pressed, "#add-button")
    def on_add_button(self) -> None:
        """Handle the add button press."""
        self.app.set_timer(0.01, self.action_add_entity)
    
    @on(Button.Pressed, "#edit-button")
    def on_edit_button(self) -> None:
        """Handle the edit button press."""
        self.app.set_timer(0.01, self.action_edit_entity)
    
    @on(Button.Pressed, "#delete-button")
    def on_delete_button(self) -> None:
        """Handle the delete button press."""
        self.app.set_timer(0.01, self.action_delete_entity)
    
    @on(Button.Pressed, "#search-button")
    def on_search_button(self) -> None:
        """Handle the search button press."""
        self._perform_search()
    
    @on(Input.Submitted, "#search-input")
    def on_search_submitted(self) -> None:
        """Handle when the user presses Enter in the search input."""
        self._perform_search()
    
    @on(Button.Pressed, "#students-tab")
    def on_students_tab_pressed(self) -> None:
        """Handle students tab button press."""
        self._switch_tab("students")
    
    @on(Button.Pressed, "#teachers-tab")
    def on_teachers_tab_pressed(self) -> None:
        """Handle teachers tab button press."""
        self._switch_tab("teachers")
    
    @on(Button.Pressed, "#faculties-tab")
    def on_faculties_tab_pressed(self) -> None:
        """Handle faculties tab button press."""
        self._switch_tab("faculties")
    
    def _perform_search(self) -> None:
        """Search for entities based on current tab."""
        query = self.query_one("#search-input", expect_type=Input).value
        
        if not query:
            self.action_refresh()
            return
            
        if self.current_tab == "students":
            self._search_students(query)
        elif self.current_tab == "teachers":
            self._search_teachers(query)
        else:
            self._search_faculties(query)
    
    def _search_students(self, query: str) -> None:
        """Search students and update table."""
        table = self.query_one("#students-table", expect_type=DataTable)
        table.clear()
        
        results = self.data_manager.search_students(query)
        
        for student in results:
            table.add_row(
                student.full_name(),
                str(student.age),
                student.major,
                f"{student.gpa:.2f}",
                key=student.id
            )
        
        self.notify(f"Found {len(results)} matching students")
    
    def _search_teachers(self, query: str) -> None:
        """Search teachers and update table."""
        table = self.query_one("#teachers-table", expect_type=DataTable)
        table.clear()
        
        results = self.data_manager.search_teachers(query)
        
        for teacher in results:
            table.add_row(
                teacher.full_name(),
                str(teacher.age),
                teacher.department,
                teacher.title,
                key=teacher.id
            )
        
        self.notify(f"Found {len(results)} matching teachers")
    
    def _search_faculties(self, query: str) -> None:
        """Search faculties and update table."""
        table = self.query_one("#faculties-table", expect_type=DataTable)
        table.clear()
        
        results = self.data_manager.search_faculties(query)
        
        for faculty in results:
            table.add_row(
                faculty.name,
                faculty.building,
                faculty.head_name,
                str(faculty.established_year),
                str(faculty.num_staff),
                key=faculty.id
            )
        
        self.notify(f"Found {len(results)} matching faculties")


def main():
    """Run the application."""
    app = StudentManagerApp()
    app.run()


if __name__ == "__main__":
    main()