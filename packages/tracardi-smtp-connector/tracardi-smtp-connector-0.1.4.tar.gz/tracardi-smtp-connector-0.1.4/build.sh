python setup.py sdist bdist_wheel
python -m twine upload dist/*


rm -rf build
rm -rf dist
rm -rf tracardi_smtp_connector.egg-info
