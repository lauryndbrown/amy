from django_filters import rest_framework as filters
from consents.models import Term


class TermFilter(filters.FilterSet):
    class Meta:
        model = Term
        fields = ("slug", "content", "required_type")
