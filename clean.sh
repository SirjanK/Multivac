find . -name "*.rdb" | xargs -r rm
find . -name "*.class" | xargs -r rm
find . -name "__pycache__" -not -path "./venv/*" | xargs -r rm -r
