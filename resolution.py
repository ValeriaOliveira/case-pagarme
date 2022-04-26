SOURCE_FOLDER = "input_data/"
import os 
import pandas as pd 
from time import sleep
from pathlib import Path



def query_historic():
    """
    
    """
    historic = pd.read_csv("historic.csv")
    historic_copy = historic.copy()
   
    customer_id_most_updates = historic_copy['customer_id'].value_counts().index.tolist()[0]    
    customer_most_updates=historic_copy.loc[(historic_copy.customer_id == customer_id_most_updates)]

    customer_most_updates.to_csv("customer_most_updates.csv", index=False)
    

def query_database():
    """
    
    """
    database = pd.read_csv("database.csv")
    database_copy = database.copy()
    
    #---------------------------------------------------------------------------------#
    most_balance = database_copy['balance'].sort_values(ascending=False)[:5].tolist()
    customers_most_balance = database_copy[database_copy['balance'].isin(most_balance)]

    customers_most_balance.to_csv("customers_most_balance.csv", index=False)
    
    #---------------------------------------------------------------------------------#
    customers_last_timestamp = database_copy[database_copy['op']=='u'] \
        .sort_values(by=['update_timestamp'],ascending=False)[:5]

    customers_last_timestamp.to_csv("customers_last_timestamp.csv", index=False)
    
    #---------------------------------------------------------------------------------#    
    customers_total_balance = database_copy["balance"].sum()

    f = open("customers_total_balance.txt", "w")
    f.write(str(customers_total_balance))
    f.close()   
    

def insert_data(database, insert_row):
    """
    
    """

    database=pd.concat([database, insert_row.to_frame().T], ignore_index=True)
    return database


def update_data(database, update_row):
    """
    
    """
    
    database.loc[(database.customer_id == update_row["customer_id"]), \
        ['op', 'balance', 'create_timestamp', 'update_timestamp']]= \
        [update_row["op"], update_row["balance"], update_row["create_timestamp"], \
        update_row["update_timestamp"]]
   
    return database


def read_and_write_files():
    """

    """
    customers_files = sorted(Path(SOURCE_FOLDER).iterdir(), key=lambda files: files.stat().st_mtime)

    database = pd.DataFrame()
    historic = pd.DataFrame()    
    for accounts in customers_files:
        raw_data = pd.read_csv(accounts)
        for rows in raw_data.iterrows():
            row = rows[1]
            historic = pd.concat([historic, row.to_frame().T], ignore_index=True)	
            if rows[1][0] == "i":
                database = insert_data(database, row)
            else:
                database = update_data(database, row)
   
    database.to_csv("database.csv", index=False)
    historic.to_csv("historic.csv", index=False)
    sleep(2)  


def main():
	read_and_write_files()
	query_database()
	query_historic()
	sleep(5)

main()
