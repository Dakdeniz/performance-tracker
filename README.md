# performance-tracker
### Django Excercise


### Installation: 
Poetry or pip can be used to install dependencies. pyproject.toml and requirements.txt files have same content

After installing dependencies, make migrations.

### Testing
Pytest is used for testing models.
Run:

    pytest

## Scripts
After activating virtualenv

#### Random Revenue:

    python random_revenue.py

#### Slow Iteration
Start celery worker first:

    celery -A performance_tracker worker -l INFO

Then run the script in another terminal

    python slow_iteration.py

