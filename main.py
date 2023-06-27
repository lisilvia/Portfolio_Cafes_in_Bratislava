# from flask import Flask, render_template, redirect, url_for, flash
# from flask_bootstrap import Bootstrap
# from flask_ckeditor import CKEditor
# from datetime import date
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import relationship
# from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
# from forms import CreatePostForm
# from flask_gravatar import Gravatar

from flask import Flask, render_template, redirect, url_for, jsonify
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import os

#WTF_CSRF_SECRET_KEY=os.environ.get('CSRF_KEY')
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("CSRF_KEY")
csrf = CSRFProtect(app)
Bootstrap(app)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Create Table
with app.app_context():
    class Cafe(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(250), unique=True, nullable=False)
        map_url = db.Column(db.String(500), nullable=False)
        img_url = db.Column(db.String(500), nullable=False)
        location = db.Column(db.String(250), nullable=False)
        seats = db.Column(db.String(5), nullable=False)
        rating = db.Column(db.String(3), nullable=False)
        has_wifi = db.Column(db.String(3), nullable=False)
        has_sockets = db.Column(db.String(3), nullable=False)
        loud_music = db.Column(db.String(3), nullable=False)
        coffee_price = db.Column(db.String(250), nullable=True)
        comments = db.Column(db.String(1000), nullable=True)
    db.create_all()

class AddCafeForm(FlaskForm):
    name = StringField("Cafe Name", validators=[DataRequired()])
    map_url = StringField("Map URL", validators=[DataRequired(), URL()])
    img_url = StringField("Image URL", validators=[DataRequired(), URL()])
    location = StringField("Location", validators=[DataRequired()])
    has_sockets = SelectField("Has Sockets?", choices=['Yes', 'No'])
    rating = SelectField("Rating max.5", choices=['5/5', '4/5', '3/5','2/5', '1/5'], validators=[DataRequired()])
    has_wifi = SelectField("Has WiFi?", choices=['Yes', 'No'])
    loud_music = SelectField("Loud Music?", choices=['Yes', 'No'])
    seats = SelectField("Number of Seats", choices=['0-10', '11-20', '21-30','31-40', '41-50', '51-60', 'more'], validators=[DataRequired()])
    coffee_price = SelectField("Price for Cappuccino", choices=['0.50€ - 1.00€','1.10€ - 1.50€', '1.60€ - 2.00€', '2.10€ - 2.50€', '2.60€ - 3.00€', '3.10€ - 3.50€', '3.60€ - 4.00€'], validators=[DataRequired()])
    comments = StringField("Comments")
    submit = SubmitField("Add Cafe")

@app.route("/")
def home():
    all_cafes = Cafe.query.all()
    db.session.commit()
    return render_template("index.html", cafes=all_cafes)

#Create Record
@app.route("/add", methods=["GET","POST"])
def add_cafe():
    form = AddCafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
        name=form.name.data,
        map_url=form.map_url.data,
        img_url=form.img_url.data,
        location=form.location.data,
        has_sockets=form.has_sockets.data,
        rating=form.rating.data,
        has_wifi=form.has_wifi.data,
        loud_music=form.loud_music.data,
        seats=form.seats.data,
        coffee_price=form.coffee_price.data,
        comments=form.comments.data,
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_cafe.html", form=form)


#Delete Cafe
@app.route("/delete/<int:cafe_id>")
def delete_cafe(cafe_id):
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for("home"))

# #Edit Cafe
@app.route("/edit/<int:cafe_id>", methods=["GET","POST"])
def edit(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    edit_form = AddCafeForm(
        name=cafe.name,
        img_url=cafe.img_url,
        location=cafe.location,
        rating=cafe.rating,
        coffee_price=cafe.coffee_price,
    )

    if edit_form.validate_on_submit():
        cafe.name = edit_form.name.data
        cafe.img_url = edit_form.img_url.data
        cafe.location = edit_form.location.data
        cafe.rating = edit_form.rating.data
        cafe.coffee_price = edit_form.coffee_price.data
        db.session.commit()
        return redirect(url_for("home"))
        # return redirect(url_for("home"))
    return render_template("add_cafe.html", form=edit_form, is_edit=True)
    # return render_template("add_cafe.html", form=edit_form, is_edit=True)


if __name__ == '__main__':
    app.run(debug=True)
