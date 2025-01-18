from logs import log_error
from .. import db

# Generic utility functions for database operations
class Repository:
    @staticmethod
    def create_record(model, **kwargs):
        """
        Create a new record in the database.

        :param model: The SQLAlchemy model class
        :param kwargs: The fields and values for the new record
        :return: The created record
        """
        try:
            record = model(**kwargs) 
            db.session.add(record)
            db.session.commit()
            return record
        except Exception as e:
            db.session.rollback()
            log_error(f"Error creating record: {e}")
            raise

    @staticmethod
    def get_record_by_id(model, record_id):
        """Fetch a record by its ID."""
        return db.session.query(model).get(record_id)

    @staticmethod
    def get_record_by_field(model, field_name, field_value, options=None):
        """
        Fetch records by a specific field and value with optional pagination and additional filters.

        :param model: The SQLAlchemy model class
        :param field_name: The field to filter by
        :param field_value: The value to filter the field by
        :param options: Dictionary containing optional parameters like single, paginate, page, limit, start_date, end_date.
            Example:
            {
                "single": False,
                "paginate": True,
                "page": 1,
                "limit": 10,
                "start_date": "2023-01-01",
                "end_date": "2023-01-31"
            }
        :return: A list, a paginated result, or a single record depending on the `single` and `paginate` flags.
        """
        try:
            options = options or {}
            single = options.get('single', False)
            paginate = options.get('paginate', False)
            page = int(options.get('page', 1))
            limit = int(options.get('limit', 10))
            start_date = options.get('start_date')
            end_date = options.get('end_date')

            query = db.session.query(model).filter(getattr(model, field_name) == field_value)

            if start_date:
                query = query.filter(model.created_at >= start_date)
            if end_date:
                query = query.filter(model.created_at <= end_date)


            if paginate:
                return query.paginate(page=page, per_page=limit, error_out=False)

            if single:
                return query.first()
            return query.all()
        except Exception as e:
            log_error(f"Error querying {model.__name__}: {e}")
            return []

    @staticmethod
    def get_all_records(model):
        """Fetch all records for a model."""
        return db.session.query(model).all()

    @staticmethod
    def update_record(record, **kwargs):
        """
        Update fields in an existing record.

        :param record: The SQLAlchemy model instance to update
        :param kwargs: The fields and their new values
        :return: The updated record
        """
        try:
            for key, value in kwargs.items():
                if hasattr(record, key): 
                    setattr(record, key, value)  
            db.session.commit()  
            return record
        except Exception as e:
            db.session.rollback()
            log_error(f"Error updating record: {e}")
            raise


    @staticmethod
    def delete_record(record):
        """
        Delete a record from the database.

        :param record: The SQLAlchemy model instance to delete
        :return: True if the record was successfully deleted
        """
        try:
            db.session.delete(record)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            log_error(f"Error deleting record: {e}")
            raise

