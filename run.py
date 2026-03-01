from app import create_app
from app.extensions import db, migrate

app = create_app()

if __name__ == '__main__':
    db.init_app(app)
    migrate.init_app(app, db)
    app.run(debug=True)