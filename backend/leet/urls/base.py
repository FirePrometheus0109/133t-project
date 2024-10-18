from django.conf import settings
from django.conf.urls import include
from django.urls import path
from django.conf.urls.static import static

from leet.admin import base_admin_site


main_urlpatterns = [
    path('admin/', base_admin_site.urls),
    path('api/', include('auth.urls', namespace='auth')),
    path('api/', include('apply.urls', namespace='apply')),
    path('api/', include('candidate.urls', namespace='candidate')),
    path('api/', include('comment.urls', namespace='comment')),
    path('api/', include('company.urls', namespace='company')),
    path('api/', include('event.urls', namespace='event')),
    path('api/', include('geo.urls', namespace='geo')),
    path('api/', include('job.urls', namespace='job')),
    path('api/', include('job_seeker.urls', namespace='job-seeker')),
    path('api/', include('letter_template.urls', namespace='letter_template')),
    path('api/', include('log.urls', namespace='log')),
    path('api/', include(
        'notification_center.urls', namespace='notification_center')),
    path('api/', include('permission.urls', namespace='permission')),
    path('api/', include('public_api.urls', namespace='public-api')),
    path('api/', include('subscription.urls', namespace='subscription')),
    path('api/', include('survey.urls', namespace='survey')),
]

static_urlpatterns = static(settings.STATIC_URL, document_root='/')

media_urlpatterns = static(settings.MEDIA_URL, document_root='/')

urlpatterns = main_urlpatterns + static_urlpatterns + media_urlpatterns
