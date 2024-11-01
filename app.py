import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# Define o diretório do projeto e o arquivo do banco de dados
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "cake_database.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Desabilita notificações de modificação

db = SQLAlchemy(app)

class Cake(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flavor = db.Column(db.String(80), unique=True, nullable=False)
    size = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return "<Cake: {}>".format(self.flavor)

@app.route('/', methods=["GET", "POST"])
def home():
    cakes = Cake.query.all()  # Obtém todos os bolos de pote
    if request.method == "POST":
        try:
            flavor = request.form.get("flavor")
            size = request.form.get("size")
            price = request.form.get("price")
            rating = request.form.get("rating")

            # Cria um novo bolo de pote
            cake = Cake(flavor=flavor, size=size, price=float(price), rating=float(rating) if rating else None)
            db.session.add(cake)
            db.session.commit()
        except Exception as e:
            print("Failed to add cake")
            print(e)
    return render_template("index.html", cakes=cakes)

@app.route("/update", methods=["POST"])
def update():
    try:
        old_flavor = request.form.get("old_flavor")
        cake = Cake.query.filter_by(flavor=old_flavor).first()
        if cake:
            # Atualiza as informações do bolo
            cake.flavor = request.form.get("new_flavor")
            cake.size = request.form.get("new_size")
            cake.price = float(request.form.get("new_price")) if request.form.get("new_price") else cake.price
            cake.rating = float(request.form.get("new_rating")) if request.form.get("new_rating") else cake.rating
            db.session.commit()
    except Exception as e:
        print("Couldn't update cake details")
        print(e)
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    flavor = request.form.get("flavor")
    cake = Cake.query.filter_by(flavor=flavor).first()
    if cake:
        # Deleta o bolo
        db.session.delete(cake)
        db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados
    app.run(host='0.0.0.0', debug=True)
