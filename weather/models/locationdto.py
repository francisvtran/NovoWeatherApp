from typing import TypedDict

class LocationDTO(TypedDict):     
    city: str
    temp_min: float
    temp_max: float
    icon: str