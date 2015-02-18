from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import password_change,password_change_done
from django.conf import settings
from django.conf.urls.static import static
from registration.backends.simple.views import RegistrationView

# Make a new class that redirects the user to the index page, if successful at logging in
class MyRegistrationView(RegistrationView):
    def get_success_url(self,request,user):
        return '/rango/'

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'tango_with_django_project.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^rango/', include('rango.urls')),
                       url(r'^accounts/change_password/$', password_change, name='password_change'),
                       url(r'^accounts/change_password_done/$', password_change_done, name='password_change_done'),
                       url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
                       url(r'^accounts/', include('registration.backends.simple.urls')),
                       )

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
         'serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
else:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )