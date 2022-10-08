from flask import render_template,redirect,request,session
from flask_app import app
from flask_app.models.user import User
from flask import flash
from flask_app.models.park import Park



@app.route("/dashboard")
def user_dashboard():
    user_data={
        'id':session['user_id']
    }
    user=User.get_user_by_id(user_data)
    parks=Park.get_all()
    return render_template("dashboard.html", user=user,parks=parks)

@app.route("/parks/new")
def new_park_form():
    user_data={
        'id': session['user_id']
    }
    user= User.get_user_by_id(user_data)
    return render_template("create_parks.html",user=user)
    
@app.route("/parks/create",methods=['POST'])
def create_park():
    if not Park.validate_create(request.form):
        return redirect("/parks/new")
    Park.create(request.form)
    return redirect("/dashboard")

@app.route("/show/<int:id>")
def show_park(id):
    user_data={
        'id': session['user_id']
    }
    user = User.get_user_by_id(user_data)
    park_data={
        "id":id

    }
    park= Park.get_one(park_data)
    return render_template('show_park.html',park=park, user=user )

@app.route("/edit/<int:id>")
def show_edit_form(id):
    user_data ={
        'id': session['user_id']
    }
    user = User.get_user_by_id(user_data)
    park_data ={
        'id':id
    }
    park = Park.get_one(park_data)
    return render_template("edit_park.html",user=user,park=park)

@app.route("/parks/<int:id>/update", methods=['POST'])
def update_park(id):
    Park.update(request.form)
    return redirect('/dashboard')

@app.route("/parks/<int:id>/delete", methods = ['POST'])
def delete(id):
    park_data = {
        'id': id
    }
    park = Park.get_one(park_data)
    if (park.user_id!=session['user_id']):
        flash(f"unauthorized access to edit park with id {id}")
        return redirect("/dashboard")
    Park.delete(request.form)
    return redirect("/dashboard")

@app.route('/parks/<int:id>/favorite', methods=['POST'])
def favorite_park(id):
    Park.favorite(request.form)
    return redirect("/dashboard")

@app.route('/parks/<int:id>/unfavorite', methods=['POST'])
def unfavorit_park(id):
    Park.unfavorite(request.form)
    return redirect("/dashboard")
