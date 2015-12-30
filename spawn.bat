@echo off
echo copying the source code to folder /%1
set PYTHONPATH=.
python spawn.py %1
pushd %1
echo running tests
python -m unittest discover -s test
pause
echo starting application at port %1
start python main/main.py %1
popd
pause
echo Creating NGINX configuration %1
python create_nginx_config.py %1
pause
echo Reloading NGINX configuration
pushd nginx-1.9.9\nginx-1.9.9
nginx -s reload
popd