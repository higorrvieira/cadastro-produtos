from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          
        password="mYSqlserver!@#3", 
        database="produtos_db"
    )

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_connection()
    c = conn.cursor(dictionary=True)

    if request.method == "POST":
        nome = request.form["nome"]
        preco = request.form["preco"]
        quantidade = request.form["quantidade"]
        c.execute("INSERT INTO produtos (nome, preco, quantidade) VALUES (%s, %s, %s)",
                  (nome, preco, quantidade))
        conn.commit()

    c.execute("SELECT * FROM produtos")
    produtos = c.fetchall()
    conn.close()

    return render_template("index.html", produtos=produtos)

@app.route("/delete/<int:id>")
def delete(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM produtos WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
