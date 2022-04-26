SOURCE_FOLDER = "input_data/"
import os 
import pandas as pd 
from time import sleep


def query_historic():
    historic = pd.read_csv("historic.csv")
    historic_copy = historic.copy()
   
    customer_id_most_updates = historic_copy['customer_id'].value_counts().index.tolist()[0]    
    customer_most_updates=historic_copy.loc[(historic_copy.customer_id == customer_id_most_updates)]
   # print("\n\n--------------------MOST UPDATE--------------------")                 
   # print(customer_most_updates)
    customer_most_updates.to_csv("customer_most_updates.csv", index=False)
    

def query_database():
    
    database = pd.read_csv("database.csv")
    database_copy = database.copy()
    
    most_balance = database_copy['balance'].sort_values(ascending=False)[:5].tolist()
    customers_most_balance = database_copy[database_copy['balance'].isin(most_balance)]
  #  print("\n\n--------------------MOST 5 BALANCE--------------------")                 
  #  print(customers_most_balance)
    customers_most_balance.to_csv("customers_most_balance.csv", index=False)
    
    
    customers_last_timestamp = database_copy[database_copy['op']=='u'] \
        .sort_values(by=['update_timestamp'],ascending=False)[:5]
   # print("\n\n--------------------MOST 5 UPDATE TIME--------------------")                 
   # print(customers_last_timestamp)
    customers_last_timestamp.to_csv("customers_last_timestamp.csv", index=False)
    
    
    customers_total_balance = database_copy["balance"].sum()
   # print("\n\n--------------------TOTAL BALANCE--------------------")                 
   # print(customers_total_balance) 
    f = open("customers_total_balance.txt", "w")
    f.write(str(customers_total_balance))
    f.close()   
    

def insert_data(database, insert_row):

    database=pd.concat([database, insert_row.to_frame().T], ignore_index=True)
    return database


def update_data(database, update_row):
    
    database.loc[(database.customer_id == update_row["customer_id"]), \
        ['op', 'balance', 'create_timestamp', 'update_timestamp']]= \
        [update_row["op"], update_row["balance"], update_row["create_timestamp"], \
        update_row["update_timestamp"]]
   
    return database


def read_and_write_files():
    """

    """
    customers_files = os.listdir(SOURCE_FOLDER)
    database = pd.DataFrame()
    historic = pd.DataFrame()
    
    
    
    for account_csv in customers_files:
        data_bank = pd.read_csv(SOURCE_FOLDER+account_csv)
        for rows in data_bank.iterrows():
            if rows[1][0] == "i":
                insert_row=rows[1]
                database=insert_data(database, insert_row)
                historic=pd.concat([historic, insert_row.to_frame().T], ignore_index=True)
                
            else:
                update_row=rows[1]
                database=update_data(database, update_row)
                historic=pd.concat([historic, update_row.to_frame().T], ignore_index=True)
   
    
    database.to_csv("database.csv", index=False)
    historic.to_csv("historic.csv", index=False)
    sleep(2)  


def main():
	read_and_write_files()
	query_database()
	query_historic()
	sleep(5)

main()
