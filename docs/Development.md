# Development

## Installation

To avoid porblems with Python versions, we work inside a virtual environment that needs to be setup up at the project installation.

### Virtual environment setup

1. Install Python 3.10
    * Follow the instruction inside [this](https://www.linuxcapable.com/how-to-install-python-3-10-on-ubuntu-22-04-lts/) link

1. Create Python virtual environment using Python 3.10

    ```
    python3.10 -m venv venv
    ```

1. Activate the Python environment

    ```
    source venv/bin/activate
    ```

1. Install requirements

    ```
    pip install -r requirements/base.txt --ignore-installed
    ```

1. Run migrations
    ```
    python manage.py makemigrations core
    python manage.py migrate
    ```

1. Start project and go to http://127.0.0.1:8000/ in browser

    ```
    python manage.py runserver
    ```

