from wikitables import import_tables
from pandas import DataFrame
import pandas as pd

tables = import_tables('Opinion polling in the 2019 Canadian federal election') #returns a list of WikiTable objects

def get_federal_2019():
    table = import_tables('Opinion polling in the 2019 Canadian federal election')[0]
    polling_results = []
    for row in table.rows:
        ## Ignore empty rows
        if "Last dateof polling" in row.keys():
            result = []
            result.append(row["Polling firm"])
            result.append(row["Last dateof polling"])
            result.append(row["CPC"])
            result.append(row["LPC"])
            result.append(row["NDP"])
            result.append(row["BQ"])
            result.append(row["GPC"])
            result.append(row["PPC"])
            result.append(row["Samplesize"])
            result.append(row["Polling method"])
            result.append(row["Lead"])
            ## Once we know when the campaign period is, change this
            result.append(False)
            polling_results.append(result)
    return pd.DataFrame.from_records(polling_results, columns=["Source", "Date", "Conservative", "Liberal", "NDP", "Bloc QC", "Green", "Other", "Sample", "Type", "Margin", "Campaign"])
    

get_federal_2019().to_csv("./data/raw/2019 Federal Polling.csv")