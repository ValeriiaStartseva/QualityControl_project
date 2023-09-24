from pydantic import ConfigDict, BaseModel


class BaseModelORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)

