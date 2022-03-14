from django_filters import FilterSet, OrderingFilter

from api.models import Game


class GameFilter(FilterSet):
    class Meta:
        model = Game
        fields = {
            "type": ["exact"],
            "start_date": ["gt"],
        }

    order_by = OrderingFilter(fields=("created_date",))
