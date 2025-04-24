import json
import os
import importlib
from typing import List, Optional


class DataManager:
    """Manages the storage and retrieval of university data."""
    
    def __init__(self, data_dir: str = None):
        """Initialize the data manager with the specified data directory."""
        # Use absolute path based on the script location
        if data_dir is None:
            self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        else:
            self.data_dir = data_dir
            
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir, exist_ok=True)
            
        # Define file paths
        self.student_file = os.path.join(self.data_dir, "students.json")
        self.teacher_file = os.path.join(self.data_dir, "teachers.json")
        self.faculty_file = os.path.join(self.data_dir, "faculties.json")
        
        # Initialize data lists
        self.students = []
        self.teachers = []
        self.faculties = []
        
        # Load all data
        self._load_data()
        
    def _load_data(self) -> None:
        """Load all data from JSON files."""
        from models import Student, Teacher, Faculty
        
        # Load students
        if os.path.exists(self.student_file):
            try:
                with open(self.student_file, "r") as f:
                    data = json.load(f)
                    self.students = [Student.from_dict(item) for item in data]
            except json.JSONDecodeError:
                self.students = []
        else:
            self._save_students()
            
        # Load teachers
        if os.path.exists(self.teacher_file):
            try:
                with open(self.teacher_file, "r") as f:
                    data = json.load(f)
                    self.teachers = [Teacher.from_dict(item) for item in data]
            except json.JSONDecodeError:
                self.teachers = []
        else:
            self._save_teachers()
            
        # Load faculties
        if os.path.exists(self.faculty_file):
            try:
                with open(self.faculty_file, "r") as f:
                    data = json.load(f)
                    self.faculties = [Faculty.from_dict(item) for item in data]
            except json.JSONDecodeError:
                self.faculties = []
        else:
            self._save_faculties()
    
    # Student methods
    def _save_students(self) -> None:
        """Save student data to JSON file."""
        data = [student.to_dict() for student in self.students]
        with open(self.student_file, "w") as f:
            json.dump(data, f, indent=4)
    
    def get_all_students(self) -> List:
        """Return all students."""
        return self.students
    
    def add_student(self, student) -> None:
        """Add a new student."""
        self.students.append(student)
        self._save_students()
    
    def get_student_by_id(self, student_id: str):
        """Get a student by ID."""
        for student in self.students:
            if student.id == student_id:
                return student
        return None
    
    def update_student(self, student) -> bool:
        """Update an existing student."""
        for i, existing_student in enumerate(self.students):
            if existing_student.id == student.id:
                self.students[i] = student
                self._save_students()
                return True
        return False
    
    def delete_student(self, student_id: str) -> bool:
        """Delete a student by ID."""
        for i, student in enumerate(self.students):
            if student.id == student_id:
                del self.students[i]
                self._save_students()
                return True
        return False
    
    def search_students(self, query: str) -> List:
        """Search students by name or major."""
        query = query.lower()
        results = []
        for student in self.students:
            if (query in student.first_name.lower() or 
                query in student.last_name.lower() or 
                query in student.major.lower()):
                results.append(student)
        return results
        
    # Teacher methods
    def _save_teachers(self) -> None:
        """Save teacher data to JSON file."""
        data = [teacher.to_dict() for teacher in self.teachers]
        with open(self.teacher_file, "w") as f:
            json.dump(data, f, indent=4)
    
    def get_all_teachers(self) -> List:
        """Return all teachers."""
        return self.teachers
    
    def add_teacher(self, teacher) -> None:
        """Add a new teacher."""
        self.teachers.append(teacher)
        self._save_teachers()
    
    def get_teacher_by_id(self, teacher_id: str):
        """Get a teacher by ID."""
        for teacher in self.teachers:
            if teacher.id == teacher_id:
                return teacher
        return None
    
    def update_teacher(self, teacher) -> bool:
        """Update an existing teacher."""
        for i, existing_teacher in enumerate(self.teachers):
            if existing_teacher.id == teacher.id:
                self.teachers[i] = teacher
                self._save_teachers()
                return True
        return False
    
    def delete_teacher(self, teacher_id: str) -> bool:
        """Delete a teacher by ID."""
        for i, teacher in enumerate(self.teachers):
            if teacher.id == teacher_id:
                del self.teachers[i]
                self._save_teachers()
                return True
        return False
    
    def search_teachers(self, query: str) -> List:
        """Search teachers by name, department or title."""
        query = query.lower()
        results = []
        for teacher in self.teachers:
            if (query in teacher.first_name.lower() or 
                query in teacher.last_name.lower() or 
                query in teacher.department.lower() or
                query in teacher.title.lower()):
                results.append(teacher)
        return results
        
    # Faculty methods
    def _save_faculties(self) -> None:
        """Save faculty data to JSON file."""
        data = [faculty.to_dict() for faculty in self.faculties]
        with open(self.faculty_file, "w") as f:
            json.dump(data, f, indent=4)
    
    def get_all_faculties(self) -> List:
        """Return all faculties."""
        return self.faculties
    
    def add_faculty(self, faculty) -> None:
        """Add a new faculty."""
        self.faculties.append(faculty)
        self._save_faculties()
    
    def get_faculty_by_id(self, faculty_id: str):
        """Get a faculty by ID."""
        for faculty in self.faculties:
            if faculty.id == faculty_id:
                return faculty
        return None
    
    def update_faculty(self, faculty) -> bool:
        """Update an existing faculty."""
        for i, existing_faculty in enumerate(self.faculties):
            if existing_faculty.id == faculty.id:
                self.faculties[i] = faculty
                self._save_faculties()
                return True
        return False
    
    def delete_faculty(self, faculty_id: str) -> bool:
        """Delete a faculty by ID."""
        for i, faculty in enumerate(self.faculties):
            if faculty.id == faculty_id:
                del self.faculties[i]
                self._save_faculties()
                return True
        return False
    
    def search_faculties(self, query: str) -> List:
        """Search faculties by name, building, or head name."""
        query = query.lower()
        results = []
        for faculty in self.faculties:
            if (query in faculty.name.lower() or 
                query in faculty.building.lower() or
                query in faculty.head_name.lower()):
                results.append(faculty)
        return results