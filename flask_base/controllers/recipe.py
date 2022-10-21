from email import message
import os

from flask import redirect, render_template, request, flash, session, send_from_directory, url_for
from flask_base import app
from datetime import datetime
from flask_base.models.recipes import Recipe
from flask_base.models.images import Image
from flask_base.models.usuario import Usuario
from werkzeug.utils import secure_filename

from flask_base.utils.utils import enviar_email
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/recipes')
def recipes():
    if 'usuario_id' not in session:
        return redirect('/login')
    return render_template('recipes/recipe.html', all_recipes = Recipe.get_all_width_user())

@app.route('/recipes/new')
def new_recipe():
    if 'usuario_id' not in session:
        return redirect('/login')
    return render_template('recipes/createRecipe.html')

@app.route('/uploads/<name>')
def download_file(name):
    print("QUIERO VER IMAGE---->", name)
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/process_recipe', methods=['GET','POST'])
def process_recipe():
    if request.method == 'POST':
        print(request.form)
        if not Recipe.validar(request.form):
            return redirect('/recipes/new')
        print('in post of file')
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename =f"{int(datetime.utcnow().timestamp())}{secure_filename(file.filename)}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


    new_recipe={
        'name':request.form['name'],
        'description':request.form['description'],
        'instructions':request.form['instructions'],
        'date_made':request.form['date_made'],
        'under_30':request.form['under_30'],
        'usuario_id':session['usuario_id']
    }
    recipe=Recipe.save(new_recipe)
    
    new_image={
        'name': filename,
        'recipe_id':recipe,
    }
    print("VER IMAGE--->", new_image)
    image = Image.save(new_image)
    if recipe == False:
        flash('algo errado paso con la creacion de la receta', 'error')
        return redirect ('/recipes/new')
    flash('Exito al crear la nueva receta', 'success')
    return redirect('/recipes')

@app.route('/recipes/<id>')
def recipe_details(id):
    if 'usuario_id' not in session:
        return redirect('/login')
    recipe = Recipe.view_by_id(id)
    recipe.date_made = recipe.date_made.strftime('%Y-%m-%d')
    return render_template('recipes/detailRecipe.html', recipe = recipe)

@app.route('/recipes/delete/<id>', methods=['GET'])
def recipes_delete_process(id):
    if 'usuario_id' not in session:
        return redirect('/login')
    recipe=Recipe.view_by_id(id)
    if session['usuario_id'] == recipe.usuario_id:
        print("QUIERO VER RECIPE",recipe)
        Recipe.delete(id)
        carpeta=os.path.dirname(__file__)
        if os.path.exists(f"{carpeta}/../static/uploads/{recipe.image}"):
            os.remove(f"{carpeta}/../static/uploads/{recipe.image}")
        else:
            print("no existe imagen")
        print(f"{carpeta}/../static/uploads/{recipe.image}")
        flash(f"exito al eliminar la receta","success")
        return redirect('/recipes')
    return redirect('/recipes')

@app.route("/send_msg/<id>", methods=['POST'])
def send_msg(id):
    recipe=Recipe.view_by_id(id)
    usuario= Usuario.get_by_id(recipe.usuario_id)
    print(request.form['msg'])
    print(usuario.email)
    enviar_email(request.form['msg'], usuario.email)
    flash(f"Mensaje enviado correctamente", "success")
    return redirect(f'/recipes/{id}')

@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if 'usuario_id' not in session:
        return redirect('/login')
    recipe=Recipe.get_by_id_user(id)[0]
    if session['usuario_id'] == recipe.usuario_id:
        recipe.date_made = recipe.date_made.strftime("%Y-%m-%d")
        return render_template('recipes/editRecipe.html',recipe=recipe)
    return redirect(f'/recipes/{id}')

@app.route('/process/edit/recipes/<int:id>', methods=['POST'])
def process_edit_recipe(id):
    print(request.form)
    if not Recipe.validar(request.form):
        return redirect('/recipes/new')
    
    upgrade_recipe= {
        'id':id,
        'name':request.form['name'],
        'description':request.form['description'],
        'instructions':request.form['instructions'],
        'date_made':request.form['date_made'],
        'under_30':request.form['under_30'],
    }
    upgrade = Recipe.update(upgrade_recipe)
    print("QUIERO VER ACTUALIZAR--->",upgrade)
    return redirect('/recipes')