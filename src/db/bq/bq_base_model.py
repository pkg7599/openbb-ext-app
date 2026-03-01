from typing import ClassVar

from pydantic import BaseModel


class BigQueryModel(BaseModel):
    __table__: ClassVar[str]

    def to_bq_dict(self) -> dict:
        return self.model_dump(exclude_none=True)
