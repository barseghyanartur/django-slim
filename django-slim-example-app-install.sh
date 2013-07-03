wget -O django_slim_example_app.tar.gz http://bitbucket.org/barseghyanartur/django-slim/get/stable.tar.gz
mkdir django_slim_example_app/
tar -xvf django_slim_example_app.tar.gz -C django_slim_example_app
cd django_slim_example_app/barseghyanartur-django-slim-1168426d0577/example/example/
pip install Django
pip install -r ../requirements.txt
mkdir ../media/
mkdir ../media/static/
mkdir ../static/
mkdir ../db/
cp local_settings.example local_settings.py
./manage.py syncdb --noinput
./manage.py collectstatic --noinput
./manage.py runserver
