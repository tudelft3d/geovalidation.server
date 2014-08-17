from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from val3dity import app as val3dity_app
from prepair  import app as prepair_app
from welcome  import app as welcome_app

application = DispatcherMiddleware( 
    welcome_app, {
    '/val3dity':    val3dity_app,
    '/prepair':     prepair_app
    }
)

if __name__ == '__main__':
    run_simple('localhost', 5000, application, use_reloader=True)


