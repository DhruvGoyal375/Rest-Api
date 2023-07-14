from django.urls import path, include
from home.views import person, login, PersonAPI, PeopleViewSet, RegisterAPI, LoginAPI
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'people', PeopleViewSet, basename='people')
urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('person/', person),
    # path('login/', login),
    path('persons/', PersonAPI.as_view())
]
