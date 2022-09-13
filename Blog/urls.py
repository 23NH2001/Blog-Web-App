from django.urls import path
from Blog import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name="HomePage"),
    path('register/',views.register_new_user,name="register_new_user"),
    path('login/',views.login_user,name="login_user"),
    path('logout/',views.logout_user,name="logout_user"),
    path('myblog/',views.blogPage,name="blog_page"),
    path('about/',views.aboutPage,name="about_page"),
    path('contact/',views.contactPage,name="contact_page"),
    path('readmore/',views.ReadMoreBlog,name="readmore_page"),
    path('edit/',views.EditBlog,name="edit_blog"),
    path('delete/',views.deleteBlog,name="delete_blog"),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)