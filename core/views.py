from core import app
from flask import render_template, flash, redirect, url_for, request


@app.route('/')
def index():
    return redirect(url_for('books.showBooks'))

