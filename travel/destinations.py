from flask import Blueprint, render_template, request, redirect, url_for
from .models import Destination, Comment
from .forms import DestinationForm
from .forms import CommentForm
from flask_sqlalchemy import SQLAlchemy
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user 

#Use of blue print to group routes, 
# name - first argument is the blue print name 
# import name - second argument - helps identify the root url for it 
destbp = Blueprint('destination', __name__, url_prefix = '/destinations')

@destbp.route('/<id>')
def show(id):
    destination = db.session.scalar(db.select(Destination).where(Destination.id == id))
    #destination = get_destination()
    # create a comment form
    cForm = CommentForm()
    return render_template('destinations/show.html', destination = destination, form = cForm)

# @destbp.route('/create', methods = ['GET', 'POST'])
# def create():
#   print('Method type: ', request.method)
#   form = DestinationForm()
#   if form.validate_on_submit():
#     print('Successfully created new travel destination')
#     return redirect(url_for('destination.create'))
#   return render_template('destinations/create.html', form=form)


@destbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = DestinationForm()
  if form.validate_on_submit():
    #call the function that checks and returns image
    db_file_path = check_upload_file(form)
    destination = Destination(name=form.name.data,description=form.description.data, 
    image = db_file_path,currency=form.currency.data)
    # add the object to the db session
    db.session.add(destination)
    # commit to the database
    db.session.commit()
    print('Successfully created new travel destination', 'success')
    #Always end with redirect when form is valid
    return redirect(url_for('destination.create'))
  return render_template('destinations/create.html', form=form)
def check_upload_file(form):
  #get file data from form  
  fp = form.image.data
  filename = fp.filename
  #get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  #upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH,'static/image',secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/image/' + secure_filename(filename)
  #save the file and return the db upload path  
  fp.save(upload_path)
  return db_upload_path

# @destbp.route('/create', methods=['GET', 'POST'])
# def create():
#   print('Method type: ', request.method)
#   form = DestinationForm()
#   if form.validate_on_submit():
#     destination = Destination(name=form.name.data,
#     description=form.description.data,
#     image=form.image.data,
#     currency=form.currency.data)
#     # add the object to the db session
#     db.session.add(destination)         #may want to commit multiple 
#     # commit to the database
#     db.session.commit()
#     print('Successfully created new travel destination', 'success')
#     #Always end with redirect when form is valid
#     return redirect(url_for('destination.create'))
#   return render_template('destinations/create.html', form=form)

@destbp.route('/<id>/comment', methods=['GET', 'POST']) 
@login_required 
def comment(id):  
    form = CommentForm()  
    #get the destination object associated to the page and the comment
    destination = db.session.scalar(db.select(Destination).where(Destination.id==id))
    if form.validate_on_submit():  
      # read the comment from the form, associate the Comment's destination field
      # with the destination object from the above DB query
      comment = Comment(text=form.text.data, destination=destination, user=current_user) 
      #here the back-referencing works - comment.destination is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 
      #flashing a message which needs to be handled by the html
      #flash('Your comment has been added', 'success')  
      print('Your comment has been added', 'success') 
    # using redirect sends a GET request to destination.show
    return redirect(url_for('destination.show', id=id))
  
# @destbp.route('/<id>/comment', methods = ['GET', 'POST'])
# def comment(id):
#   form = CommentForm()
#   if form.validate_on_submit():
#     print('The Following has been posted: {form.text.data}')
#     # why do i get The Following has been posted: {form.text.data} instead of the actual text?
#     return redirect(url_for('destination.show', id=id)) #id=1
































# def get_destination():
#   # creating the description of Brazil
#   b_desc = """Brazil is considered an advanced emerging economy.
#    It has the ninth largest GDP in the world by nominal, and eight by PPP measures. 
#    It is one of the world\'s major breadbaskets, being the largest producer of coffee for the last 150 years."""
#    # an image location
#   image_loc = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQFyC8pBJI2AAHLpAVih41_yWx2xxLleTtdshAdk1HOZQd9ZM8-Ag'
#   destination = Destination('Brazil', b_desc,image_loc, 'R$10')
#   # a comment
#   comment = Comment("Sam", "Visited during the olympics, was great", '2023-08-12 11:00:00')
#   destination.set_comments(comment)
#   comment = Comment("Bill", "free food!", '2023-08-12 11:00:00')
#   destination.set_comments(comment)
#   comment = Comment("Sally", "free face masks!", '2023-08-12 11:00:00')
#   destination.set_comments(comment)
#   return destination