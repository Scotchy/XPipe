version=$1
sed -r -i "s/release[ ]?=[ ]?[\"'0-9\.]*/release = \"$version\"/" docs/source/conf.py
sed -r -i "s/version[ ]?=[ ]?[\"'0-9\.]*/version = \"$version\"/" setup.py
echo "Version set to $version"