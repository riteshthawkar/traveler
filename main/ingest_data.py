import os
import json
import re
from .models import *
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
import shutil



def download_images(query, num_images=5):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.123 Safari/537.36"
    }
    search_url = f"https://unsplash.com/s/photos/{query}?orientation=landscape&license=free"
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    try:
        img_container = soup.find("div", class_="bugb2")
        image_urls = []
        for img_tag in img_container.find_all("figure"):
            img_url = img_tag.find_all("img")[-1].get("srcset").split(",")[-1].strip()
            if img_url and img_url.startswith("http"):
                image_urls.append(img_url)
                if len(image_urls) >= num_images:
                    break
    except Exception as e:
        img_container = soup.find("div", class_="bugb2")
        image_urls = []
        for img_tag in img_container.find_all("figure"):
            img_url = img_tag.find_all("img")[-1].get("srcset").split(",")[-1].strip()
            if img_url and img_url.startswith("http"):
                image_urls.append(img_url)
                if len(image_urls) >= num_images:
                    break
        

    return image_urls


    # for i, img_url in enumerate(image_urls):
    #     try:
    #         img_response = requests.get(img_url)
    #         img = Image.open(BytesIO(img_response.content))
    #         img_path = os.path.join(save_dir, f"image_{i+1}.jpg")
    #         img.save(img_path)
    #         print(f"Downloaded {img_path}")
    #     except Exception as e:
    #         print(f"Failed to download image from {img_url}. Error: {e}")



def ingest_travel_guides():
    DATA_DIR = "/home/fahadkhan/Desktop/traveler/main/guides/new_guides"
    guide_files = os.listdir(DATA_DIR)
    for guide_file in guide_files:
        file_path = os.path.join(DATA_DIR, guide_file)
        with open(file_path, 'r') as fp:
            print(file_path)
            content = fp.read()
            json_data = json.loads(content)

            city=json_data['city']
            country=json_data["country"]

            activities_json = json_data['activities']
            tips_json = json_data['tips_and_tricks']


            img_query = city+" "+country
            image_url = download_images(img_query, num_images=2)[-1]
            img_response = requests.get(image_url)
            img = Image.open(BytesIO(img_response.content))
            img_path = os.path.join("/home/fahadkhan/Desktop/traveler/main/guides/images", f"{city}.jpg")
            img.save(img_path)

            travel_guide_obj = TravelGuide(
                city_name=json_data['city'], 
                country_name=json_data["country"] , 
                description=json_data['description'], 
                activities = activities_json,
                tips = tips_json
            )
            travel_guide_obj.save()
            with open(img_path, "rb") as img_file:
                img = File(img_file)
                travel_guide_obj.img.save(f"{city}.jpg", img, save=True)

            for place in json_data['tourist_places']:
                tourist_place_obj = Tourist_Place(place_name=place['name'], description=place['description'], travel_guide=travel_guide_obj)
                tourist_place_obj.save()

            for hotel in json_data['hotels']:
                hotel_obj = Hotel(hotel_name=hotel['name'], description=hotel['description'], travel_guide=travel_guide_obj)
                hotel_obj.save()

            for res in json_data['restaurants']:
                restaurant_obj = Restaurant(restaurant_name=res['name'], description=res['description'], travel_guide=travel_guide_obj)
                restaurant_obj.save()
            
            for contact, value in json_data['emergency_contact_numbers'].items():
                contact_name = contact.replace("_", " ").title()
                contact_obj = Emergency_Contact(entity=contact_name, value=value, travel_guide=travel_guide_obj)
                contact_obj.save()
            
            fp.close()
            shutil.move(file_path, "/home/fahadkhan/Desktop/traveler/main/guides/"+guide_file)


