from website import create_app
from flask import Blueprint, render_template
app = create_app()

if __name__ == '__main__':
    # only if run then execute not when import
    app.run(debug=True)
    # true for refreshing everytime a change occurs
    # false for production
