from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from modeltranslation.admin import TranslationAdmin
from .models import User, City, Rule, Property, PropertyImage, Booking, Review


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3

@admin.register(Property)
class PropertyAdmin(TranslationAdmin):
    list_display = ('title', 'city', 'price_per_night', 'owner', 'is_active')
    inlines = [PropertyImageInline]
    filter_horizontal = ('rules',)
    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(City)
class CityAdmin(TranslationAdmin):
    list_display = ('name',)

@admin.register(Rule)
class RuleAdmin(TranslationAdmin):
    list_display = ('rules_name',)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'avatar')}),
        ('Extra Info', {'fields': ('role', 'phone_number')}),
        ('Status', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'role', 'phone_number', 'is_staff')
    list_filter = ('role', 'is_staff')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('property', 'guest', 'status', 'check_in', 'check_out')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('property', 'guest', 'rating', 'created_at')