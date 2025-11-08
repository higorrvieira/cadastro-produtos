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
        produto_id = request.form.get("id")
        nome = request.form["nome"]
        preco = request.form["preco"]
        quantidade = request.form["quantidade"]

        if produto_id: 
            c.execute("""
                UPDATE produtos SET nome=%s, preco=%s, quantidade=%s WHERE id=%s
            """, (nome, preco, quantidade, produto_id))
        else: 
            c.execute("""
                INSERT INTO produtos (nome, preco, quantidade) VALUES (%s, %s, %s)
            """, (nome, preco, quantidade))
        conn.commit()

    edit_id = request.args.get("edit_id")
    produto_edit = None
    if edit_id:
        c.execute("SELECT * FROM produtos WHERE id = %s", (edit_id,))
        produto_edit = c.fetchone()

    c.execute("SELECT * FROM produtos")
    produtos = c.fetchall()

    conn.close()
    return render_template("index.html", produtos=produtos, produto_edit=produto_edit)

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
