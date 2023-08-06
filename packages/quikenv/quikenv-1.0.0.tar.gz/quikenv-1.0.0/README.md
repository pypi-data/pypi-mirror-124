# Quikenv

This was wrapper around the python dot-env project at

- https://github.com/theskumar/python-dotenv
- https://pypi.org/project/python-dotenv/

Here is the pypi release I made:
- https://pypi.org/project/quikenv/

I really liked the project but wanted something even more lazy. All credit goes to the original developers. I only added features I wanted on top of an already really great project.

This wrapper has the following features:

- A ezload() classmethod that automatically looks for for your .env file in the current working directory and 2 dirs up
```{python}
import quikenv

env = quikenv.ezload()
var = env.get("my_environment_var")
print(env.environment_variables)

```

- A proper_load() classmethod that will load this class with a given file path
```{python}
import quikenv

env_path = "C:/somedir/.env"
env = quikenv.proper_load(env_path)
var = env.get("my_environment_var")
print(env.environment_variables)
```

- A normal procedural start for the class
```{python}
import quikenv

env_path = "C:/somedir/.env"
env = quickenv.Quikenv(env_path)
env.load()
var = env.get("my_environment_var")
print(env.environment_variables)
```
- A lot of safety features (I don't think speed is relevant here):
    - Errors out when you give it an invalid file path to the .env file
    - Will NOT add values from your computer and will only use values from your .env file
    - Errors out when you try to get a value that doesn't exist or has am empty value
        - My years of programming has taught me that I'm still stupid enough to do this. You probably are too.
        - At least you get told now when something is null/empty instead of spending 2 hours debugging your idiocy.