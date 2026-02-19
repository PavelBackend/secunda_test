from geoalchemy2 import Geography
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


organization_activity = Table(
    "organization_activity",
    Base.metadata,
    Column("organization_id", ForeignKey("organization.id"), primary_key=True),
    Column("activity_id", ForeignKey("activity.id"), primary_key=True),
)


class Organization(Base):
    __tablename__ = "organization"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    phones: Mapped[list["Phone"]] = relationship("Phone", back_populates="organization", cascade="all, delete-orphan")

    building_id: Mapped[int] = mapped_column(ForeignKey("building.id"), nullable=False)
    building: Mapped["Building"] = relationship("Building", back_populates="organizations")

    activities: Mapped[list["Activity"]] = relationship(
        "Activity", secondary=organization_activity, back_populates="organizations"
    )


class Phone(Base):
    __tablename__ = "phone"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    number: Mapped[str] = mapped_column(String, nullable=False)

    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"), nullable=False)
    organization: Mapped["Organization"] = relationship("Organization", back_populates="phones")


class Building(Base):
    __tablename__ = "building"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    location = mapped_column(Geography(geometry_type="POINT", srid=4326), nullable=False)

    organizations: Mapped[list["Organization"]] = relationship("Organization", back_populates="building")

    @property
    def lat(self) -> float | None:
        if self.location is None:
            return None
        from geoalchemy2.shape import to_shape

        return to_shape(self.location).y

    @property
    def lon(self) -> float | None:
        if self.location is None:
            return None
        from geoalchemy2.shape import to_shape

        return to_shape(self.location).x


class Activity(Base):
    __tablename__ = "activity"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    parent_id: Mapped[int | None] = mapped_column(ForeignKey("activity.id"), nullable=True)
    children: Mapped[list["Activity"]] = relationship("Activity", back_populates="parent", cascade="all, delete-orphan")
    parent: Mapped["Activity | None"] = relationship("Activity", back_populates="children", remote_side=[id])

    organizations: Mapped[list["Organization"]] = relationship(
        "Organization", secondary=organization_activity, back_populates="activities"
    )
