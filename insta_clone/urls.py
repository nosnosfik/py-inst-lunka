from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from posts import views as post_views

urlpatterns = [
                  path("", post_views.PostList.as_view(), name='home'),
                  path('admin/', admin.site.urls),
                  path('register/', user_views.register, name='register'),
                  path('login/', user_views.user_login, name='login'),
                  path("logout", user_views.user_logout, name='logout'),
                  path('new_post/', post_views.PostCreate.as_view(), name='new_post'),
                  path('<pk>/delete/', post_views.PostDelete.as_view(), name='post_delete'),
                  path('<pk>/like/', post_views.like, name='likes'),
                  path('<pk>/comment/', post_views.comment, name='comment')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
