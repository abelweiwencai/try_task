import functools
from werkzeug.exceptions import abort
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, Response
)
from werkzeug.security import check_password_hash, generate_password_hash
import hashlib
from . import utils
from flaskr.db import get_db
import json

bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@bp.route('/register', methods=('POST',))
def register():
    req_data = request.get_json()
    username = req_data.get('username', None)
    password = req_data.get('password', None)
    email = req_data.get('email', None)
    db = get_db()
    error = None

    if not utils.validate_username(username):
        error = '用户名必填，长度为 5-20个字符，只能为字母和数字.'
    elif not utils.validate_password(password):
        error = '密码必填，长度为8-20个字符，至少要有一个大写字母，一个小写字母，一个特殊字符.'
    elif not utils.validate_email(email):
        error = 'Please fill correct email.'

    user = db.execute(
        'SELECT * FROM user WHERE username = ? or email = ?', (username, email)
    ).fetchone()
    if user is not None:
        if user['username'] == username:
            error = f'Username {username} has exists.'
        else:
            error = f'Email {email} has exists.'

    if error is None:
        try:
            db.execute(
                f"INSERT INTO user (username, password, email) VALUES (?, ?, ?)",
                (username, generate_password_hash(password), email),
            )
            db.commit()
        except db.IntegrityError:
            error = f"User {username} is already registered."
        else:
            return {'code': 201, 'msg': 'register success'}
    return jsonify({'code': 400, 'msg': error})


@bp.route('/login', methods=('POST',))
def login():
    form_data = request.get_json()
    username = form_data.get('username', '')
    password = form_data.get('password', '')
    remember_me = form_data.get('remember', False)
    db = get_db()
    error = None
    user = db.execute(
        'SELECT * FROM user WHERE username = ? or email = ?', (username, username)
    ).fetchone()

    if user is None:
        error = 'Incorrect username or email.'
    elif not check_password_hash(user['password'], password):
        error = 'Incorrect password.'

    if error is None:
        session.clear()
        session['user_id'] = user['id']
        if remember_me:
            session.permanent = True
             # 设置session到期时间
        return jsonify({'code': 200})

    return jsonify({'code': 400, 'msg': error})


@bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    print('logout !!!')
    return {'code': 200}


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return jsonify({'code': 403, 'msg': 'login required'})
        return view(**kwargs)

    return wrapped_view


@bp.route('/info', methods=('GET',))
@login_required
def get_user_info():
    return jsonify({
        'code': 200,
        'data': {
            'username': g.user['username'],
            'email': g.user['email']
        }
    })


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
