from django.urls import path, re_path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'core'

urlpatterns = [
    # Use for GET, PUT, DELETE
    # re_path(r'^order-detail/(?P<id>[\d-]+)/$', views.OrdersDetailView.as_view(), name='order_detail'),
    # # Use for POST, for new order
    re_path(r'^get-expression-by-id/$', views.ExpressionsDetailView.as_view(), name='get_expression'),
    re_path(r'^upload-bulk-expressions/$', views.ExpressionsPostView.as_view(), name='upload_expressions'),
    # re_path(r'update-order/(?P<string>[\w\-]+)/$', views.OrdersDetailView.as_view(), name='update-order'),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)