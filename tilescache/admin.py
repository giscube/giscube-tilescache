from django.contrib import admin

from tilescache.models import Service, Layer


class LayerInline(admin.StackedInline):
    model = Layer
    extra = 0


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = (LayerInline,)

admin.site.register(Service, ServiceAdmin)
