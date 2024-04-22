from django.urls import path
from . import views
from rest_framework.routers import DefaultRouterf

   
router = SimpleRouter()
router.register('', views.HomeViewSet)
router.register('products/', views.views.ProductsViewSet)
   
app_name = 'home'
#app_name = namespace
urlpatterns = [
    path('detail/<int:id>/', views.Product_detail, name='detail'),
    path('category/<slug>/<int:id>/', views.All_product, name='category'),
    path('like/<int:id>/', views.product_like, name='product_like'),
    path('unlike/<int:id>/', views.product_unlike, name='product_unlike'),
    path('comment/<int:id>/', views.product_comment, name='product_comment'),
    path('reply/<int:id>/<int:comment_id>/', views.product_reply, name='product_reply'),
    path('like_comment/<int:id>/', views.comment_like, name='comment_like'),
    path('search/', views.product_search, name='product_search'),
    path('favorite/<int:id>', views.favorite_product, name='favorite_product'),
    path('contact/', views.contact, name='contact'),
]
