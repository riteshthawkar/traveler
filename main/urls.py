from django.urls import path
from .views import *

urlpatterns = [
    path("", index_view, name="index-view"),
    path("about/", about_view, name="about-view"),
    path("services/", service_view, name="service-view"),
    path("packages/", tour_packages_view, name="tour-package-view"),
    path("contact/", contact_view, name="contact-view"),

    path("travel_guide/", travel_guide_view, name="travel-guide-view"),
    path("travel_guide/<int:pk>/", single_travel_guide_view, name="single-travel-guide-view"),

    path('search_packages/', package_Search_view, name="package-search-view"),
    path('package/<int:pk>', single_package_view, name="single-package-view"),

    path('blog/', blog_view, name="blog-view"),
    path('blog/<int:pk>', single_blog_view, name="single-blog-view"),

    path('visa_assistance/', visa_assiatance_view, name="visa-assistance-view"),
    path('visa_guides/', visa_guide_list_view, name="visa-guide-list-view"),
    path('visa_assistance/<int:pk>', single_visa_assiatance_view, name="single-visa-assistance-view"),

    path('chat/', chat_view, name="chat-view"),
    path('process_question/', transcribe_view, name="transcribe-view"),

]
