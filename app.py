from flask import Flask, url_for, render_template, redirect, flash, jsonify
from models import db, connect_db, Pet
from forms import AddPetForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "1235"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    connect_db(app)
    db.create_all()


@app.route('/')
def list_pets():
    pets = Pet.query.all()
    return render_template("pet_list.html", pets=pets)


@app.route("/add", methods=["GET", "POST"])
def add_pet():
    form = AddPetForm()
    print(form)
    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        url = form.url.data
        age = form.age.data
        notes = form.notes.data

        pet = Pet(name=name, species=species, url=url, age=age, notes=notes)
        db.session.add(pet)
        db.session.commit()
        flash(f"{pet.name} added.")
        return redirect(url_for('list_pets'))
    else:
        return render_template("pet_add_form.html", form=form)

# @app.route("/<int:pet_id>", methods=["GET", "POST"])
# def edit_pet(pet_id):
#
#
# @app.route("/api/pets/<int:pet_id>", methods=['GET'])
# def api_get_pet(pet_id):
#     return render_template("base.html")
#

