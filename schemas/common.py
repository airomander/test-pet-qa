from pydantic import BaseModel


class Support(BaseModel):
    url: str
    text: str
