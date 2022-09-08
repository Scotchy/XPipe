# Build python package
echo "Building python package"
python setup.py sdist bdist_wheel

echo "Checking long description syntax for Pypi"
twine check dist/*