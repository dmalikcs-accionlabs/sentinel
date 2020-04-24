import django.views.static
import django.views.generic
from django.urls import path, include, \
    re_path
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from .views import home,login_redirect,logout_redirect,DashboardLogin,DashboardLogout
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site

admin.site.site_header = 'Sentinel: Email parser'

class SettingsTemplateView(django.views.generic.TemplateView):
    def get_context_data(self, **kwargs):
        context = super(SettingsTemplateView, self).get_context_data(**kwargs)
        context['settings'] = settings
        return context

admin.site.login = DashboardLogin.as_view()
admin.site.logout = DashboardLogout.as_view()
urlpatterns = [
    path('robots.txt', SettingsTemplateView.as_view(
        template_name='robots.txt', content_type='text/plain'
    )),
    path('', home, name="home"),
    path('admin/', admin.site.urls),
    path('collector/', include(('collector.urls', 'collector'), namespace='collector'), ),
    path('oauth2/', include('django_auth_adfs.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        re_path('media/(?P<path>.*)', django.views.static.serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
        path('__debug__/', include(debug_toolbar.urls)),
    ]

admin.site.unregister(Group)
admin.site.unregister(Site)