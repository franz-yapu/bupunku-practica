from flask import Flask

from .errors import registrar_errores
from .extensions import db, migrate


def create_app( config_class="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.json.ensure_ascii = False

    db.init_app(app)
    migrate.init_app(app, db)

 

    from . import models
    from .routes.autores import bp as autores_bp
    from .routes.libros import bp as libros_bp
    from .routes.prestamos import bp as prestamos_bp
    from .routes.socios import bp as socios_bp
    app.register_blueprint(autores_bp)
    app.register_blueprint(libros_bp)
    app.register_blueprint(prestamos_bp)
    app.register_blueprint(socios_bp)

    from .autor import Autor
    from .libro import Libro
    from .prestamo import Prestamo
    from .socio import Socio   
    
    registrar_errores(app)

    return app