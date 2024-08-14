import django_filters

from fs_audits.models import AuditTrail
from fs_utils.constants import ICONTAINS, IEXACT


class AuditTrailFilterSet(django_filters.FilterSet):
    actor_email = django_filters.CharFilter(
        field_name="actor__email", lookup_expr=ICONTAINS)

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

    class Meta:
        model = AuditTrail
        fields = ['module', 'id', 'actor_email', 'changes', 'action']
