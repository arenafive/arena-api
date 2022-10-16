from django.contrib import admin, messages

# Register your models here.
# from django.contrib.contenttypes.admin import GenericTabularInline
# from django.contrib.contenttypes.models import ContentType
from django import forms
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.core.exceptions import ValidationError
from django.shortcuts import resolve_url
from django.utils.html import strip_tags, format_html
from modeltranslation.admin import TranslationAdmin

from api.models import (
    Player,
    Manager,
    Arena,
    InformationDetails,
    Adress,
    Game,
    Media,
    Availability,
    ArenaFiveSettings,
    Payment,
    BankilyPayment,
    PaymentGame,
)
from api.scripts import generate_availabilities


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
    list_filter = ("id", "full_name", "email_adress", "phone_number")
    search_fields = ("id", "full_name", "email_adress", "phone_number")


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "available_at",
        "price",
        "arena",
    )

    list_filter = ("arena",)

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
class AdressAdmin(TranslationAdmin, admin.ModelAdmin):
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
class ArenaAdmin(TranslationAdmin, admin.ModelAdmin):
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
        "availabilities",
    )
    readonly_fields = ("availabilities",)
    inlines = [
        MediaInline,
    ]
    actions = ("generate_availabilities_",)

    @admin.action(description="generer des disponiblités")
    def generate_availabilities_(self, request, queryset):
        count = generate_availabilities(queryset)
        self.message_user(
            request=request,
            level=messages.INFO,
            message=f"des disponibiltés ont/a été créée(s) pour {count} cités",
        )

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
        "payment",
    )
    list_filter = (
        "captain",
        "start_date",
        "status",
        "type",
    )
    readonly_fields = ("reference", "players")
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

    def payment(self, obj):
        return obj.paymentgame_set.first()


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "updated_at", "amount", "phone_number")


@admin.register(BankilyPayment)
class BankilyPaymentAdmin(admin.ModelAdmin):
    list_display = ("transaction_id", "operation_id", "payment")
    search_fields = ("id", "transaction_id", "operation_id")
    list_display_links = ("transaction_id",)

    def payment(self, obj):
        return obj.payment.first()


@admin.register(PaymentGame)
class PaymentGameAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "p",
        "game",
        "player",
        "to_be_refund",
        "refunded",
    )
    search_fields = (
        "id",
        "player__full_name",
        "player__email_adress",
        "player__phone_number",
    )

    def p(self, obj):
        url = resolve_url(admin_urlname(obj.payment._meta, "change"), obj.payment.pk)
        return format_html('<a href="%s">%s</a>' % (url, obj.payment))

    p.allow_tags = True
    p.short_description = "Payment"

    def payment(self, obj):
        return obj.paymentgame_set.first()


@admin.register(ArenaFiveSettings)
class ArenaFiveSettingsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "portable",
        "fix_number",
        "bankily_number",
        "maservi_number",
        "twitter_link",
        "facebook_link",
        "whatsapp_number",
        "created_at",
        "updated_at",
    )


admin.site.site_header = "ARENA Administration"
admin.site.site_title = "ARENA Admin Portal"
admin.site.index_title = "Welcome to ARENA Researcher Portal"
