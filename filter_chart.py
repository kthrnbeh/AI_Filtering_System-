import matplotlib.pyplot as plt
import sqlite3
import pandas as pd

def generate_chart():
    conn = sqlite3.connect("filtering.db")
    df = pd.read_sql_query("SELECT action, COUNT(*) as count FROM logs GROUP BY action", conn)
    conn.close()
    
    plt.figure(figsize=(6, 4))
    plt.bar(df["action"], df["count"], color=["red", "blue"])
    plt.xlabel("Filtering Action")
    plt.ylabel("Count")
    plt.title("Filtering Actions Frequency")
    plt.savefig("static/filter_chart.png")  # Save chart to static folder
    plt.close()

if __name__ == "__main__":
    generate_chart()
    print("Filtering chart generated successfully!")