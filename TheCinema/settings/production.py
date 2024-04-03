"""
    Production settings for project security and other
    necessary settings for project production should be configured
    before project production.

"""


ALLOWED_HOSTS = []

# security
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
