from flask import Blueprint, jsonify, request

from .db import get_db

bp = Blueprint('contract', __name__)


@bp.route('/')
def list_contracts():
    columns = ['id', 'debt', 'is_open', 'closed_on']
    cmd = 'SELECT {columns} FROM contract'.format(columns=', '.join(columns))

    is_open = request.args.get('is_open', '')
    if is_open.upper() in ['TRUE', 'FALSE']:
        cmd += f' WHERE is_open = {is_open}'

    rows = get_db().execute(cmd).fetchall()

    contracts = [dict(zip(columns, row)) for row in rows]
    return jsonify(contracts)
