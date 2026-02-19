from pydantic import BaseModel, ConfigDict


class PhoneOut(BaseModel):
    id: int
    number: str

    model_config = ConfigDict(from_attributes=True)


class BuildingOut(BaseModel):
    id: int
    address: str
    lat: float | None = None
    lon: float | None = None

    model_config = ConfigDict(from_attributes=True)


class ActivityOut(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class OrganizationOut(BaseModel):
    id: int
    name: str
    phones: list[PhoneOut]
    building: BuildingOut
    activities: list[ActivityOut]

    model_config = ConfigDict(from_attributes=True)
