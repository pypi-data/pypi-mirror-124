A package with basic calculator functions: addition, subtraction, multiplication, division, root.

#### INSTALLATION
    pip install not-so-basic-calculator

#### VIRTUAL ENVIRONMENT SETUP
1. navigate to project's root directory
2. create the new virtual environment with:

    `python3 -m venv venv`
3. activate venv with:

    `source venv/bin/activate`

You should see '(venv)' at the end of your terminal prompt line which indicates that virtual environment is active.

To run tests:

    pytest

To generate 'requirements.txt' file with dependencies of the project:

    pip freeze > requirements.txt