from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("produtos.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            quantidade INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect("produtos.db")
    c = conn.cursor()

    if request.method == "POST":
        nome = request.form.get("nome")
        preco = request.form.get("preco")
        quantidade = request.form.get("quantidade")
        c.execute("INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)",
                  (nome, preco, quantidade))
        conn.commit()
        return redirect("/")

    c.execute("SELECT * FROM produtos")
    produtos = c.fetchall()
    conn.close()

    return render_template("index.html", produtos=produtos)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
