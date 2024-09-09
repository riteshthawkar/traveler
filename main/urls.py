from django.urls import path
from .views import *

urlpatterns = [

    path("", landing_page_view, name="landing-page-view"),
    path("features/", feature_page_view, name="feature-page-view"),
    path("plans/", plan_page_view, name="paln-page-view"),
    path("usecases/", usecases_page_view, name="usecases-page-view"),
    path("privacy-policy", privacy_page_view, name="privacy-page-view"),
    path("terms-and-conditions/", terms_page_view, name="terms-page-view"),


    path("demo/", index_view, name="index-view"),
    path("demo/about/", about_view, name="about-view"),
    path("demo/services/", service_view, name="service-view"),
    path("demo/packages/", tour_packages_view, name="tour-package-view"),
    path("demo/contact/", contact_view, name="contact-view"),

    path("demo/travel_guide/", travel_guide_view, name="travel-guide-view"),
    path("demo/travel_guide/<int:pk>/", single_travel_guide_view, name="single-travel-guide-view"),

    path('demo/search_packages/', package_Search_view, name="package-search-view"),
    path('demo/package/<int:pk>', single_package_view, name="single-package-view"),

    path('demo/blog/', blog_view, name="blog-view"),
    path('demo/blog/<int:pk>', single_blog_view, name="single-blog-view"),

    path('demo/visa_assistance/', visa_assiatance_view, name="visa-assistance-view"),
    path('demo/visa_guides/', visa_guide_list_view, name="visa-guide-list-view"),
    path('demo/visa_assistance/<int:pk>', single_visa_assiatance_view, name="single-visa-assistance-view"),



    path('chat/', chat_view, name="chat-view"),


    # path('chat/', chat_view, name="chat-view"),
    # path('process_question/', transcribe_view, name="transcribe-view"),

]
