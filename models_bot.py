from pydantic import BaseModel

class Place(BaseModel):
    name:str
    city:str
    description:str
    rating:float
    google:str
    poster:str