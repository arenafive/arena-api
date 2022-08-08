from django.contrib import admin

# Register your models here.
# from django.contrib.contenttypes.admin import GenericTabularInline
# from django.contrib.contenttypes.models import ContentType
from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags, format_html

from api.models import (
    Player,
    Manager,
    Arena,
    InformationDetails,
    Adress,
    Game,
    Media,
    Availability,
)


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = "__all__"

    def clean_players(self):
        type = self.cleaned_data["type"]
        players = self.cleaned_data["players"]

        if len(players) > int(type):
            raise ValidationError(
                f"Only {type} players are allowed to increase players change type of game."
            )
        return players


class DetailAdminMixin:
    list_display = (
        "id",
        "full_name",
        "phone_number",
        "email_adress",
    )

    def content_object(self, obj) -> InformationDetails:
        pass

    def full_name(self, obj):
        return self.content_object(obj).full_name

    def phone_number(self, obj):
        return self.content_object(obj).phone_number

    def email_adress(self, obj):
        return self.content_object(obj).email_adress


class AvailabilityInline(admin.TabularInline):
    model = Availability


class MediaInline(admin.StackedInline):
    model = Media


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "phone_number",
        "email_adress",
    )
    list_filter = ("id", "full_name", "email_adress")


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "available_at",
    )

    def available_at(self, obj) -> str:
        return f"{obj.day} : {obj.start_hour}h:{obj.start_minute}min - {obj.end_hour}h:{obj.end_minute}min"


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "updated_at", "url")
    list_filter = ("id", "created_at", "updated_at", "url")


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin, DetailAdminMixin):
    # manager_type = ContentType.objects.get_for_model(Manager)
    list_display = (
        "id",
        "full_name",
        "phone_number",
        "email_adress",
    )
    list_filter = ("id", "full_name", "email_adress")

    """def get_list_display(self, request):
        return DetailAdminMixin.list_display"""

    """def content_object(self, obj):
        return UserDetail.objects.get(content_type=self.manager_type, object_id=obj.pk)"""


@admin.register(Adress)
class AdressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "ville",
        "quartier",
        "longitude",
        "latitude",
        "longitudeDelta",
        "latitudeDelta",
        "description",
    )
    list_filter = (
        "id",
        "ville",
        "quartier",
    )


@admin.register(Arena)
class ArenaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "slug",
        "adress",
        "manager",
        "note",
        "is_partener",
        "description",
        "availabilities",
    )
    list_filter = (
        "id",
        "slug",
        "adress__ville",
        "adress__quartier",
        "manager",
        "note",
        "is_partener",
        "description",
    )
    inlines = [
        MediaInline,
        AvailabilityInline,
    ]

    def availabilities(self, obj):
        list = "<ul>"
        for av in obj.availabilities.all():
            list += f"<li>{strip_tags(str(av))}</li>"
        list += "</ul>"

        return format_html(list)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created_date",
        "start_date",
        "end_date",
        "type",
        "captain",
        "attendee",
        "score",
        "reference",
        "status",
        "amount",
    )
    list_filter = (
        "captain",
        "start_date",
        "status",
        "type",
    )
    readonly_fields = ("reference",)
    search_fields = (
        "id",
        "reference",
    )
    form = GameForm

    def attendee(self, obj):
        list = "<ul>"
        for p in obj.players.all():
            list += f"<li>{strip_tags(p.full_name)}</li>"
        list += "</ul>"

        return format_html(list)


admin.site.site_header = "ARENA Administration"
admin.site.site_title = "ARENA Admin Portal"
admin.site.index_title = "Welcome to ARENA Researcher Portal"
