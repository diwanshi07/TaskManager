import logging
from flask_restx import Namespace, Resource
from flask import request
from app.models import Task
from app.repository import Repository
from app.utils import create_response, jwt_required
from logs import log, log_error  

tasks_namespace = Namespace('tasks', description='Task management')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_task_owner(task, current_user_id):
    """
    Helper function to check if the logged-in user is the owner of the task.

    :param task: The task object to check ownership
    :param current_user_id: The ID of the logged-in user
    :return: True if the user is the owner, False otherwise
    """
    return str(task.user_id) == str(current_user_id)

@tasks_namespace.route('/')
class TaskList(Resource):
    @jwt_required
    def get(self):
        """
        Fetch all tasks for the logged-in user with optional pagination and filters.

        :return: JSON response containing the tasks of the logged-in user.
        """
        try:
            log("Entering the get function in TaskList")
            
            page = request.args.get('page', 1, type=int)
            limit = request.args.get('limit', 10, type=int)
            start_date = request.args.get('start_date')  # Format: YYYY-MM-DD
            end_date = request.args.get('end_date')  # Format: YYYY-MM-DD
            paginate = True if request.args.get('page') else False

            current_user_id = request.user_id

            options = {
                "paginate": paginate,
                "page": page,
                "limit": limit,
                "start_date": start_date,
                "end_date": end_date,
                "single": False
            }

            log(f"Options for task fetch - Page: {page}, Limit: {limit}, Start Date: {start_date}, End Date: {end_date}")

            user_tasks_query = Repository.get_record_by_field(Task, field_name='user_id', field_value=current_user_id, options=options)
            tasks_list = [task.to_dict() for task in user_tasks_query.items] if paginate else [task.to_dict() for task in user_tasks_query]

            total_count = user_tasks_query.total if paginate else len(tasks_list)

            return create_response(
                data=tasks_list,
                message="Tasks fetched successfully",
                success=True,
                total_count=total_count,
                page=page if paginate else None,
                limit=limit if paginate else None
            )
        except Exception as e:
            log_error(f"Error fetching tasks: {e}")
            return create_response(message="An error occurred while fetching tasks", success=False, error=str(e))

    @jwt_required
    def post(self):
        """
        Add a new task for the logged-in user.

        :return: JSON response indicating the success or failure of the task creation.
        """
        try:
            log("Entering the post function in TaskList")

            current_user_id = request.user_id
            data = request.json
            title = data.get('title')
            description = data.get('description')

            log(f"Received data for task - Title: {title}, Description: {description}")

            if not title or not description:
                log("Validation failed: Title and description are required")
                return create_response(message="Title and description are required", success=False)

            created_task = Repository.create_record(Task, title=title, description=description, user_id=current_user_id)
            log(f"Created task with ID: {created_task.id}")

            return create_response(data=created_task.to_dict(), message="Task created successfully", success=True)
        except Exception as e:
            log_error(f"Error creating task: {e}")
            return create_response(message="An error occurred while creating the task", success=False, error=str(e))


@tasks_namespace.route('/<int:task_id>')
class TaskId(Resource):
    @jwt_required
    def get(self, task_id):
        """
        Fetch a specific task for the logged-in user.

        :param task_id: The ID of the task to fetch
        :return: JSON response with task details or an error message.
        """
        try:
            log("Entering the get function in TaskId")

            current_user_id = request.user_id
            task = Repository.get_record_by_id(Task, task_id)
            if not task:
                log(f"Task with ID {task_id} not found")
                return create_response(message="Task not found", success=False)

            if not check_task_owner(task, current_user_id):
                log(f"Unauthorized access attempt to task with ID {task_id}")
                return create_response(message="Unauthorized access to task", success=False)

            return create_response(data=task.to_dict(), message="Task fetched successfully", success=True)
        except Exception as e:
            log_error(f"Error fetching task with id {task_id}: {e}")
            return create_response(message="An error occurred while fetching the task", success=False, error=str(e))

    @jwt_required
    def put(self, task_id):
        """
        Update a specific task for the logged-in user.

        :param task_id: The ID of the task to update
        :return: JSON response indicating the success or failure of the task update.
        """
        try:
            log("Entering the put function in TaskId")

            current_user_id = request.user_id
            task = Repository.get_record_by_id(Task, task_id)
            if not task:
                log(f"Task with ID {task_id} not found")
                return create_response(message="Task not found", success=False)

            if not check_task_owner(task, current_user_id):
                log(f"Unauthorized access attempt to task with ID {task_id}")
                return create_response(message="Unauthorized access to task", success=False)

            data = request.json
            updated_task = Repository.update_record(task, **data)

            log(f"Task with ID {task_id} updated successfully")

            return create_response(data=updated_task.to_dict(), message="Task updated successfully", success=True)
        except Exception as e:
            log_error(f"Error updating task with id {task_id}: {e}")
            return create_response(message="An error occurred while updating the task", success=False, error=str(e))

    @jwt_required
    def delete(self, task_id):
        """
        Delete a specific task for the logged-in user.

        :param task_id: The ID of the task to delete
        :return: JSON response indicating the success or failure of the task deletion.
        """
        try:
            log("Entering the delete function in TaskId")

            current_user_id = request.user_id
            task = Repository.get_record_by_id(Task, task_id)
            if not task:
                log(f"Task with ID {task_id} not found")
                return create_response(message="Task not found", success=False)

            if not check_task_owner(task, current_user_id):
                log(f"Unauthorized access attempt to task with ID {task_id}")
                return create_response(message="Unauthorized access to task", success=False)

            Repository.delete_record(task)
            log(f"Task with ID {task_id} deleted successfully")

            return create_response(message="Task deleted successfully", success=True)
        except Exception as e:
            log_error(f"Error deleting task with id {task_id}: {e}")
            return create_response(message="An error occurred while deleting the task", success=False, error=str(e))


@tasks_namespace.route('/delete_all')
class TaskDeleteAll(Resource):
    @jwt_required
    def delete(self):
        """
        Delete all tasks for the logged-in user.

        :return: JSON response indicating the success or failure of deleting all tasks.
        """
        try:
            log("Entering the delete_all function in TaskDeleteAll")

            current_user_id = request.user_id
            user_tasks = Repository.get_record_by_field(Task, 'user_id', current_user_id, options={"single": False})
            if not user_tasks:
                log(f"No tasks found to delete for user {current_user_id}")
                return create_response(message="No tasks found to delete", success=False)

            for task in user_tasks:
                Repository.delete_record(task)
                log(f"Task with ID {task.id} deleted")

            return create_response(message="All tasks deleted successfully", success=True)
        except Exception as e:
            log_error(f"Error deleting all tasks for user {current_user_id}: {e}")
            return create_response(message="An error occurred while deleting tasks", success=False, error=str(e))
