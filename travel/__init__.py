from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from .forms import LoginForm, RegisterForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    #we use this utility module to display forms quickly
    Bootstrap5(app)

    #A secret key for the session object
    app.secret_key = 'somerandomvalue'
    # Configure and initialize the database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel.db'
    db.init_app(app)
    
    
        #initialise the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    
    #create a user loader function takes userid and returns User
    from .models import User  # importing here to avoid circular references
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    #add Blueprints
    from . import views
    app.register_blueprint(views.mainbp)
    from . import destinations
    app.register_blueprint(destinations.destbp)
    from . import auth
    app.register_blueprint(auth.authbp)
    
    @app.errorhandler(404)
    
    def not_found(e):
        return render_template('404.html', error=e)

    return app