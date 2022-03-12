from django.contrib import admin

# Register your models here.
# from django.contrib.contenttypes.admin import GenericTabularInline
# from django.contrib.contenttypes.models import ContentType
from django.utils.html import strip_tags, format_html

from api.models import Player, Manager, Arena, InformationDetails, Adress, Game


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


class DetailInline(admin.TabularInline):
    model = InformationDetails
    max_num = 1


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "phone_number",
        "email_adress",
    )
    list_filter = ("id", "full_name", "email_adress")


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


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        "created_date",
        "start_date",
        "end_date",
        "type",
        "organised_by",
        "attendee",
        "score",
    )
    filter_horizontal = ("players",)

    def attendee(self, obj):
        list = "<ul>"
        for p in obj.players.all():
            list += f"<li>{strip_tags(p.full_name)}</li>"
        list += "</ul>"

        return format_html(list)


admin.site.site_header = "ARENA Administration"
admin.site.site_title = "ARENA Admin Portal"
admin.site.index_title = "Welcome to ARENA Researcher Portal"
