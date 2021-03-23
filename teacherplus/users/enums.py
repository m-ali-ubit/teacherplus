from enum import Enum


class UserTypeEnum(Enum):
    STUDENT = "STUDENT"
    PARENT = "PARENT"
    TEACHER = "TEACHER"
    INSTITUTE = "INSTITUTE"

    @classmethod
    def get_user_types(cls):
        return [
            cls.STUDENT.value,
            cls.PARENT.value,
            cls.INSTITUTE.value,
            cls.TEACHER.value,
        ]


class GenderEnum(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class ShiftsEnum(Enum):
    MORNING = "MORNING"
    EVENING = "EVENING"


class JobTypeEnum(Enum):
    PART_TIME = "PART_TIME"
    FULL_TIME = "FULL_TIME"


class AvailabilityEnum(Enum):
    PRIVATE = "PRIVATE"
    GROUP = "GROUP"
    ONLINE = "ONLINE"
    CENTRE = "CENTRE"


class EmploymentTypeEnum(Enum):
    PART_TIME = "PART_TIME"
    FULL_TIME = "FULL_TIME"
    SELF_EMPLOYED = "SELF_EMPLOYED"
    FREELANCE = "FREELANCE"
    INTERNSHIP = "INTERNSHIP"
