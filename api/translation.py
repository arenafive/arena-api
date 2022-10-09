from modeltranslation.translator import register, TranslationOptions
from api.models import Arena, Adress


@register(Arena)
class ArenaTranslationOptions(TranslationOptions):
    fields = (
        "slug",
        "description",
    )


@register(Adress)
class AdressTranslationOptions(TranslationOptions):
    fields = ("ville", "quartier", "description")
