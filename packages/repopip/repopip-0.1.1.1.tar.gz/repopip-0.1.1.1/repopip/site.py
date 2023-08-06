import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from repopip.local_repo.repo import Repo

repo = Repo()

bp = Blueprint('site', __name__)

@bp.route('/')
def index():
    return render_template('pages/index.html.j2', terminal = True)


@bp.route('/contacto')
def contacto():
    return render_template('pages/contact.html.j2')


@bp.route('/packages')
def packages():
    packages = repo.packages
    return render_template('pages/packages.html.j2', packages = packages, total = len(packages), size = repo.size)
