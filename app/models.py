from datetime import datetime
from app import db


class Profile(db.Model):
    """Singleton-style table holding the site owner's info."""
    __tablename__ = "profile"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(160), nullable=False)
    tagline = db.Column(db.String(255))
    bio = db.Column(db.Text)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(40))
    location = db.Column(db.String(120))
    resume_url = db.Column(db.String(255))
    github_url = db.Column(db.String(255))
    linkedin_url = db.Column(db.String(255))
    twitter_url = db.Column(db.String(255))
    avatar_url = db.Column(db.String(255))

    def __repr__(self):
        return f"<Profile {self.full_name}>"


class Skill(db.Model):
    __tablename__ = "skill"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(80), default="General")
    proficiency = db.Column(db.Integer, default=80)  # 0-100, used for a progress bar
    display_order = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Skill {self.name}>"


class Project(db.Model):
    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    slug = db.Column(db.String(180), unique=True, nullable=False)
    summary = db.Column(db.String(300))
    description = db.Column(db.Text)
    tech_stack = db.Column(db.String(255))  # comma-separated, e.g. "Flask, MySQL, Bootstrap"
    image_url = db.Column(db.String(255))
    github_url = db.Column(db.String(255))
    live_url = db.Column(db.String(255))
    featured = db.Column(db.Boolean, default=False)
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def tech_list(self):
        if not self.tech_stack:
            return []
        return [t.strip() for t in self.tech_stack.split(",") if t.strip()]

    def __repr__(self):
        return f"<Project {self.title}>"


class Experience(db.Model):
    __tablename__ = "experience"

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(160), nullable=False)
    role = db.Column(db.String(160), nullable=False)
    location = db.Column(db.String(120))
    start_date = db.Column(db.String(40))  # kept as text for simplicity, e.g. "Jan 2024"
    end_date = db.Column(db.String(40))    # "Present" allowed
    description = db.Column(db.Text)
    display_order = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Experience {self.role} @ {self.company}>"


class ContactMessage(db.Model):
    __tablename__ = "contact_message"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<ContactMessage from {self.name}>"
