import pandas as pd



def csv_to_json(input_path, output_path):
    ##Seperate by ; from csv, not sure if this is needed but it works, and pycharm gave me the autocomplete.
    ##orient by records, makes each row in the df become a separate JSON obj, and all rows are put into a list.
    df = pd.read_csv(input_path, sep=";")
    df.to_json(output_path, orient='records', indent=2)