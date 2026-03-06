

import pandas as pd
import pymysql
import sqlalchemy as sqlalchemy
from sqlalchemy import create_engine
import streamlit as st


df=pd.read_csv(r"C:\Users\91636\Downloads\project2_cleaned (1).csv")

try:
    # Connection Parameters
    connection5 = pymysql.connect(
         host = 'localhost', user = 'root', 
         password = '12345', database = 'project2')
    print("connection = ", connection5)
    cursor = connection5.cursor()
    print("cursor = ", cursor)  
    
except Exception as e:
    print(str(e))


engine=create_engine("mysql+pymysql://root:12345@localhost/project2")
queries={
    "1. top spending customers":
     """select Customer_ID,SUM(Order_Value) AS total_spent from anaysis group by Customer_ID order by total_spent desc limit 10""",
     
     "2.Analyze age group vs order value":
     """select Age_Group, COUNT(Order_ID) AS total_orders, SUM(Order_Value) AS total_order_value, avg(Order_Value) AS avg_order_value from analysis
     group by Age_Group order by Age_Group desc""",
     
     "3. Weekend vs weekday order patterns":
      """select Order_Day,count(Order_ID) AS TotalOrders  from analysis group by  Order_Day""",
      
    "4.Monthly revenue trends":
     """select DATE_FORMAT(order_date, '%Y-%m') AS month,SUM(Order_Value) AS total_revenue,COUNT(*) AS total_orders from analysis 
     group by month order by month""",
     
    "5.Impact of discounts on profit":
      """select Discount_Applied,count(Order_ID) AS total_orders,AVG(Profit_Margin) AS avg_profit_margin
     from analysis group by  Discount_Applied order by Discount_Applied""",

     "6.High-revenue cities and cuisines":
     """select city,Cuisine_Type,count(Order_ID) AS total_orders,sum(Order_Value) AS total_revenue 
     from analysis group by City,Cuisine_Type order by total_revenue desc""",

    "7.Average delivery time by city":
     """select city, avg(Delivery_Time_Min) as average_delivery_time from analysis group by City""",
     
    "8.Distance vs delivery delay analysis":
     """select Distance_Km,avg(Delivery_Time_Min) AS avg_delivery_time from analysis group by Distance_Km order by avg_delivery_time desc""",
     
     "9.Delivery rating vs delivery time":
     """select Delivery_Time_Min,count(Order_ID) AS total_orders,avg(Delivery_Rating) as avg_delivery_rating
     from analysis group by Delivery_Time_Min order by Delivery_Time_Min""",
     
     "10.Top-rated restaurants":
     """select  Restaurant_ID,Restaurant_Name,count(Order_ID) as total_orders,avg(Delivery_Rating) as avg_rating from analysis
     group by Restaurant_ID, Restaurant_Name order by avg_rating desc limit 10""",

     "11.Cancellation rate by restaurant":
     """select  Restaurant_ID, Restaurant_Name,sum(case when Order_Status = 'Cancelled' then 1 else 0 end) as cancelled_orders,
     round(sum(case when Order_Status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / count(Order_ID),2) as cancellation_rate_percent
     from analysis group by Restaurant_ID, Restaurant_Name having count(Order_ID) >= 2 order by cancellation_rate_percent desc""",
     
     "12.Cuisine-wise performance":
     """select Cuisine_Type,count(Order_ID) as total_orders,sum(Order_Value) AS total_revenue,sum(Profit_Margin) AS total_profit 
     from analysis group by  Cuisine_Type order by total_revenue desc""",
     
     "13.Peak hour demand analysis":
     """select Peak_Hour,count(Order_ID) as total_orders from analysis group by Peak_hour order by  total_orders desc""",
     
     "14.Payment mode preferences":
      """select Payment_Mode,count(Order_ID) as Total_Orders from analysis group by Payment_Mode order by Total_orders desc""",
     
     "15.Cancellation reason analysis":
     """select Cancellation_Reason,count(Order_ID) as cancelled_orders from  analysis where Order_Status = 'Cancelled'
      group by Cancellation_Reason order by cancelled_orders Desc"""
     
}

st.title("Online food delivery Analysis Dashboard")
 
task = st.selectbox("choose query number", list(queries.keys()))

if st.button("run query"):
    query=queries[task]
    df=pd.read_sql(query,engine)
    
    st.subheader(f"results for: {task}")
    st.dataframe(df, use_container_width = True)
    