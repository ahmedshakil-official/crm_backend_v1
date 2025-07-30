from django.urls import path
from .views import MortgageEnquiryAPIView

urlpatterns = [
path(
        "network/mortgage/enquiry/",
        MortgageEnquiryAPIView.as_view(),
        name="network-dashboard",
    ),
]
