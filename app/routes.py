import re
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app import db
from app.models import Profile, Skill, Project, Experience, ContactMessage

main_bp = Blueprint("main", __name__)

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@main_bp.app_context_processor
def inject_globals():
    """Makes `profile` and `current_year` available in every template."""
    profile = Profile.query.first()
    return {"profile": profile, "current_year": datetime.utcnow().year}


@main_bp.route("/")
def home():
    profile = Profile.query.first()
    featured_projects = (
        Project.query.filter_by(featured=True)
        .order_by(Project.display_order.asc())
        .limit(3)
        .all()
    )
    skills = Skill.query.order_by(Skill.display_order.asc()).all()
    return render_template(
        "index.html",
        profile=profile,
        projects=featured_projects,
        skills=skills,
    )


@main_bp.route("/about")
def about():
    profile = Profile.query.first()
    skills = Skill.query.order_by(Skill.display_order.asc()).all()
    experiences = Experience.query.order_by(Experience.display_order.asc()).all()
    return render_template(
        "about.html",
        profile=profile,
        skills=skills,
        experiences=experiences,
    )


@main_bp.route("/projects")
def projects():
    all_projects = Project.query.order_by(Project.display_order.asc()).all()
    return render_template("projects.html", projects=all_projects)


@main_bp.route("/projects/<slug>")
def project_detail(slug):
    project = Project.query.filter_by(slug=slug).first()
    if project is None:
        abort(404)
    return render_template("project_detail.html", project=project)


@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()

        errors = []
        if not name:
            errors.append("Please enter your name.")
        if not email or not EMAIL_RE.match(email):
            errors.append("Please enter a valid email address.")
        if not message:
            errors.append("Please enter a message.")

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template(
                "contact.html",
                form_data={"name": name, "email": email, "subject": subject, "message": message},
            )

        entry = ContactMessage(name=name, email=email, subject=subject, message=message)
        db.session.add(entry)
        db.session.commit()

        flash("Thanks for reaching out! I'll get back to you soon.", "success")
        return redirect(url_for("main.contact"))

    return render_template("contact.html", form_data={})


@main_bp.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404
