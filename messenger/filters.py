from django_filters import rest_framework as filters

from base.filters import NumberInFilter
from messenger.models import Message


class MessageFilter(filters.FilterSet):
    tags = NumberInFilter(field_name='tags__id')
    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Message
        fields = ("tags", "created_at")

    # @property
    # def qs(self):
    #     queryset = super().qs
    #     user = getattr(self.request, 'user', None)
    #
    #     return queryset.filter(user=user)
