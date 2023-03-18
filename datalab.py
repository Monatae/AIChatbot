import pandas as pd
import sqlite3
 
 
 
con = sqlite3.connect("db.sqlite3")
df = pd.read_sql_query("SELECT * from StatementTable", con)

print(df['text'])