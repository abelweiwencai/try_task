from flask import (
    Blueprint, flash, g, redirect, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from .auth import login_required
from .db import get_db
from . import config

bp = Blueprint('comment', __name__, url_prefix='/api/comment')


@bp.route('/', methods=('GET', 'POST'))
def comment_view():
    if request.method == 'POST':
        if g.user is None:
            return {'code': 403, 'msg': 'you can post a comment after you login.'}
        req_data = request.get_json()
        content = req_data.get('content', '')
        parent_id = req_data.get('parent', 0)
        error = None
        if not (config.MIN_COMMENT_LEN <= len(content) <= config.MAX_COMMENT_LEN):
            error = f'字数必须在{config.MIN_COMMENT_LEN} ~ {config.MAX_COMMENT_LEN} 之间。'

        if error is not None:
            return jsonify({
                'code': 400,
                'msg': error
            })
        else:
            db = get_db()
            depth = 0
            parent_path = '/'
            # path = f"{'0' * config.MAX_COMMENT_ID_LEN}/"
            if parent_id:
                try:
                    parent_comment = db.execute(
                        f'SELECT * FROM comment Where id = {parent_id};'
                    ).fetchone()
                except Exception as e:
                    print(e)
                    return {'code': 500, 'msg': 'Unknown error.'}
                if parent_comment is None:
                    return {'code': 400, 'msg': f'Can`t not reply for a not exists comment.'}
                depth = parent_comment['depth'] + 1
                #
                # curr_path = str(parent_comment["id"]).rjust(config.MAX_COMMENT_ID_LEN, '0')
                # path = f'{parent_comment["path"].rstrip("/")}.{curr_path}/'
                parent_path = parent_comment["path"]
            sql = f'select max(depth_id) as depth_id from comment where parent_path = "{parent_path}"'
            res = db.execute(sql).fetchone()
            if res['depth_id'] is None:
                max_depth_id = 1
            else:
                max_depth_id = res['depth_id'] + 1

            curr_path = str(max_depth_id).rjust(config.MAX_COMMENT_ID_LEN, '0')
            path = f'{parent_path.rstrip("/")}.{curr_path}/'

            print(max_depth_id, '------')

            sql = f'INSERT INTO comment (author_id, parent_id, content, depth, depth_id, path, parent_path)' \
                  f' VALUES ({g.user["id"]}, {parent_id}, "{content}", {depth}, {max_depth_id}, "{path}", "{parent_path}")'
            try:
                db.execute(sql)
                db.commit()
            except Exception as e:
                print(e)
                print(sql)
                return {'code': 500, 'msg': 'comment add failed. Unknown error.'}
            else:
                return {'code': 201, 'msg': 'comment added.'}

    elif request.method == 'GET':
        db = get_db()
        try:
            comments = db.execute(
                'SELECT c.*, j.username FROM comment c left join user j'
                ' where c.author_id = j.id order by c.path desc;').fetchall()
        except Exception as e:
            print(e)
            return {'code': 500, 'msg': 'Unknown error.'}
        else:
            comments = [{'id': comment['id'],
                         'username': comment['username'],
                         'parent_id': comment['parent_id'],
                         'content': comment['content'],
                         'depth': comment['depth'],
                         'path': comment['path'],
                         'created': comment['created']}
                        for comment in comments]
            return jsonify({
                'code': 200,
                'data': comments,
                'msg': 'success'
            })
