import pandas as pd
from validate import Product, ValidationError

def clean_data(path):
    df = pd.read_json(path)
    ##Went over lambda expressions in lekt 7,
    # did this because it worked better than what we went through during the lecture.

    ##df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
    ##both of these work, both the for loop and the lambda.
    for col in df.select_dtypes(include="object"):
        df[col] = df[col].str.strip()


    ###For the pydantic version as you can see i got alot of help from LLMs
    ## because pydantic in its simplest form, wont flag float "" or float null apparently.
    ##it wasent rly my intention to even use pydantic, but i ended up here anyways to see what the difference was.
    validated_records = []
    rejected_records = []

    ## well i dont need all of this to make it work, it was just from the perspective of,
    # what if i have multiple float values and not just "price"
    float_fields = [
        name for name, type_ in Product.__annotations__.items()
        if getattr(type_, "__origin__", None) is not None and float in getattr(type_, "__args__", ())
    ]
    #DataFrame to dictionary rows and validate
    for record in df.to_dict(orient="records"):
        if any(record.get(f) is None or pd.isna(record.get(f)) for f in float_fields):
            rejected_records.append(record)
            continue

        try:
            p = Product(**record)
            ## need to save as dict for Pandas.
            validated_records.append(p.dict())

        ##This uses the validation from pydantic
        except ValidationError:
            rejected_records.append(record)

    clean_df = pd.DataFrame(validated_records)
    rejected_df = pd.DataFrame(rejected_records)



    return clean_df, rejected_df
    ##########

    ## code below is used without pydantic.


    ##if something is stated as free, it will replace it with 0
    # read later that we should simply flag, and never replace.
    df["price"] = df["price"].replace("free", 0)

    ##errors become NaN previously Free would be NaN since its not numeric, after using replace to swap free to 0, this should not be an issue
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    ##creating new "tables" to sort out missind prices, zero price and luxery prices.
    df["missing_currency"] = df["currency"].isna()
    df["zero_price"] = df["price"] == 0
    df["extreme_price"] = df["price"] > 2500

    return df