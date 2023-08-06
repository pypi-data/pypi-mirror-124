from .base import BaseModel

class IntakeV3Response(BaseModel):

    def __init__(self,
        item=None
    ):

        super().__init__()

        self.item = item if item else IntakeV3ResponseItem()

class IntakeV3ResponseItem(BaseModel):

    def __init__(self,
        up_doc_ref=None
    ):

        super().__init__()

        self.up_doc_ref = up_doc_ref