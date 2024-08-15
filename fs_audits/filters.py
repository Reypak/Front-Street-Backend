import django_filters
from django.db.models import Q
from fs_audits.models import AuditTrail
from fs_utils.constants import ICONTAINS, IEXACT


class AuditTrailFilterSet(django_filters.FilterSet):
    actor_name = django_filters.CharFilter(
        method='advanced_filter', lookup_expr=ICONTAINS)

    module = django_filters.CharFilter(
        field_name="model_name", lookup_expr=IEXACT)

    changes = django_filters.CharFilter(
        lookup_expr=ICONTAINS)
    ref_number = django_filters.CharFilter(field_name="object_id",
                                           lookup_expr=ICONTAINS)

    # reperesents the object_id , id of the object in the module
    id = django_filters.CharFilter(
        field_name="object_id", lookup_expr=IEXACT)

    action = django_filters.CharFilter()

    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = AuditTrail
        fields = ['module', 'id', 'actor_name',
                  'changes', 'action', 'created_at']

    def advanced_filter(self, queryset, name, value):
        return queryset.filter(
            Q(actor__first_name__icontains=value) |
            Q(actor__last_name__icontains=value)
        )
