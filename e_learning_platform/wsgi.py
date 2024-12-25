from django.core.wsgi import get_wsgi_application
import os
import sys

# path = '/home/abdoelshaikh/e_learning_platform'
# if path not in sys.path:
#     sys.path.append(path)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_learning_platform.settings')

application = get_wsgi_application()

app = get_wsgi_application()
