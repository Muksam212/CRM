from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('register/', views.registerPage, name='register'),
	path('login/', views.loginPage, name='login'),
	path('logout/', views.logoutPage, name='logout'),
	path('', views.homePage, name='home'),
	path('update_order/<int:pk>/', views.order_update, name='update_order'),
	path('delete_order/<int:pk>/', views.order_delete, name='delete_order'),
	path('user/', views.userPage,name='user_page'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)