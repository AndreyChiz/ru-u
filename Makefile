.PHONY: create_tables
.PHONY: purge_tables

create_tables:
	alembic revision --autogenerate -m "Added tables"
	alembic upgrade head
purge_tables:
	alembic downgrade -1  
	rm -r alembic/versions/*.*


