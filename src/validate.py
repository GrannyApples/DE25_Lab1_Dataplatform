from pydantic import BaseModel, validator, ValidationError, field_validator
from typing import Optional
from datetime import datetime, date


##mitt försök för att få pydantic att fungera, mycket hjälp ifrån LLM för pydantic.
class Product(BaseModel):
    id: Optional[str]
    name: Optional[str]
    price: Optional[float]
    currency: Optional[str]
    created_at: Optional[date]

    @validator("price", pre=True)
    def convert_price(cls, v):
        if v is None or "":
            raise ValueError("Price is null")
        # Convert "free" to 0 or other strings to None
        # the free = 0 happens before validation since we are using pre=True, and thus the free prices will be converted into
        # 0 and placed into products.json as price=0 instead of price=free, the rest will land in the rejected.json
        if isinstance(v, str):
            v_stripped = v.strip().lower()
            if v_stripped in ["", "not_available", "null"]:
                raise ValueError("Price is invalid")
            if v_stripped == "free":
                return 0
        return v
    ##check positive price
    @validator("price")
    def price_positive(cls, v):
        if v is not None and v < 0:
            raise ValueError("Negative price")
        return v


    # ensure ID exists
    @validator("id")
    def id_exist(cls, v):
        if not v or not v.strip():
            raise ValueError("Missing ID")
        return v.strip()

    # same but for name
    @validator("name")
    def name_exist(cls, v):
        if not v or not v.strip():
            raise ValueError("Missing name")
        return v.strip()

    # check for SEK to be currency
    @validator("currency")
    def currency_check_sek(cls, v):
        if not v or v.strip().upper() != "SEK":
            raise ValueError(f"Invalid currency: {v}")
        return v.strip().upper()

    # this is just me asking an llm to check created at cause i couldnt figure this one out myself. aint no way.
    #can porbably update this to convert to the format you want, altho at that point im sure pandas has something to just convert the format
    # or maybe python has something alrdy built in to convert datetimes for certain, since im using V2 pydantic, the created parsing
    #needs to have field_validator, since the validator is deprecated for this.


    ##i am not expecting to be graded on this validator since im just playing around with LLMs at this point seeing what
    ## can be used.
    @field_validator("created_at", mode="before")
    def parse_created_at(cls, v):
        if not v or str(v).strip() == "":
            return None
        v = str(v).strip()
        # try multiple formats
        for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
            try:
                return datetime.strptime(v, fmt).date()
            except ValueError:
                continue
        # invalid date (like 2024-13-01) will raise
        raise ValueError(f"Invalid date format: {v}")