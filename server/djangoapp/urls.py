from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view
    path(route='about', view=views.about, name='about'),

    # path for contact us view
    path(route='contact_us', view=views.contact, name='contact_us'),

    # path for registration    
    path(route='registration_request', view=views.registration_request, name='registration_request'),

    # path for login
    path(route='login_request', view=views.login_request, name='login_request'),

    # path for logout
    path(route='logout_request', view=views.logout_request, name='logout_request'),

    path(route='', view=views.get_dealerships, name='index'),

    # path for dealer reviews view
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),

    # path for add a review view

    path('dealer/<int:dealer_id>/add_review', views.add_review, name='add_review')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)