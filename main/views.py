from django.shortcuts import render
from .models import *
from .ingest_data import *
import random


# Create your views here.
def landing_page_view(request):
    return render(request, 'landing_page.html')

def feature_page_view(request):
    return render(request, 'features.html')

def plan_page_view(request):
    return render(request, 'plans.html')

def usecases_page_view(request):
    return render(request, 'usecases.html')

def privacy_page_view(request):
    return render(request, 'privacy-policy.html')

def terms_page_view(request):
    return render(request, 'terms.html')

def index_view(request):
    guides = TravelGuide.objects.all()
    guides = random.sample(list(guides), 6)
    tours = Tour_Package.objects.all()
    tours = random.sample(list(tours), 9)
    blogs = Blog.objects.all()
    blogs = random.sample(list(blogs), 3)
    return render(request, "index.html", {'tours': tours, 'guides': guides, 'blogs':blogs})


def about_view(request):
    return render(request, "about.html")


def service_view(request):
    return render(request, "service.html")



def tour_packages_view(request):
    tours = Tour_Package.objects.all()
    tours = random.sample(list(tours), 9)
    return render(request, "package.html", {"tour_packages": tours})

def tour_packages_list_view(request):
    tours = Tour_Package.objects.all()
    return render(request, "package_list.html", {"tour_packages": tours})



from fuzzywuzzy import process

def find_best_match(search_string, keywords):
    """
    Find the best fuzzy match for the search_string in the keywords list.

    :param search_string: The string you want to search for.
    :param keywords: List of keywords to match against.
    :return: The best matching keyword and its score.
    """
    best_match = process.extractOne(search_string, keywords)
    return best_match

def package_Search_view(request):
    search_query = request.GET.get('keyword')

    if search_query is not None:
        packages = Tour_Package.objects.all()
        filtred_packages = []

        for package in packages:
            if search_query.lower() in package.country.lower():
                filtred_packages.append(package)
            else:
                keywords = []

                for place in package.places_to_visit:
                    keywords.append(place['name'].lower())

                for hotel in package.hotels:
                    keywords.append(hotel['name'].lower())

                for res in package.restaurants:
                    keywords.append(res['name'].lower())

                best_match = find_best_match(search_query, keywords)

                if best_match[-1] >= 80:
                    filtred_packages.append(package)
    else:
        filtred_packages = Tour_Package.objects.all()


    return render(request, "package_list.html", {"tour_packages": filtred_packages, "search_query": search_query})


def single_package_view(request, pk):
    package = Tour_Package.objects.get(pk=pk)
    contacts = []
    for key, val in package.emergency_contacts.items():
        key = key.replace("_", " ").title()
        contacts.append((key, val))
    package.emergency_contacts = contacts
    return render(request, "single_package.html", {'package': package})


from django.core.mail import send_mail
from django.conf import settings


def contact_view(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')
            email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            subject = 'Message from lawa.ai User'
            recipient_list = ['riteshthawkar2003@gmail.com', 'contact@lawa.app']
            email_from = settings.DEFAULT_FROM_EMAIL

            send_mail(subject, email_message, email_from, recipient_list)

            return render(request, "contact.html", {'success': "Your message is successfully sent."})
        except Exception as e:
            return render(request, "contact.html", {'error': "Something went wrong. Please try again."})

    return render(request, "contact.html")


def travel_guide_view(request):
    travel_guides = TravelGuide.objects.all()
    return render(request, "travel_guide.html", {"travel_guides": travel_guides})

def single_travel_guide_view(request, pk):
    guide = TravelGuide.objects.get(pk=pk)
    return render(request, "travel_guide_document.html", {"guide": guide})



def blog_view(request):
    blogs = list(Blog.objects.all())
    random.shuffle(blogs)
    return render(request, "blogs.html", {"blogs":blogs})

def single_blog_view(request, pk):
    blog = Blog.objects.get(pk=pk)
    return render(request, "single_blog.html", {"blog": blog})



def visa_assiatance_view(request):
    countries = list(Visa_Assitance.objects.filter(country__in=["United States", "India", "France", "Italy", "Indonesia", "Japan"]).order_by("-country"))
    return render(request, "visa_assistance.html", {"countries": countries[:6]})

def visa_guide_list_view(request):
    countries = list(Visa_Assitance.objects.all())
    random.shuffle(countries)
    return render(request, "visa_guide_list.html", {"countries": countries})

def single_visa_assiatance_view(request, pk):
    visa_guide = Visa_Assitance.objects.get(pk=pk)
    updated_visa_requirements = {}
    for key, value in visa_guide.visa_requirements.items():
        updated_visa_requirements[key.replace("_", " ").title()] = value
    additional_info = {}
    for key, value in visa_guide.additional_info.items():
        additional_info[key.replace("_", " ").title()] = value

    return render(request, "single_visa_guide.html", {"guide": visa_guide, "visa_requirements": updated_visa_requirements, "additional_info": additional_info})


def chat_view(request):
    return render(request, 'base.html')



from django.views.decorators.csrf import csrf_exempt
# from .llm_pipeline import LLMChatPipeline
from django.http import JsonResponse
import timeit

# pipeline = LLMChatPipeline()

# @csrf_exempt
# def chat_view(request):
#     if request.method == 'POST':
#         question = request.POST.get('question', '')

#         starting_time = timeit.default_timer()
#         answer = pipeline.get_answer(question)
#         ending_time = timeit.default_timer()

#         print("=========================================")
#         print("Time Taken: ", ending_time - starting_time)

#         return JsonResponse({'answer': answer})
#     else:
#         return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

# @csrf_exempt
# def transcribe_view(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         question = data.get('question')

#         # Here you would typically process the question and generate an answer
#         # For this example, we'll just echo the question
#         answer = f"You asked: {question}"

#         print(answer)

#         return JsonResponse({'answer': answer})
#     return JsonResponse({'error': 'Invalid request method'}, status=400)
