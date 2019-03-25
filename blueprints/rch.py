from flask import *

bp = Blueprint('rch',__name__,url_prefix="/rch")

@bp.route('/')
def index():
    return render_template("rch/index.html")