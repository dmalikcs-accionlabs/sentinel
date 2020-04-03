import django.views.static
import django.views.generic
from django.urls import path, include, \
    re_path
from django.contrib import admin
from django.conf import settings
from .views import home

admin.site.site_header = 'Sentinel: Email parser'

class SettingsTemplateView(django.views.generic.TemplateView):
    def get_context_data(self, **kwargs):
        context = super(SettingsTemplateView, self).get_context_data(**kwargs)
        context['settings'] = settings
        return context


urlpatterns = [
    path('robots.txt', SettingsTemplateView.as_view(
        template_name='robots.txt', content_type='text/plain'
    )),
    path('', home, name="home"),
    path('admin/', admin.site.urls),
    path('collector/', include(('collector.urls', 'collector'), namespace='collector'),)
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        re_path('media/(?P<path>.*)', django.views.static.serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
        path('__debug__/', include(debug_toolbar.urls)),
    ]