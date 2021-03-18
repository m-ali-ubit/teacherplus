from enum import Enum


class UserType(Enum):
    STUDENT = "STUDENT"
    PARENT = "PARENT"
    TUTOR = "TUTOR"
    INSTITUTE = "INSTITUTE"

    @classmethod
    def get_user_types(cls):
        return [
            cls.STUDENT.value,
            cls.PARENT.value,
            cls.INSTITUTE.value,
            cls.TUTOR.value,
        ]
