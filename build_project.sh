# Build python package
echo "Building python package"
python -m build

echo "Checking long description syntax for Pypi"
twine check dist/*