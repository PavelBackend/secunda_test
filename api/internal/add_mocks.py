import asyncio
from sqlalchemy import func, cast
from geoalchemy2 import Geography
from api.database import async_session_maker
from api.internal.orm_models.dao import Organization, Building, Activity, Phone


async def seed():
    async with async_session_maker() as session:
        # --- Buildings ---
        b1 = Building(
            address="Main Street 1",
            location=cast(
                func.ST_SetSRID(func.ST_MakePoint(37.618423, 55.751244), 4326),
                Geography,
            ),  # Москва центр
        )
        b2 = Building(
            address="Main Street 2",
            location=cast(
                func.ST_SetSRID(func.ST_MakePoint(37.619000, 55.752000), 4326),
                Geography,
            ),  # рядом с b1
        )
        b3 = Building(
            address="Main Street 3",
            location=cast(
                func.ST_SetSRID(func.ST_MakePoint(30.3350986, 59.9342802), 4326),
                Geography,
            ),  # Питер
        )

        # --- Activities (3 уровня) ---
        a_it = Activity(name="IT Services")
        a_edu = Activity(name="Education")
        a_health = Activity(name="Healthcare")

        a_web = Activity(name="Web Development", parent=a_it)
        a_mobile = Activity(name="Mobile Development", parent=a_it)
        a_school = Activity(name="School Education", parent=a_edu)
        a_university = Activity(name="University Education", parent=a_edu)
        a_clinic = Activity(name="Clinic", parent=a_health)

        a_frontend = Activity(name="Frontend", parent=a_web)
        a_backend = Activity(name="Backend", parent=a_web)
        a_ios = Activity(name="iOS", parent=a_mobile)
        a_android = Activity(name="Android", parent=a_mobile)
        a_primary = Activity(name="Primary School", parent=a_school)
        a_high = Activity(name="High School", parent=a_school)
        a_general = Activity(name="General Medicine", parent=a_clinic)

        # --- Organizations ---
        org1 = Organization(
            name="Test Org 1",
            building=b1,
            activities=[a_web, a_frontend],
        )
        org2 = Organization(
            name="Test Org 2",
            building=b1,
            activities=[a_university, a_high],
        )
        org3 = Organization(
            name="Test Org 3",
            building=b2,
            activities=[a_mobile, a_android],
        )
        org4 = Organization(
            name="Test Org 4",
            building=b3,
            activities=[a_clinic, a_general],
        )
        org5 = Organization(
            name="Test Org 5",
            building=b3,
            activities=[a_school, a_primary],
        )

        # --- Phones ---
        phones = [
            Phone(number="+7-999-111-1111", organization=org1),
            Phone(number="+7-999-222-2222", organization=org1),
            Phone(number="+7-999-333-3333", organization=org2),
            Phone(number="+7-999-444-4444", organization=org3),
            Phone(number="+7-999-555-5555", organization=org4),
            Phone(number="+7-999-666-6666", organization=org5),
        ]

        session.add_all([org1, org2, org3, org4, org5, *phones])
        await session.commit()
