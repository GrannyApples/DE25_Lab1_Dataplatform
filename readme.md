Added file structure based on LLM to know the proper setup in a python pipeline.
Some file names is not what i would have made myself most likely, altho data is commonly used in .NET aswell,
current structure is alot more formed after python.

This lab is somewhat overengineered but im just trying to learn the proper file structure for a project like this in the future.

It might not follow the actual guidelines we learned in lecture 7 and 8, but after having done this project in a single main.py,
i just felt i kinda needed to explore a proper structure.

So i implemented a mini data pipeline with a schema validation and staging layers to simulate a more proper workflow.


I am just gonna state this here, the way pydantic handles null values is garbage when it comes to float, it doesnt work at all. I can catch alot of things with the validation in transform, and it just wont catch price = null, but the analyze part of the code does catch it when running pandas.

I tried alot of different things but i cant get anything to work, this is concerning SKU-1006, And from what i found, it has to do with the way pydantic converts float values.

Now i think i just figured it out, the validator is parsing "" to None, but it does not update before the next check for validation, is my hypothesis.

The validation will convert or reject things that dont look right, and then the analyze will make sure its correct.

I could update it so that the validation is actually just catching everything. But if i did that i wouldnt be able to show how important it might be to explore edgecases in the differences with pydantic and manual testing.

And why you test, and then test again.
```json
SKU-1006;designer coat;;SEK;2024-05-01
 {
    "id":"SKU-1006",
    "name":"designer coat",
    "price":null,
    "currency":"SEK",
    "created_at":"2024-05-01"
  }
```

The pandas version will catch it.
**in analyze** 
```python
 rejected = df[
        df["id"].isna() |
        df["name"].isna() |
        df["price"].isna() |
        (df["price"] < 0)
    ]

rejected.to_json(REJECTED_ANALYSIS, orient="records", indent=2)
```

This will not.
**In Validate**
```python
@validator("price", pre=True)
    def convert_price(cls, v):
        if isinstance(v, str):
            v = v.strip().lower()
            if v in ["", "not_available"]:
                return None
            if v in ["free"]:
                return 0
        return v
    ##check positive price
    @validator("price")
    def price_positive(cls, v):
        if v is not None and v < 0:
            raise ValueError("Negative price")
        return v
```
If i update the code to this other verison,
it still doesnt work with pydantic,
    you would expect it to since you catch it before you convert anything.
```python
@validator("price", pre=True)
def convert_price(cls, v):
    # Reject invalid or missing prices
    if v is None or "":
        raise ValueError("Price is null")
    if isinstance(v, str):
        v_stripped = v.strip().lower()
        if v_stripped in ["", "not_available", "null"]:
            raise ValueError("Price is invalid")
        if v_stripped == "free":
            return 0
    return v
```
What you need to do is make a check in the transform layer,
to check for null on manual price.

```python

for record in df.to_dict(orient="records"):
    if pd.isna(record.get("price")):
            rejected_records.append(record)
        continue
```

Now if we wanted to make this even better we can grab the basemodel to isolate the float values, 
and since we know this is an issue with pydantic and float values,
we can make something like 
```python

from validate import Product, ValidationError

 float_fields = [
        name for name, type_ in Product.__annotations__.items()
        if getattr(type_, "__origin__", None) is not None and float in getattr(type_, "__args__", ())
    ]
 
    for record in df.to_dict(orient="records"):
        if any(record.get(f) is None or pd.isna(record.get(f)) for f in float_fields):
            rejected_records.append(record)
            continue

```
This version does work, and i would assume you could reuse this for any basemodel where you use 
pydantic and floats.

Teori:

Ingest = ta in rådata från källa i.e products.csv

storage = spara rådata, ie data/processed.json

transform = rensa, konvertera och validera data. transform/clean_data function.

access = allt i data/outputs ie analyser, rapporter och göra datan tillgänglig.


ETL:

Extract Hämta rådata

transform rensa/omvandla data till läsbart format

load Spara data för senare användning, t.ex analys o rapport.