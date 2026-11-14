#!/usr/bin/env bash
# Builds the package (egg for Deluge, sdist/wheel for PyPI) and publishes it to PyPI.
#
# Usage: ./pub.sh
#
# Requirements: python3 with setuptools, uv, and PyPI credentials for uv publish
# (UV_PUBLISH_TOKEN or ~/.pypirc).

set -euo pipefail
cd "$(dirname "$0")"

rm -rf build/ deluge_webapi.egg-info/
rm -f dist/*.tar.gz dist/*.whl

echo ">>> Building the egg ..."
python3 -c "from setuptools import setup; setup()" bdist_egg -q

echo ">>> Building sdist and wheel ..."
uv build --quiet

echo ">>> Publishing to PyPI ..."
uv publish dist/*.tar.gz dist/*.whl

echo ">>> Done. Do not forget to commit the new egg from dist/."
