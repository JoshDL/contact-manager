# FlaskApp

This application is built on the Python Flask framework. The objective of the challenge was to develop a simple contact manager. It has a graphical interface with the functionality required. Please, continue to the dashboard and proceed evaluating the web app.  

The functionality of this Flask app is:

- The information of a contact will be; name, surname, telephone, address (street, town, zip code and country), email address and web page.  
- Contact data must be stored in a SQL database (client / server, sqlite not. So a MariaDB was chosen).
- Query interface with the ability to filter by name, email address, zip code, town and country.
- Record / Edit interface.
- [Google Places API](https://developers.google.com/places/?hl=es-419) was used to fill in the address information.

## Requirements

To use this template, you need:

- [Python 3.5](https://python.org)
- [Pip Package Manager](https://pypi.python.org/pypi)
- [Requirements](requirements.txt)

### Running the app

```bash
python app.py
```

### DDL

The table designed for this app was created using the following MySQL code:

```mysql
CREATE TABLE IF NOT EXISTS registry (
    id INT(5) NOT NULL AUTO_INCREMENT,
    name VARCHAR(80) NOT NULL,
    last_name VARCHAR(80) NOT NULL,
    phone VARCHAR(15) DEFAULT NULL,
    street VARCHAR(100) DEFAULT NULL,
    city VARCHAR(100) DEFAULT NULL,
    postal_code VARCHAR(12) DEFAULT NULL,
    country VARCHAR(100) DEFAULT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    web_page VARCHAR(100) DEFAULT NULL,
    PRIMARY KEY(id)
    );
```
