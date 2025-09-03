from sqlalchemy.types import TypeDecorator, String
import re

class Email(TypeDecorator):
    impl = String(255)

    def process_bind_param(self, value, dialect):
        if value is not None:
            pattern = r"^[^@]+@[^@]+\.[^@]+$"
            if not re.match(pattern, value):
                raise ValueError(f"Invalid email: {value}")
        return value