from dataclasses import dataclass
from typing import Optional
import uuid


@dataclass
class Student:
    """Represents a university student."""
    first_name: str
    last_name: str
    age: int
    major: str
    gpa: float
    id: str = None

    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())

    def full_name(self) -> str:
        """Return student's full name."""
        return f"{self.first_name} {self.last_name}"
    
    def to_dict(self) -> dict:
        """Convert student object to dictionary for storage."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "major": self.major,
            "gpa": self.gpa
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Student":
        """Create a Student instance from dictionary data."""
        return cls(
            id=data.get("id"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            age=data.get("age"),
            major=data.get("major"),
            gpa=data.get("gpa")
        )


@dataclass
class Teacher:
    """Represents a university teacher."""
    first_name: str
    last_name: str
    age: int
    department: str
    title: str  # e.g., "Professor", "Assistant Professor", etc.
    id: str = None
    
    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())
            
    def full_name(self) -> str:
        """Return teacher's full name."""
        return f"{self.first_name} {self.last_name}"
    
    def to_dict(self) -> dict:
        """Convert teacher object to dictionary for storage."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "department": self.department,
            "title": self.title
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Teacher":
        """Create a Teacher instance from dictionary data."""
        return cls(
            id=data.get("id"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            age=data.get("age"),
            department=data.get("department"),
            title=data.get("title")
        )


@dataclass
class Faculty:
    """Represents a university faculty/department."""
    name: str
    building: str
    head_name: str
    established_year: int
    num_staff: int
    id: str = None
    
    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())
    
    def to_dict(self) -> dict:
        """Convert faculty object to dictionary for storage."""
        return {
            "id": self.id,
            "name": self.name,
            "building": self.building,
            "head_name": self.head_name,
            "established_year": self.established_year,
            "num_staff": self.num_staff
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Faculty":
        """Create a Faculty instance from dictionary data."""
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            building=data.get("building"),
            head_name=data.get("head_name"),
            established_year=data.get("established_year"),
            num_staff=data.get("num_staff")
        )