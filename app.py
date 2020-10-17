from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pets'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)


@app.route('/')
def main_route():
    """Show pets, name, photo, display "Available" in bold if the pet is available."""

    pets = Pet.query.all()
    #[pet1, pet2, pet3]
    return render_template("index.html", pets=pets)


@app.route('/add', methods=["GET", "POST"])
def add_pet_form():
    """ Add pet form; handle adding pets """

    form = AddPetForm()
  
    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        available = form.available.data

        new_pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes, available=available)
        db.session.add(new_pet)
        db.session.commit()

        flash(f"Added {name}, species: {species}, age: {age}, notes: {notes}, photo_url={photo_url}, available={available}")
        
        return redirect("/add")

    else:
        return render_template(
            "pet_add_form.html", form=form)


@app.route('/<int:pet_id>', methods=['GET', 'POST'])
def show_pet(pet_id):
    """ Edit pet form; handle editing pets """
    
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        notes = form.notes.data
        photo_url = form.photo_url.data
        available = form.available.data

        pet.notes = notes
        pet.photo_url = photo_url
        pet.available = available

        db.session.commit()
        flash(f"notes: {notes}, photo_url={photo_url}, available={pet.available}")
       
        return redirect(f'/{pet_id}')

    p = dict(name=pet.name, species=pet.species, photo_url=pet.photo_url, age=pet.age, notes=pet.notes, available=pet.available)


    return render_template('pet_edit_form.html', pet=p, form=form)
