import pandas as pd
import sqlite3


con = sqlite3.connect("db.sqlite3")
# con2 = sqlite3.connect("database.sqlite3")
df = pd.read_sql_query("SELECT * from ResponseTable", con)


def check_existence(input):
    if str(input) in df["text"].to_string(index=False):
        return True
    else:
        return False
