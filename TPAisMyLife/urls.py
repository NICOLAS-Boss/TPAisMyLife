from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from blog.forms import *
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^logout$', auth_views.logout,{'next_page':'/'},name='logout'),
        url(r'^login/$',
        'django.contrib.auth.views.login',
        {
            'template_name': 'registration/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Авторизация',

            }
        },
        name='login'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'', include('blog.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
