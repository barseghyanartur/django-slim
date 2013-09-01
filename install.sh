python setup.py install
python example/example/manage.py collectstatic --noinput
python example/example/manage.py syncdb --noinput
#python example/example/manage.py migrate --noinput