from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from ipm_learning.pages.views import AboutPageView, HomePageView, subscription
from ipm_learning.content.models import Course

info_dict = {
    'queryset': Course.objects.all(),
}

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    # path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    # path(
    #     "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    # ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),

    # Content
    path("learn/", include("ipm_learning.content.urls", namespace="content")),
    path("order/", include("ipm_learning.order.urls", namespace="order")),
    path("comeback/", include("ipm_learning.comeback.urls", namespace="comeback")),

    # User management
    path("users/", include("ipm_learning.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    
    # Your stuff: custom urls includes go here
    path('subscribe/', subscription, name="subscription"),
    # path("email-test/",TemplateView.as_view(template_name="account/email/payment_success.html")),
    path('tinymce/', include('tinymce.urls')),
    path('forest', include('django_forest.urls')),
    path("robots.txt",TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml', sitemap,
        {'sitemaps': {'course': GenericSitemap(info_dict, priority=0.6)}},
        name='django.contrib.sitemaps.views.sitemap'),
    path("__reload__/", include("django_browser_reload.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
