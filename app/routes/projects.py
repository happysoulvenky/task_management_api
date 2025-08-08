from flask import Blueprint, request, jsonify, g
from app.models import Project, Task
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User

project_bp = Blueprint("projects", __name__, url_prefix="/projects")


def get_current_user():
    user_id = get_jwt_identity()
    return User.query.get(user_id)


@project_bp.route("/", methods=["POST"])
@jwt_required()
def create_project():
    data = request.get_json()
    user = get_current_user()

    project = Project(
        name=data.get("name"),
        description=data.get("description"),
        owner=user
    )
    db.session.add(project)
    db.session.commit()
    return jsonify({"id": project.id, "name": project.name}), 201


@project_bp.route("/", methods=["GET"])
@jwt_required()
def list_projects():
    user = get_current_user()
    projects = Project.query.filter_by(user_id=user.id).all()
    result = [{"id": p.id, "name": p.name, "description": p.description} for p in projects]
    return jsonify(result), 200


# fetch a project with its tasks
@project_bp.route("/<int:project_id>", methods=["GET"])
@jwt_required()
def get_project(project_id):
    user = get_current_user()
    project = Project.query.filter_by(id=project_id, user_id=user.id).first()
    if not project:
        return jsonify({"error": "Project not found"}), 404
    
    # Manually fetch tasks from Task table
    tasks = Task.query.filter_by(project_id=project.id).all()

    task_list = []
    for task in tasks:
        task_list.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "assigned_to_id": task.assigned_to_id
        })

    return jsonify({
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "tasks": task_list
    })


@project_bp.route("/<int:project_id>", methods=["PATCH"])
@jwt_required()
def update_project(project_id):
    user = get_current_user()
    project = Project.query.filter_by(id=project_id, user_id=user.id).first()
    if not project:
        return jsonify({"error": "Project not found"}), 404

    data = request.get_json()
    project.name = data.get("name", project.name)
    project.description = data.get("description", project.description)

    db.session.commit()
    return jsonify({"message": "Project updated"})


@project_bp.route("/<int:project_id>", methods=["DELETE"])
@jwt_required()
def delete_project(project_id):
    user = get_current_user()
    project = Project.query.filter_by(id=project_id, user_id=user.id).first()
    if not project:
        return jsonify({"error": "Project not found"}), 404

    db.session.delete(project)
    db.session.commit()
    return jsonify({"message": "Project deleted"})
