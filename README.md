# Pos Inventory

The POS Inventory Management System is a user-friendly web application designed to streamline the management of inventory for Point of Sale (POS) businesses. This system allows businesses to efficiently track their products, update stock levels, manage suppliers, and generate reports to make informed decisions.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Features
- **Product Management:** Add, edit, and delete products from the inventory. Each product includes details such as name, description, price, and quantity.

- **Stock Updates:** Keep track of product stock levels in real-time. Receive alerts when products are running low to ensure you never run out of popular items.

- **Supplier Information:** Maintain a list of suppliers with contact details. Link products to their respective suppliers for easy reordering.

- **Sales Tracking:** Record sales transactions and automatically deduct sold quantities from the inventory. Monitor sales history for each product.

- **User Authentication:** Secure user accounts with authentication to manage access control. Different user roles (admin, staff) have varying levels of system access.

- **Reports Generation:** Generate comprehensive reports to gain insights into inventory levels, sales trends, and supplier performance. Export reports in various formats for further analysis.

## Prerequisites

Before you begin, ensure you have the following:

- PostgreSQL: [Download PostgreSQL](https://www.postgresql.org/download/)

## Installation Steps

1. Install PostgreSQL:

   Follow the installation instructions provided on the PostgreSQL download page based on your operating system.

2. Create a Database:

   Open a terminal or command prompt and log in to PostgreSQL:

   ```bash
      psql -U postgres
   ```
3. Create a new database for the POS

    create a database 
    ```bash
       CREATE DATABASE pos_inventory_db;
    ```
    Exit the PostgreSQL console:
    ```bash
       \q
    ```
    Export your host, port, database name, database user and password
## Installation
1. Clone the repository:
```bash
   git clone https://github.com/iakev/pos_inventory.git
```
2. Navigate to the Requirements Directory, 
```bash
   cd pos_inventory/requirements
```
3. Create a Virtual Environment
```bash
    python -m venv venv
```
4. Activate the Virtual Environment:
- On windows:
```bash
    venv\Scripts\activate
```
- On MacOs and Linux
```bash
   source venv/bin/activate
```
5. Install Requirements:
```bash
   pip install -r requirements/local.txt
```
License: MIT

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy pos_inventory

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

### Celery

This app comes with Celery.

To run a celery worker:

```bash
cd pos_inventory
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the same folder with _manage.py_, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process:

```bash
cd pos_inventory
celery -A config.celery_app beat
```

or you can embed the beat service inside a worker with the `-B` option (not recommended for production use):

```bash
cd pos_inventory
celery -A config.celery_app worker -B -l info
```

### Sentry

Sentry is an error logging aggregator service. You can sign up for a free account at <https://sentry.io/signup/?code=cookiecutter> or download and host it yourself.
The system is set up with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).

### Custom Bootstrap Compilation

The generated CSS is set up with automatic Bootstrap recompilation with variables of your choice.
Bootstrap v5 is installed using npm and customised by tweaking your variables in `static/sass/custom_bootstrap_vars`.

You can find a list of available variables [in the bootstrap source](https://github.com/twbs/bootstrap/blob/v5.1.3/scss/_variables.scss), or get explanations on them in the [Bootstrap docs](https://getbootstrap.com/docs/5.1/customize/sass/).

Bootstrap's javascript as well as its dependencies are concatenated into a single file: `static/js/vendors.js`.
