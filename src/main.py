import pandas as pd


if __name__ == '__main__':
    ##Plockar in csv filen, och konverterar till json enligt instruktioner att det ska läsas som .json fil
    # #Ingest...
    df = pd.read_csv('../data/products.csv', sep=";")

    df.to_json('data/products.json', orient='records')

    df = pd.read_json('data/products.json')

    ####################
    #