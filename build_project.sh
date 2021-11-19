project_dir=$(dirname $(realpath -s $0))

cd $project_dir/xpipe/server/frontend
echo "Installing js libraries"
npm i
echo "Building react app"
npm run build

# Build python package
cd $project_dir
echo "Building python package"
python -m build

echo "Checking long description syntax for Pypi"
twine check dist/*