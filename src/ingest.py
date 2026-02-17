import pandas as pd
def csv_tojson(input_path, output_path):
    df = pd.read_csv(input_path, sep=";")
    df.tojson(output_path, orient='records')