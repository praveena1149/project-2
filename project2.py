import pandas as pd
import pymysql
import sqlalchemy as sqlalchemy
from sqlalchemy import create_engine


df=pd.read_csv(r'"C:\Users\91636\Downloads\project2_cleaned.csv"')

try:
    # Connection Parameters
    connection1 = pymysql.connect(
         host = 'localhost', user = 'root', 
         password = '12345', database = 'project2')
    print("connection = ", connection1)
    cursor = connection1.cursor()
    print("cursor = ", cursor)  
    
except Exception as e:
    print(str(e))


engine=create_engine("mysql+pymysql://root:12345@localhost/project2")

df.to_sql(
    name='fooddelivery',        # table name
    con=engine,
    if_exists='append',     # insert data (no overwrite)
    index=False             # avoid DataFrame index column
)

print('data inserted sucessfully')
