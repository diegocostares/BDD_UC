import uuid

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class CourseCatalog(Base):
    __tablename__ = "course_catalog"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String)
    credits = Column(Integer)
    code = Column(String)
    general_area = Column(String)
    syllabus = Column(String)
    academic_level = Column(String)
    description = Column(String)
    restrictions = Column(String)
    prerequisites = Column(String)
    equivalencies = Column(String)
    need_all_requirements = Column(Boolean)
    is_active = Column(Boolean)
    course_sections = relationship("CourseSection", back_populates="course_catalog")


class CourseSection(Base):
    __tablename__ = "course_section"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    nrc = Column(String)
    code = Column(String)
    allows_withdraw = Column(String)
    is_in_english = Column(String)
    section = Column(Integer)
    requires_special_approval = Column(String)
    fg_area = Column(String)
    format = Column(String)
    category = Column(String)
    name = Column(String)
    campus = Column(String)
    credits = Column(Integer)
    current_semester = Column(String)
    course_id = Column(UUID, ForeignKey("course_catalog.id"))
    course_catalog = relationship("CourseCatalog", back_populates="course_sections")
    schedules = relationship("CourseSectionSchedule", back_populates="course_section")
    teachers = relationship("CourseTeacher", back_populates="course_section")
    banner_vacancies = relationship("CourseSectionBannerVacancy", back_populates="course_section")


class CourseSectionSchedule(Base):
    __tablename__ = "course_section_schedule"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    type = Column(String)
    day = Column(String)
    module = Column(Integer)
    classroom = Column(String)
    course_section_id = Column(UUID, ForeignKey("course_section.id"))
    course_section = relationship("CourseSection", back_populates="schedules")


class Teacher(Base):
    __tablename__ = "teacher"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String)
    email = Column(String)
    photo_url = Column(String)
    website = Column(String)
    course_teachers = relationship("CourseTeacher", back_populates="teacher")


class CourseTeacher(Base):
    __tablename__ = "course_teacher"

    # TODO: revisar
    # TODO: revisar el , default=uuid.uuid4
    course_section_id = Column(UUID, ForeignKey("course_section.id"), primary_key=True, default=uuid.uuid4)
    teacher_id = Column(UUID, ForeignKey("teacher.id"), primary_key=True, default=uuid.uuid4)
    course_section = relationship("CourseSection", back_populates="teachers")
    teacher = relationship("Teacher", back_populates="course_teachers")


class CourseSectionBannerVacancy(Base):
    __tablename__ = "course_section_banner_vacancy"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    course_section_id = Column(UUID, ForeignKey("course_section.id"))
    banner = Column(Integer)
    course_section = relationship("CourseSection", back_populates="banner_vacancies")
    vacancy_details = relationship("VacancyDetail", back_populates="course_section_banner_vacancy")


class VacancyDetail(Base):
    __tablename__ = "vacancy_detail"

    course_section_banner_vacancy_id = Column(
        UUID, ForeignKey("course_section_banner_vacancy.id"), primary_key=True, default=uuid.uuid4
    )
    school = Column(String)
    level = Column(String)
    program = Column(String)
    concentration = Column(String)
    cohort = Column(String)
    admission_period = Column(String)
    offered = Column(Integer)
    occupied = Column(Integer)
    available = Column(Integer)
    course_section_banner_vacancy = relationship("CourseSectionBannerVacancy", back_populates="vacancy_details")
