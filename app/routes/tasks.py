from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Task, User, Project
from app.extensions import db
from datetime import datetime
from app.utils.email_utils import send_task_created_email
from app.utils.email_utils import _send_async_email ,send_status_update_email, send_assignment_email, send_priority_change_email
from flask_mail import Message
from flask import current_app


task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def get_user_from_jwt():
    """Helper to get the current authenticated user."""
    return User.query.get(get_jwt_identity())

@task_bp.route("/", methods=["POST"])
@jwt_required()
def create_task():
    data = request.json
    user = get_user_from_jwt()

    # Input validation
    title = data.get("title")
    project_id = data.get("project_id")
    assigned_to_id = data.get("assigned_to_id")
    due_date_str = data.get("due_date")

    if not title or not project_id:
        return jsonify({"error": "Title and project_id are required"}), 400

    # Ensure user owns the project
    project = Project.query.filter_by(id=project_id, user_id=user.id).first()
    if not project:
        return jsonify({"error": "Invalid or unauthorized project"}), 403

    due_date = None
    if due_date_str:
        try:
            due_date = datetime.fromisoformat(due_date_str)
        except ValueError:
            return jsonify({"error": "Invalid due_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS or YYYY-MM-DD)."}), 400

    assigned_user = None
    if assigned_to_id:
        assigned_user = User.query.get(assigned_to_id)
        if not assigned_user:
            return jsonify({"error": "Assigned user not found"}), 404

    task = Task(
        title=title,
        description=data.get("description"),
        status=data.get("status", "pending"),
        priority=data.get("priority", 3),
        due_date=due_date,
        project=project,
        assigned_to_id=assigned_to_id
    )
    db.session.add(task)
    db.session.commit()

    # Send email notification
    if assigned_user and assigned_user.email:
        send_task_created_email(task.title, assigned_user.email)
    

    return jsonify({"id": task.id, "title": task.title, "message": "Task created successfully"}), 201


# get tasks list with filters and sorting
@task_bp.route("/", methods=["GET"])
@jwt_required()
def list_tasks():
    user = get_user_from_jwt()
    query = Task.query.join(Project).filter(Project.user_id == user.id)

    # Filters
    if status := request.args.get("status"):
        query = query.filter(Task.status == status)
    if priority := request.args.get("priority"):
        try:
            query = query.filter(Task.priority == int(priority))
        except ValueError:
            return jsonify({"error": "Invalid priority. Must be an integer."}), 400
    if due_date_str := request.args.get("due_date"):
        try:
            # Parse date only for comparison, assuming due_date in DB is datetime object
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            query = query.filter(Task.due_date == due_date) # Comparing date parts
        except ValueError:
            return jsonify({"error": "Invalid due_date format. Use YYYY-MM-DD"}), 400
    if pid := request.args.get("project_id"):
        try:
            query = query.filter(Task.project_id == int(pid))
        except ValueError:
            return jsonify({"error": "Invalid project_id. Must be an integer."}), 400

    # Sorting
    sort_by = request.args.get("sort_by", "created_at") # Default sort
    order = request.args.get("order", "asc")

    if sort_by == 'priority':
        query = query.order_by(Task.priority.asc() if order == 'asc' else Task.priority.desc())
    elif sort_by == 'due_date':
        # Handle nulls for due_date sorting: nulls last for asc, nulls first for desc
        if order == 'asc':
            query = query.order_by(db.case((Task.due_date.isnot(None), 0), else_=1), Task.due_date.asc())
        else: # desc
            query = query.order_by(db.case((Task.due_date.isnot(None), 0), else_=1), Task.due_date.desc())
    else: # Default to created_at
        query = query.order_by(Task.created_at.asc() if order == 'asc' else Task.created_at.desc())

    # Pagination
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("limit", 10))
    paginated_tasks = query.paginate(page=page, per_page=per_page, error_out=False)

    result = [
        {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "status": t.status,
            "priority": t.priority,
            "due_date": t.due_date.isoformat() if t.due_date else None,
            "created_at": t.created_at.isoformat(),
            "project_id": t.project_id,
            "assigned_to_id": t.assigned_to_id
        }
        for t in paginated_tasks.items
    ]
    return jsonify({
        "tasks": result,
        "total": paginated_tasks.total,
        "pages": paginated_tasks.pages,
        "current_page": paginated_tasks.page
    })


@task_bp.route("/<int:task_id>", methods=["GET"])
@jwt_required()
def get_task(task_id):
    user = get_user_from_jwt()
    task = Task.query.join(Project).filter(Task.id == task_id, Project.user_id == user.id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "created_at": task.created_at.isoformat(),
        "project_id": task.project_id,
        "assigned_to_id": task.assigned_to_id
    })


@task_bp.route("/<int:task_id>", methods=["PATCH"])
@jwt_required()
def update_task(task_id):
    user = get_user_from_jwt()
    task = Task.query.join(Project).filter(Task.id == task_id, Project.user_id == user.id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.json

    # Store old values for comparison
    old_status = task.status
    old_assigned_to_id = task.assigned_to_id

    # Update fields
    if "title" in data:
        task.title = data["title"]
    if "description" in data:
        task.description = data["description"]
    if "status" in data:
        task.status = data["status"]
    if "priority" in data:
        try:
            task.priority = int(data["priority"])
        except ValueError:
            return jsonify({"error": "Priority must be an integer."}), 400
    if "due_date" in data:
        if data["due_date"] is None:
            task.due_date = None
        else:
            try:
                task.due_date = datetime.fromisoformat(data["due_date"])
            except ValueError:
                return jsonify({"error": "Invalid due_date format. Use ISO format."}), 400
    if "assigned_to_id" in data:
        new_assigned_to_id = data["assigned_to_id"]
        if new_assigned_to_id is None:
            task.assigned_to_id = None
        else:
            assigned_user_candidate = User.query.get(new_assigned_to_id)
            if not assigned_user_candidate:
                return jsonify({"error": "Assigned user not found."}), 404
            task.assigned_to_id = new_assigned_to_id

    db.session.commit()

    # --- Email Notification Logic --- 
    # # your async email sender
    if old_status != task.status:
        send_status_update_email(task.title, old_status, task.status, user.email)

    if task.assigned_to_id is not None:
        assigned_user = User.query.get(task.assigned_to_id)
        if assigned_user and assigned_user.email:
            send_assignment_email(task.title, assigned_user.email)   

    if "priority" in data:
        send_priority_change_email(task.title, task.priority, user.email)         

# # Send if assigned_to_id changed
#     if task.assigned_to_id != old_assigned_to_id and task.assigned_to_id is not None:
#         assigned_user = User.query.get(task.assigned_to_id)
#     if assigned_user:
#         msg = Message(
#             subject=f"You have been assigned to task '{task.title}'",
#             recipients=[assigned_user.email],
#             body=f"You have been assigned to the task '{task.title}'. Please check your task list.",
#             sender=current_app.config['MAIL_DEFAULT_SENDER']
#         )
#         _send_async_email(current_app._get_current_object(), msg)

    return jsonify({"message": "Task updated", "id": task.id, "title": task.title}), 200



@task_bp.route("/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    user = get_user_from_jwt()
    task = Task.query.join(Project).filter(Task.id == task_id, Project.user_id == user.id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 204