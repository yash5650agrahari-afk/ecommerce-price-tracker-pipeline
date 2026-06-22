import pandas as pd 
import pymysql


connection = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "Yash@7529",
    db = "Ecommerce"

)

# Old line: Query = "select order_date,sum(total_amount) Sales from orders group by Order_Date"
# Change it to this:
Query = "select Order_Date, sum(Total_Amount) as Sales from Orders group by Order_Date"

df = pd.read_sql(Query,connection)
print(df)

df.to_excel("Sales.xlsx",index=False)
print("Report Created!....")
