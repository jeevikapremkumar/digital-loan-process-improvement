"""Load the CSV into SQLite, run every named query in sql/analysis_queries.sql, save results."""
import re, sqlite3, pandas as pd
df = pd.read_csv("../data/loan_applications.csv")
con = sqlite3.connect(":memory:")
df.to_sql("loan_applications", con, index=False)
sql = open("../sql/analysis_queries.sql").read()
blocks = re.split(r"-- name: (\w+)\n", sql)[1:]
for name, body in zip(blocks[::2], blocks[1::2]):
    res = pd.read_sql_query(body.strip().rstrip(";"), con)
    res.to_csv(f"../outputs/{name}.csv", index=False)
    print(f"\n== {name} ==\n{res.to_string(index=False)}")
