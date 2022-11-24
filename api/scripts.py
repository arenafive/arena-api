from api.models import Availability


def generate_availabilities(queryset):
    days = (
        "LUNDI",
        "MARDI",
        "MERCREDI",
        "JEUDI",
        "VENDREDI",
        "SAMEDI",
        "DIMANCHE",
    )
    availabilities = []
    count = 0
    for arena in queryset:
        qs = Availability.objects.filter(arena__pk=arena.pk)
        if not qs.exists():
            count += 1
            for day in days:
                av0 = Availability(
                    day=day,
                    start_hour=0,
                    start_minute=0,
                    end_hour=1,
                    end_minute=0,
                    price=5000,
                    arena=arena,
                )
                av1 = Availability(
                    day=day,
                    start_hour=1,
                    start_minute=0,
                    end_hour=2,
                    end_minute=0,
                    price=5000,
                    arena=arena,
                )
                av2 = Availability(
                    day=day,
                    start_hour=2,
                    start_minute=0,
                    end_hour=3,
                    end_minute=0,
                    price=5000,
                    arena=arena,
                )
                availabilities.append(av0)
                availabilities.append(av1)
                availabilities.append(av2)
                for i in range(10, 23):
                    av = Availability(
                        day=day,
                        start_hour=i,
                        start_minute=0,
                        end_hour=i + 1,
                        end_minute=0,
                        price=5000,
                        arena=arena,
                    )
                    availabilities.append(av)
                av3 = Availability(
                    day=day,
                    start_hour=23,
                    start_minute=0,
                    end_hour=0,
                    end_minute=0,
                    price=5000,
                    arena=arena,
                )
                availabilities.append(av3)
    if availabilities:
        Availability.objects.bulk_create(availabilities, batch_size=100)
    return count
