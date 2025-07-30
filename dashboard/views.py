from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from case.models import Case
from common.enums import ProductCategoryChoices, CaseStageChoices
from dashboard.serializers import MortgageEnquirySerializer
from organization.models import NetworkUser


class MortgageEnquiryAPIView(ListAPIView):
    serializer_class = MortgageEnquirySerializer
    permission_classes = [IsAuthenticated]

    def get_networks(self):
        user = self.request.user
        network_users = NetworkUser.objects.filter(user=user)
        if not network_users.exists():
            raise NotFound("You are not assigned to any network.")
        return [nu.network for nu in network_users]

    def get_queryset(self):
        return Case.objects.filter().order_by("id")[:1]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['networks'] = self.get_networks()
        context['filter'] = self.request.query_params.get('filter', 'all')
        return context
