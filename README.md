# Bootcamp Trainer Management — Assignment 2

A Django application for managing trainers and their teaching subjects, with a Tailwind CSS interface and a Django administration panel.

## Features

- View trainers in a paginated table with a total record count.
- Create trainers with form validation.
- Edit existing records.
- Search by surname.
- Confirm deletion before submitting a POST request.
- Display feedback messages and empty search results.
- Manage trainers through Django admin.

## Technology and compatibility

| Component | Requirement |
| --- | --- |
| Django | 5.2.x; install the version declared in `requirements.txt` |
| Python | 3.10–3.13; Python 3.14 requires Django 5.2.8 or later |
| SQLite | 3.31 or later; default database, normally included with Python |
| MySQL (optional) | 8.0.11 or later |
| MariaDB (optional) | 10.5 or later |
| Frontend | Tailwind CSS 4, Node.js and npm |

Use the latest patch release of your selected, maintained Python series. Database versions above are Django 5.2 compatibility minimums, not recommendations to install obsolete server releases. Choose a maintained server release for a new installation. Follow the project's package files for dependency versions rather than upgrading Django to a different major release automatically.

These instructions cover local development on Windows, Linux and macOS. They do not establish that every OS and dependency combination has been tested. The full dependency files and test results must be checked before claiming cross-platform verification.

