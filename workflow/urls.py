from django.urls import path
from .views import create_form, approve_form,all_approved_forms,all_pending_forms,my_approved_forms,my_pending_forms,form_details

urlpatterns = [
    path("create/", create_form),
    path("approve/<int:form_id>/", approve_form),
    path("all/approved/", all_approved_forms),
    path("all/pending/", all_pending_forms),
    path("my/approved/", my_approved_forms),
    path("my/pending/", my_pending_forms),
    path("details/<int:form_id>/", form_details),






]
