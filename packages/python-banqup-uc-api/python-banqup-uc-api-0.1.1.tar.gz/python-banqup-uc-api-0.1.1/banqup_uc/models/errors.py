from .base import BaseModel

class Error(BaseModel):

    def __init__(self,
        errors=None
    ):

        self.errors = errors