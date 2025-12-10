from django.urls import path, include

urlpatterns = [
    path('', include('migration_app.urls')),
]
