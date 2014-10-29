# ref: celery and scrapy integrate
# http://stackoverflow.com/questions/11528739/running-scrapy-spiders-in-a-celery-task
find . -name "*.pyc" -exec rm -rf {} \;
find . -name "*.json" -exec rm -rf {} \;
find . -name "*.log" -exec rm -rf {} \;
find . -name "*.html" -exec rm -rf {} \;
rm -rf dist
rm -rf build
rm -rf *.egg-info
rm -rf tmp
rm -rf data
#pip install -r requirements.txt
#python setup.py install
#nosetests -vv --nocapture
#python bin/start.py --debug
#rm -rf tmp
#mkdir tmp
#mongod -dbpath ./tmp &
#export C_FORCE_ROOT=true
#celery -A bin.tasks worker -l info -P eventlet -c 1000 &
