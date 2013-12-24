wget -O django_slim_example_app_installer.tar.gz https://github.com/barseghyanartur/django-slim/archive/stable.tar.gz
virtualenv slim
source slim/bin/activate
mkdir django_slim_example_app_installer/
tar -xvf django_slim_example_app_installer.tar.gz -C django_slim_example_app_installer
cd django_slim_example_app_installer/django-slim-stable/example/example/
pip install Django==1.5.5
pip install -r ../example/requirements.txt
pip install -e git+https://github.com/barseghyanartur/django-slim@stable#egg=django-slim
mkdir -p ../media/ ../media/static/ ../static/ ../db/ ../logs/ ../tmp/
cp local_settings.example local_settings.py
./manage.py syncdb --noinput --traceback -v 3
./manage.py migrate --noinput
./manage.py collectstatic --noinput --traceback -v 3
./manage.py foo_create_test_data --traceback -v 3
./manage.py runserver 0.0.0.0:8001 --traceback -v 3