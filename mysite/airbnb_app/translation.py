from modeltranslation.translator import register, TranslationOptions
from .models import City, Rule, Property

@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Rule)
class RuleTranslationOptions(TranslationOptions):
    fields = ('rules_name',)

@register(Property)
class PropertyTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'address')