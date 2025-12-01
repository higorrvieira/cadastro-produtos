from flask import Flask, render_template, request, redirect, url_for, Response
import mysql.connector
import csv

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

    # CADASTRO / EDIÇÃO
    if request.method == "POST":
        produto_id = request.form.get("id")
        nome = request.form["nome"]
        preco = float(request.form["preco"])
        quantidade = int(request.form["quantidade"])

        if produto_id:
            c.execute("""
                UPDATE produtos SET nome=%s, preco=%s, quantidade=%s WHERE id=%s
            """, (nome, preco, quantidade, produto_id))
        else:
            c.execute("""
                INSERT INTO produtos (nome, preco, quantidade) VALUES (%s, %s, %s)
            """, (nome, preco, quantidade))
        conn.commit()

    # EDIÇÃO EXISTENTE
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

# NOVA ROTA: Exportar CSV
@app.route("/export")
def export_csv():
    conn = get_connection()
    c = conn.cursor(dictionary=True)
    c.execute("SELECT * FROM produtos")
    produtos = c.fetchall()
    conn.close()

    def generate():
        output = csv.writer()
        output.writerow(['ID','Nome','Preço','Quantidade'])
        for p in produtos:
            output.writerow([p['id'], p['nome'], p['preco'], p['quantidade']])
        return output

    def generate_stream():
        yield "ID,Nome,Preço,Quantidade\n"
        for p in produtos:
            yield f"{p['id']},{p['nome']},{p['preco']},{p['quantidade']}\n"

    return Response(generate_stream(), mimetype="text/csv",
                    headers={"Content-Disposition":"attachment;filename=produtos.csv"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