References: [Django Python compatibility](https://docs.djangoproject.com/en/5.2/faq/install/#what-python-version-can-i-use-with-django), [Django database support](https://docs.djangoproject.com/en/5.2/ref/databases/).

## Project layout

| Path | Purpose |
| --- | --- |
| `bootcamp/manage.py` | Django management commands |
| `bootcamp/bootcamp/settings.py` | Application settings |
| `bootcamp/trainers/` | Models, forms, views, admin and tests |
| `bootcamp/templates/` | Shared layout, includes and trainer templates |
| `bootcamp/assets/css/app.css` | Tailwind source stylesheet |
| `bootcamp/static/css/main.css` | Compiled stylesheet |
| `bootcamp/staticfiles/` | Output of `collectstatic` |
| `bootcamp/db.sqlite3` | Local SQLite database |
| `.env.example` | Example environment settings |
| `package.json` | Frontend dependencies and CSS scripts |
| `rav.yaml` | Optional project command shortcuts |

Run the commands below from the repository root: the directory containing `requirements.txt` and `package.json`.

## 1. Create a virtual environment

Install Python, Node.js and npm first. Node.js is needed to build Tailwind CSS; XAMPP is not required for SQLite development.

### Windows — PowerShell

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
Copy-Item .env.example .env
```

If PowerShell blocks activation, use Command Prompt and run `env\Scripts\activate.bat`, or invoke `env\Scripts\python.exe` directly in place of `python`.

### Linux / macOS — bash or zsh

```bash
python3 -m venv env
source env/bin/activate
cp .env.example .env
```

On Debian/Ubuntu, if the `venv` module is missing, install the matching Python venv package using your system package manager before retrying.

Copy `.env.example` only when creating your local `.env`; do not overwrite an existing configuration accidentally.

## 2. Install dependencies and configure Django

With the virtual environment active:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
npm ci
```

`npm ci` uses the committed `package-lock.json`. If it reports a mismatch with `package.json`, resolve the dependency change intentionally rather than deleting the lock file blindly.

If `requirements.txt` includes `mysqlclient`, its native installation requirements still apply even when SQLite is selected. See the optional database section below. SQLite itself does not need `mysqlclient`.

Generate a secret key:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

Copy the generated value into `.env`:

```dotenv
DJANGO_SECRET_KEY=replace-with-the-generated-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

# Optional: ignored while SQLite is selected in settings.py.
MYSQL_DB_NAME=djbootcamp_trainers
MYSQL_DB_USER=bootcamp_user
MYSQL_DB_PASSWORD=replace-with-your-database-password
MYSQL_DB_HOST=127.0.0.1
MYSQL_DB_PORT=3306
```

Keep the real `.env` out of Git. The settings must load these values through the environment loader used by the project. `DEBUG=True` is for local development.

## 3. Initialize the default SQLite database

Keep this configuration active in `bootcamp/bootcamp/settings.py`:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

Run:

```bash
python bootcamp/manage.py check
python bootcamp/manage.py migrate
python bootcamp/manage.py createsuperuser
```

`migrate` applies the committed migrations and creates the database tables. Run `makemigrations` when you change models, not as a routine installation step.

## 4. Build CSS and start the application

```bash
npm run css:build
python bootcamp/manage.py runserver
```

- Application: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Administration: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

During development, use two terminals with the project as the working directory:

| Terminal | Command |
| --- | --- |
| CSS watcher | `npm run css:watch` |
| Django, with the virtual environment active | `python bootcamp/manage.py runserver` |

The CSS watcher stays running and rebuilds after source changes. Stop either process with `Ctrl+C`.

The beginning of `bootcamp/assets/css/app.css` should contain:

```css
@import "tailwindcss";
@source "../../templates";
```

The base template must load the compiled file with `{% static 'css/main.css' %}` after loading Django's `static` template tags.

## Collect static files

Configure these settings once:

```python
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
```

Build first, then collect:

```bash
npm run css:build
python bootcamp/manage.py collectstatic
```

Review the destination and confirm when prompted. This collects application and admin assets into `bootcamp/staticfiles/`. It does not compile Tailwind or configure production hosting. With the normal development configuration (`DEBUG=True`), `runserver` serves source static files without requiring collection after every edit.

Reference: [Django collectstatic](https://docs.djangoproject.com/en/5.2/ref/contrib/staticfiles/#collectstatic).

## Tests

The trainer test module is `bootcamp/trainers/tests.py`.

```bash
python bootcamp/manage.py test trainers --verbosity 2
```

The proposed initial tests cover listing, valid creation, rejecting an empty form, updating without duplication, GET deletion confirmation, and POST deletion. Ensure these tests are present in the repository; do not treat this list as evidence of a passing run.

Django uses a separate test database. Default SQLite testing uses an in-memory database. MySQL/MariaDB testing requires a database account with permission to create and remove the test database; ordinary privileges limited to the application database are not sufficient.

Reference: [Django testing](https://docs.djangoproject.com/en/5.2/topics/testing/overview/).

## Optional: MySQL / MariaDB

### XAMPP compatibility

The official XAMPP Windows 8.2.12 package includes MariaDB 10.4.32, which is incompatible with Django 5.2. The XAMPP version number refers to PHP, not the database server. Check the bundled database version for each OS rather than assuming that a recent download is compatible.

Check the server through phpMyAdmin's SQL tab or a database client:

```sql
SELECT VERSION();
```

Use SQLite or a compatible MySQL/MariaDB server if the result is below Django's minimum. Changing a port, running migrations, or installing a Python driver does not upgrade the database server. Do not disable Django's version check. Back up existing databases before replacing or upgrading a server; do not copy old database data directories into a new installation without following its supported upgrade procedure.

XAMPP is optional. Django can connect to a standalone local or remote database. Apache is not needed by `runserver`; it may be needed separately if you access phpMyAdmin through XAMPP.

Reference: [Official XAMPP downloads and bundled versions](https://www.apachefriends.org/download.html).

### Install the database driver

Django's MySQL backend can connect to both MySQL and MariaDB using `mysqlclient`.

Use the version declared by the project. If it is not declared, install a release compatible with your Python and Django versions:

```bash
python -m pip install mysqlclient
```

Native build prerequisites depend on the OS:

| OS | Installation notes |
| --- | --- |
| Windows | Prefer an available wheel matching Python and architecture. Building from source requires the supported MariaDB Connector/C and appropriate Visual Studio build tools. |
| Debian / Ubuntu | Common prerequisites: `python3-dev default-libmysqlclient-dev build-essential pkg-config`. Match Python headers to the interpreter in use. |
| macOS | The mysqlclient documentation describes Homebrew `mysql-client` and `pkg-config`, with `PKG_CONFIG_PATH` configured for the installed client library. |

Consult the [mysqlclient installation guide](https://github.com/PyMySQL/mysqlclient#install) for exact commands for your environment. Installing client libraries does not itself provide a running database server.

### Create the database and application user

Connect to the intended server as a database administrator. For a local development connection, use a new application account and replace the example password:

```sql
CREATE DATABASE djbootcamp_trainers CHARACTER SET utf8mb4;
CREATE USER 'bootcamp_user'@'localhost'
    IDENTIFIED BY 'replace-with-a-unique-password';
GRANT ALL PRIVILEGES ON djbootcamp_trainers.*
    TO 'bootcamp_user'@'localhost';
```

If the database or account already exists, inspect it instead of rerunning creation commands or resetting its password blindly. Remote connections need an account host appropriate to the actual client; the example is for local use.

### Select MySQL in settings.py

Fill in the `MYSQL_DB_*` values in your local `.env`. Use the real server port: `3307` is valid only if a server has been configured to listen there.

Comment out the SQLite `DATABASES` block and uncomment the existing MySQL block. Keep exactly one active assignment. The existing block assumes the project's `config()` environment loader is already imported and configured:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": config("MYSQL_DB_NAME"),
        "USER": config("MYSQL_DB_USER"),
        "PASSWORD": config("MYSQL_DB_PASSWORD"),
        "HOST": config("MYSQL_DB_HOST", default="127.0.0.1"),
        "PORT": config("MYSQL_DB_PORT", default="3306", cast=int),
        "OPTIONS": {
            "charset": "utf8mb4",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

Then initialize this database:

```bash
python bootcamp/manage.py migrate
python bootcamp/manage.py createsuperuser
python bootcamp/manage.py runserver
```

Switching the connection does not transfer SQLite records or users. Data transfer is a separate operation. Keep existing migration files when changing database backends.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| `MariaDB 10.5 or later is required` | The connected server is too old for Django 5.2. |
| Connection refused / error 10061 | Start the database server and verify host and listening port. |
| `Access denied ... using password: NO` | The connection supplied no password. Check the loaded settings and the account's actual requirements. |
| `Unknown database` | Create the named database on the intended server before migrations. |
| Missing layout or CSS | Check the Tailwind source path, run `npm run css:build`, and reload without cache. |
| Static file not found | Run `python bootcamp/manage.py findstatic css/main.css --verbosity 2`. The output file is `main.css`, not `app.css`. |
| `IndentationError` in admin.py | Use four spaces consistently inside the class; save before checking again. |
| `config` is undefined | Check settings imports and the project's actual environment-loader dependency; `python-dotenv` and `python-decouple` have different APIs. |

## Repository hygiene

Keep environment files, virtual environments, local databases and generated collections out of commits. Preserve `.env.example`, migration source files and dependency lock files.

Suggested root `.gitignore` entries:

```gitignore
.env
env/
venv/
node_modules/
__pycache__/
*.py[cod]
/bootcamp/db.sqlite3
/bootcamp/db.sqlite3-*
/bootcamp/staticfiles/
```

Ignore rules do not untrack files that were already committed. Review staged changes before pushing, especially credentials and database files.

## Scope

This README describes local development. Public deployment additionally requires production settings, suitable application/static-file serving, and a review of access control for the custom trainer views. Django admin authentication does not automatically protect custom pages.
