from flask import Flask, render_template, flash, redirect, url_for, session, request
from models.forms import RegistryForm, SearchForm

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Config MariaDB Server Connection

db_type = "mysql+pymysql"  # Type of database (MySQL, Postgre, etc...)
db_user = "root"  # database user
db_passwd = "root"  # user's passwd
db_name = "cimd"  # name of the db
db_server = "localhost"  # server name / ip location
app.config['SQLALCHEMY_DATABASE_URI'] = db_type + '://' + db_user + ':' + db_passwd + '@' + db_server + '/' + db_name

# init MariaDB server
db = SQLAlchemy(app)


class Registry(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(15))
    street = db.Column(db.String(100))
    city = db.Column(db.String(100))
    postal_code = db.Column(db.SmallInteger)
    country = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    web_page = db.Column(db.String(100))

    def __repr__(self):
        return '<Registry %r>' % self.id


# Index
@app.route('/')
def index():
    return render_template('home.html')


# Dashboard
@app.route('/dashboard')
def dashboard():
    # Get registries
    registries = Registry.query.all()

    if len(registries) > 0:
        return render_template('dashboard.html', registries=registries)
    else:
        msg = 'No Registry Found'
        return render_template('dashboard.html', msg=msg)


# Add Registry
@app.route('/add_registry', methods=['GET', 'POST'])
def add_article():
    form = RegistryForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        last_name = form.last_name.data
        phone = form.phone.data
        street = form.route.data
        city = form.locality.data
        postal_code = form.postal_code.data
        country = form.country.data
        email = form.email.data
        web_page = form.web_page.data

        # Execute
        new_registry = Registry(name=name,
                                last_name=last_name,
                                phone=phone,
                                street=street,
                                city=city,
                                postal_code=postal_code,
                                country=country,
                                email=email,
                                web_page=web_page)
        db.session.add(new_registry)

        # Commit to DB
        db.session.commit()

        flash('Registry Created', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_registry.html', form=form)


# Edit Registry
@app.route('/edit_registry/<string:_id>', methods=['GET', 'POST'])
def edit_registry(_id):
    # Get registry by id
    _registry = db.session.query(Registry).filter_by(id=_id).first()

    # Get form
    form = RegistryForm(request.form)

    # Populate registry form fields
    form.name.data = _registry.name
    form.last_name.data = _registry.last_name
    form.phone.data = _registry.phone
    form.route.data = _registry.street
    form.locality.data = _registry.city
    form.postal_code.data = _registry.postal_code
    form.country.data = _registry.country
    form.email.data = _registry.email
    form.web_page.data = _registry.web_page

    if request.method == 'POST' and form.validate():
        name = request.form['name']
        last_name = request.form['last_name']
        phone = request.form['phone']
        street = request.form['route']
        city = request.form['locality']
        postal_code = request.form['postal_code']
        country = request.form['country']
        email = request.form['email']
        web_page = request.form['web_page']

        # Create Cursor
        app.logger.info(_id)

        # Execute
        update = db.session.query(Registry).filter_by(id=_id).update({"name": name,
                                                                      "last_name": last_name,
                                                                      "phone": phone,
                                                                      "street": street,
                                                                      "city": city,
                                                                      "postal_code": postal_code,
                                                                      "country": country,
                                                                      "email": email,
                                                                      "web_page": web_page})

        # Commit to DB
        db.session.commit()

        flash('Registry Updated', 'success')

        return redirect(url_for('dashboard'))

    return render_template('edit_registry.html', form=form)


# Delete Registry
@app.route('/delete_registry/<string:id>', methods=['POST'])
def delete_registry(id):
    # Get registry
    _registry = Registry.query.filter(Registry.id == id).first()

    # Execute
    db.session.delete(_registry)

    # Commit to DB
    db.session.commit()

    flash('Registry Deleted', 'success')

    return redirect(url_for('dashboard'))


# Search Registry
@app.route('/search_registry', methods=['POST'])
def search_registry():
    form = SearchForm(request.form)

    search_text = ''
    search_field = ''
    _registries = []

    if request.method == 'POST' and form.validate():
        search_text = form.search_text.data
        search_field = form.search_field.data

        rd_name = False
        rd_email = False
        rd_postal_code = False
        rd_city = False
        rd_country = False

        if search_field == 'name':
            rd_name = True
        elif search_field == 'email':
            rd_email = True
        elif search_field == 'postal_code':
            rd_postal_code = True
        elif search_field == 'city':
            rd_city = True
        elif search_field == 'country':
            rd_country = True

        # Get registry
        _registries = Registry.query.filter(Registry.name.like("%" + search_text * rd_name + "%")) \
                                    .filter(Registry.email.like("%" + search_text * rd_email + "%")) \
                                    .filter(Registry.postal_code.like("%" + search_text * rd_postal_code + "%")) \
                                    .filter(Registry.city.like("%" + search_text * rd_city + "%")) \
                                    .filter(Registry.country.like("%" + search_text * rd_country + "%")).all()

        # Commit to DB
        db.session.commit()

    if len(_registries) > 0:
        msg = str(len(_registries)) + ' registries found for \'' + search_text + '\', in field \'' + search_field.capitalize() + '\''
        return render_template('search_registry.html', registries=_registries, msg=msg)
    else:
        error = 'No registry found for \'' + search_text + '\', in field \'' + search_field.capitalize() + '\''
        return render_template('search_registry.html', error=error)


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
