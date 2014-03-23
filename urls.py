from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

from django.contrib import admin
admin.autodiscover()

handler500 = 'rostr.views.custom_500'

urlpatterns = patterns('',
    url(r'^$',                                'rostr.views.index',                                      name="rostr-index"),
    url(r'^parse/$',                          'rostr.views.parse',                                      name="rostr-parse"),
    url(r'^download/(?P<accesstoken>\w+)/?$', 'rostr.views.download',                                   name="rostr-download"),
    url(r'^help/?$',                          TemplateView.as_view(template_name='rostr/help.html'),    name="rostr-help"),
    url(r'^bm.js?$', 'rostr.views.serve_bookmarklet', name="roster-serve_bookmarklet"),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('django.contrib.auth.views', url(r'^login/$', 'login', {'template_name': 'login.html'}))
