from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List, Dict, Any


class SocialMedia(BaseModel):
    social_media: List[str] = Field(description="Social media of person")

    def to_dict(self) -> Dict[str, Any]:
        return {"social_media": self.social_media}


topics_of_interest_parser = PydanticOutputParser(pydantic_object=SocialMedia)
