import os
from modal import Image, Stub, wsgi_app

image = (
    Image.debian_slim(python_version="3.11")
        .pip_install_from_requirements("requirements.txt")
        .copy_local_dir('static', '/static')
        .copy_local_dir('media', '/media')
        .copy_local_dir('templates', '/templates')
        .copy_local_dir('traveler', '/traveler')
        .copy_local_dir('main', '/main')
        .copy_local_dir('traveler', '/traveler')
        # .copy_local_dir('bm25_traveler_website.json', 'bm25_traveler_website.json')
        # .copy_local_file('db.splite3', 'db.splite3')
        .copy_local_file('manage.py', 'manage.py')
)

stub = Stub(name="WEBRAG", image=image)

@stub.function(
        gpu="T4",
        concurrency_limit=1,
        container_idle_timeout=300,
    )
@wsgi_app()
def run():
    from traveler.wsgi import application
    return application