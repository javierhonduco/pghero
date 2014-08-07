# Basic wsgi middleware to display pghero statistics


class PgHeroWsgi:
    
    def __init__(self, app, mount_path='__pghero__'):
        self.app = app
        self.mount_path = mount_path

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '').lstrip('/')
        if path == mount_path:
            start_response('200 OK', [('Content-Type', 'text/html')])
            return 'This is (going to be) pghero.'
        return self.app(environ, start_response)
