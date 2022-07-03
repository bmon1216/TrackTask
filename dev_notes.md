Development Notes

Uses the Flask framework for web app
    
    Flask Notes and Commands:

        Install Flask to the venv
            python3 -m pip install Flask
    
        Run the Flask app:
            python -m flask run
    

Flask uses the HTTP protocol for serving requests between client and server

    GET - ideal for retrieving data
    POST - ideal for submitting data, resulting in modification of state
    PUT - for replacing server’s target resource with request resource
    DELETE - for deleting a server resource 

Templates

    Use templates to render HTML 
    render_template allows use to pass an argument to the HTML, such as name=
    

    We are using flask_wtf for forms/
    {{  form.hidden_tag() }} is a method we use on the register.jinja2 template which adds a CSRF token to protect the data

    

We use the Jinja2 template engine to allow us to insert logic and some level of dynamic nature
    
    Here is a list of delimiter options of Jinja2:

    {% ... %} for code statements
    {{ ... }} for printing an expression to the template
    {# ... #} for comments not included in the template output
    # ... ## for line statements

Static Assets
    
    CSS and JS files that complement the HTML code of your website need to be in a directory named 'static.'
    
    use the static folder to serve other static assets like images, gifs etc that can be used in our web pages.

Database
    
    Using flask sql alchemy
    
    pip install flask-sqlalchemy


Authentication
    Using flask-bcrypt
    
    # To generate a hashed password
    from flask_bcrypt import Bcrypt
    bcrypt = Bcrypt()
    bcrypt.generate_password_hash('password').decode('utf-8')
    
    # To verify / authenticate a password
    from flask_bcrypt import Bcrypt
    bcrypt = Bcrypt()
    
    # save a hashed password as a variable
    hashed_pw = bcrypt.generate_password_hash('password').decode('utf-8')
    
    # use bcrypt.check_password_hash to check password against saved variable
    bcrypt.check_password_hash(hashed_pw, 'test')
        returns False
    bcrypt.check_password_hash(hashed_pw, 'password')
        returns True


