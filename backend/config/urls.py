from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve

from catalog import views as catalog_views
from demandes import views as demandes_views

admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.disable_action("delete_selected")
admin.site.site_title = "PS GROUP — Admin"
admin.site.index_title = "Gestion du site et des demandes"
admin.site.site_url = settings.FRONTEND_URL

api = [
    path("site/", catalog_views.site),
    path("pages/<slug:page>/", catalog_views.page),
    path("entreprises/", catalog_views.entreprises),
    path("entreprises/<slug:slug>/", catalog_views.entreprise_detail),
    path("offres/", catalog_views.offres),
    path("offres/<slug:slug>/", catalog_views.offre_detail),
    path("demandes/", demandes_views.creer_demande),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api)),
    # Les médias sont servis par Django (volume Docker). Derrière Caddy, ils
    # pourront être servis directement par le proxy.
    path("media/<path:path>", serve, {"document_root": settings.MEDIA_ROOT}),
]
