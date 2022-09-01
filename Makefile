celery:
	celery -A performance_tracker worker -l INFO

random-revenue:
	python random_revenue.py

slow-iteration: 
	python slow_iteration.py
