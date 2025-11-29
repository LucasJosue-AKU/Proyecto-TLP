from rest_framework import routers
from .api import LibroViewSet
router = routers.DefaultRouter()

router.register('api/projects', LibroViewSet, 'projects')

urlpatterns = router.urls
#ocupe la framwork para importar el comando routers que me genera automaricamente las urls para el crud