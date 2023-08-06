# Example Package

This is a simple example package. You can use
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.



```
python3 -m build
python3 -m twine upload  dist/* --verbose
```



On the folder where pyproject.toml is located run the following commands

```
python3 -m venv publishing_environment
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade build
python3 -m build
python3 -m pip install --upgrade twine
python -m twine upload dist/* --verbose 
```