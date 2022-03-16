from flask import Flask

def create_app():
    app = Flask('app')
    app.debug = True

    # Define route with Blueprint
    from .views import views
    app.register_blueprint(views, url_prefix='/')
    print('web', app.config)
    
    return app



