"""issuetracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from accounts import urls as urls_accounts
from issues import urls as urls_issues
from cart import urls as urls_cart
from checkout import urls as urls_checkout
from issues.views import get_issues
from .settings import MEDIA_ROOT
import notifications.urls


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', get_issues, name='index'),
    url(r'^issues/', include(urls_issues)),
    url(r'^accounts/', include(urls_accounts)),
    url(r'^cart/', include(urls_cart)),
    url(r'^checkout/', include(urls_checkout)),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
]

