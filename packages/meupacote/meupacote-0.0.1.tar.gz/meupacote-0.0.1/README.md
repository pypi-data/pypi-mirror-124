
## REQUIZITOS
pip install twine
pip install buildozer
pip install cython


## BUILD ( pip install wheel)
python setup.py sdist bdist_wheel

## UPLOAD
twine upload dist/*


sudo python setup.py install