def ingest_tour_packages():
    DATA_DIR = "C:/Users/Ritesh/Desktop/travel_website/traveler/main/new_tour_packages"
    tour_files = os.listdir(DATA_DIR)
    for tour in tour_files:
        file_path = os.path.join(DATA_DIR, tour)
        with open(file_path, 'r') as fp:
            content = fp.read()
            json_data = json.loads(content)
            tour_obj = Tour_Package(
                package_name = json_data['package_name'],
                description = json_data['region_description'],
                country = json_data['country'],
                duration = json_data['duration_days'],
                cost = int(json_data['tour_cost_usd']) * 5,
                rating = json_data['customer_rating'],
                places_to_visit = json_data['places_to_visit'],
                hotels = json_data['hotels_and_restaurants'][0]['hotels'],
                restaurants = json_data['hotels_and_restaurants'][0]['restaurants'],
                activities = json_data['activities'],
                tips = json_data['tips_and_tricks'],
                timeline = json_data['timeline'],
                emergency_contacts = json_data['emergency_contacts'],
                reviews = json_data['customer_reviews']
            )

            tour_obj.save()



def ingest_blogs():
    h1_re = r'<h1\b[^>]*>(.*?)<\/h1>'
    content_removal_pattern = r'<h1\b[^>]*>.*?<\/h1>|<img\b[^>]*\/?>'

    DATA_DIR = "/home/fahadkhan/Desktop/traveler/main/blogs/new_set"
    # DATA_DIR = blog_dir
    tour_files = os.listdir(DATA_DIR)
    for tour in tour_files:
        file_path = os.path.join(DATA_DIR, tour)
        with open(file_path, 'r') as fp:
            print(file_path)
            content = fp.read()
            json_data = json.loads(content)
            city = json_data["city"]
            country = json_data["country"]
            heading = re.search(h1_re, json_data["blog"], re.IGNORECASE).group(1)
            content = re.sub(content_removal_pattern, '', json_data["blog"], flags=re.IGNORECASE)

            img_query = city+" "+country
            image_url = download_images(img_query, num_images=1)[0]
            img_response = requests.get(image_url)
            img = Image.open(BytesIO(img_response.content))
            img_path = os.path.join("/home/fahadkhan/Desktop/traveler/main/blogs/images", f"{city}.jpg")
            img.save(img_path)

            with open(img_path, "rb") as img_file:
                img = File(img_file)
                blog_obj = Blog(
                    city = city,
                    country = country,
                    content = content,
                    heading = heading,
                    # img = img
                )
                blog_obj.save()
                blog_obj.img.save(f"{city}.jpg", img, save=True)
                shutil.move(file_path, "/home/fahadkhan/Desktop/traveler/main/blogs/"+tour)



def ingest_visa_info():
    h1_re = r'<h1\b[^>]*>(.*?)<\/h1>'
    content_removal_pattern = r'<h1\b[^>]*>.*?<\/h1>|<img\b[^>]*\/?>'

    DATA_DIR = "/home/fahadkhan/Desktop/traveler/main/visa_assistance"
    # DATA_DIR = blog_dir
    tour_files = os.listdir(DATA_DIR)
    for tour in tour_files:
        file_path = os.path.join(DATA_DIR, tour)
        with open(file_path, 'r') as fp:
            print(file_path)
            content = fp.read()
            json_data = json.loads(content)
            country = json_data["country_name"]
            overview = json_data["visa_guide"]["country_overview"]["content"]
            visa_types = json_data["visa_guide"]["types_of_visas"]
            visa_requirements = json_data["visa_guide"]["visa_requirements"]
            visa_process = json_data["visa_guide"]["step_by_step_visa_application_process"]
            additional_info = json_data["visa_guide"]["additional_information"]
            faqs = json_data["visa_guide"]["faqs"]

            img_query = "beautiful places in "+ country
            image_url = download_images(img_query, num_images=1)[0]
            img_response = requests.get(image_url)
            img = Image.open(BytesIO(img_response.content))
            img_path = os.path.join("/home/fahadkhan/Desktop/traveler/visa_data/images", f"{country}.jpg")
            img.save(img_path)

            with open(img_path, "rb") as img_file:
                img = File(img_file)
                visa_obj = Visa_Assitance(
                    country = country,
                    overview = overview,
                    visa_types = visa_types,
                    visa_requirements = visa_requirements,
                    visa_process = visa_process,
                    additional_info = additional_info,
                    faqs = faqs
                    # img = img
                )
                visa_obj.save()
                visa_obj.img.save(f"{country}.jpg", img, save=True)
                # break

