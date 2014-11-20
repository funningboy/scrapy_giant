# ref: celery and scrapy integrate
# http://stackoverflow.com/questions/11528739/running-scrapy-spiders-in-a-celery-task
find . -name '*.pyc' -exec rm -rf {} \;
find . -name '*.json' -exec rm -rf {} \;
find . -name '*.log' -exec rm -rf {} \;
find . -name '*.html' -exec rm -rf {} \;
find . -type d -name '.ropeproject' -exec rm -rf {} \;
#rm -rf .env
rm -rf dist
rm -rf build
rm -rf *.egg-info
#mkdir tmp
#rm -rf data
#virtualenv .env
#source .env/bin/activate
#export PATH=".env/bin" 
#export LD_LIBRARY_PATH=".env/lib"
#pip install -r requirements.txt
#pip uninstall lxml
#STATIC_DEPS=true pip install -U lxml
#python setup.py install
##nosetests -vv --nocapture
##python bin/start.py --debug
##rm -rf tmp
##mkdir tmp
##mongod -dbpath ./tmp &
##export C_FORCE_ROOT=true
##celery -A bin.tasks worker -l info -P eventlet -c 1000 &
##deactivate
#sudo port install openssl
#env ARCHFLAGS="-arch x86_64" LDFLAGS="-L/opt/local/lib" CFLAGS="-I/opt/local/include" pip install cryptography
