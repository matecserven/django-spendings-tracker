from django.urls import re_path
from custom_spendings import views

urlpatterns = [
    re_path(r'^api/spendings$', views.spending_list),
    re_path(r'^api/spendings/(?P<spending_id>[0-9]+)$', views.spending_detail),
    re_path(r'^api/spendings/(?P<order>asc|desc)$', views.spending_ordered_list)
]
