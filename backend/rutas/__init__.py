""" from index import index_bp
from register import register_bp
from login import login_bp
from feed import feed_bp
from curso import curso_bp

blueprints = [index_bp, register_bp, login_bp, feed_bp, curso_bp]
 """
from .index import index_bp
from .register import register_bp
from .login import login_bp
from .feed import feed_bp
from .curso import curso_bp

blueprints = [index_bp, register_bp, login_bp, feed_bp, curso_bp]