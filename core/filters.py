from django_filters import FilterSet, OrderingFilter

from api.models import Game, Player, Arena, Manager


class GameFilter(FilterSet):
    class Meta:
        model = Game
        fields = {"type": ["exact"], "start_date": ["gte"], "arena__manager": ["exact"]}

    order_by = OrderingFilter(fields=("created_date",))


class PlayerFilter(FilterSet):
    class Meta:
        model = Player
        fields = {
            "full_name": ["exact"],
        }

    order_by = OrderingFilter(fields=("created_at",))


class ManagerFilter(FilterSet):
    class Meta:
        model = Manager
        fields = {
            "full_name": ["exact"],
        }

    order_by = OrderingFilter(fields=("created_at",))


class ArenaFilter(FilterSet):
    class Meta:
        model = Arena
        fields = {
            "slug": ["contains", "icontains"],
            "adress__ville": ["exact"],
        }

    order_by = OrderingFilter(fields=("created_at",))
