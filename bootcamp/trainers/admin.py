from django.contrib import admin
from .models import Trainer


admin.site.site_header = 'Trainer adminstration'
admin.site.index_title = 'Bootcamp admin'
admin.site.site_title = 'Trainer management'


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'subject')
	list_display_links = ('first_name', 'last_name')
	list_filter = ('subject',)
	ordering = ('first_name', 'last_name')
	search_fields = ('first_name', 'last_name', 'subject')
	list_per_page = 15
