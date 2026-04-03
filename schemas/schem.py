from pydantic import BaseModel, Field


class SGrade(BaseModel):
    full_name: str
    estimation: int