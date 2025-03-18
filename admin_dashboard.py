from flask import Flask, render_template, request, redirect
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

def get_filter_logs():
    conn = sqlite3.connect("filtering.db")
    df = pd.read_sql_query("SELECT action, COUNT(*) as count FROM logs GROUP BY action", conn)
    conn.close()
    return df

@app.route("/")
def index():
    df = get_filter_logs()
    
    # Generate a bar chart
    plt.figure(figsize=(6, 4))
    plt.bar(df["action"], df["count"], color=["red", "blue"])
    plt.xlabel("Filtering Action")
    plt.ylabel("Count")
    plt.title("Filtering Actions Frequency")
    plt.savefig("static/filter_chart.png")  # Save the graph
    plt.close()

    return render_template("dashboard.html", img_url="/static/filter_chart.png", profiles=get_profiles())

def get_profiles():
    conn = sqlite3.connect("filtering.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profiles")
    profiles = cursor.fetchall()
    conn.close()
    return profiles

@app.route("/add_profile", methods=["POST"])
def add_profile():
    name = request.form["name"]
    conn = sqlite3.connect("filtering.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO profiles (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete_profile/<int:id>")
def delete_profile(id):
    conn = sqlite3.connect("filtering.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM profiles WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)