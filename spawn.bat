set PYTHONPATH=.
python spawn.py %1
cd %1
python -m unittest discover -s test