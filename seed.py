"""
Populates the database with starter content so the site isn't empty on
first run. Safe to re-run: it clears existing rows in these tables first.

Usage:
    python seed.py

Edit the values below (or, once deployed, edit rows directly with MySQL
Workbench) to make the site your own.
"""
from app import create_app, db
from app.models import Profile, Skill, Project, Experience

app = create_app()

with app.app_context():
    # --- Reset tables (keeps ContactMessage / real inquiries intact) ---
    Project.query.delete()
    Skill.query.delete()
    Experience.query.delete()
    Profile.query.delete()
    db.session.commit()

    # --- Profile ---
    profile = Profile(
        full_name="Jane Doe",
        title="Full-Stack Developer",
        tagline="I design and build web applications end to end — from database to deploy.",
        bio=(
            "I'm a full-stack developer who enjoys turning ideas into working software. "
            "I work across the stack — Python and Flask on the backend, MySQL for data, "
            "and clean, responsive interfaces on the frontend. I care about writing code "
            "that's easy to read, easy to test, and easy to hand off. Outside of work I "
            "like exploring new frameworks, contributing to open source, and writing about "
            "what I learn along the way."
        ),
        email="jane.doe@example.com",
        phone="+91 90000 00000",
        location="Haryana, India",
        resume_url="",
        github_url="https://github.com/yourusername",
        linkedin_url="https://linkedin.com/in/yourusername",
        twitter_url="",
        avatar_url="",
    )
    db.session.add(profile)

    # --- Skills ---
    skills = [
        Skill(name="Python", category="Backend", proficiency=90, display_order=1),
        Skill(name="Flask", category="Backend", proficiency=88, display_order=2),
        Skill(name="SQLAlchemy", category="Backend", proficiency=82, display_order=3),
        Skill(name="MySQL", category="Database", proficiency=80, display_order=4),
        Skill(name="JavaScript", category="Frontend", proficiency=75, display_order=5),
        Skill(name="HTML / CSS", category="Frontend", proficiency=85, display_order=6),
        Skill(name="Bootstrap", category="Frontend", proficiency=85, display_order=7),
        Skill(name="Git / GitHub", category="Tools", proficiency=88, display_order=8),
    ]
    db.session.add_all(skills)

    # --- Projects ---
    projects = [
        Project(
            title="Careers Portal",
            slug="careers-portal",
            summary="A job-listing platform with employer dashboards and applicant tracking.",
            description=(
                "A full-stack web application that lets companies post job openings and "
                "candidates apply directly through the site. Built with Flask and MySQL, "
                "deployed on Render, with a responsive Bootstrap frontend."
            ),
            tech_stack="Flask, MySQL, SQLAlchemy, Bootstrap",
            image_url="",
            github_url="https://github.com/yourusername/careers-portal",
            live_url="",
            featured=True,
            display_order=1,
        ),
        Project(
            title="Personal Finance Tracker",
            slug="finance-tracker",
            summary="Track income, expenses, and savings goals with visual reports.",
            description=(
                "A budgeting tool that lets users log transactions, categorize spending, "
                "and view monthly summaries. Includes authentication and per-user data."
            ),
            tech_stack="Flask, MySQL, Chart.js, Bootstrap",
            image_url="",
            github_url="https://github.com/yourusername/finance-tracker",
            live_url="",
            featured=True,
            display_order=2,
        ),
        Project(
            title="Recipe Sharing App",
            slug="recipe-sharing-app",
            summary="A community app for sharing and rating recipes.",
            description=(
                "Users can post recipes with photos and ingredients, browse by category, "
                "and leave ratings. Built to practice relational data modeling in MySQL."
            ),
            tech_stack="Flask, MySQL, SQLAlchemy, Bootstrap",
            image_url="",
            github_url="https://github.com/yourusername/recipe-app",
            live_url="",
            featured=True,
            display_order=3,
        ),
    ]
    db.session.add_all(projects)

    # --- Experience ---
    experiences = [
        Experience(
            company="Freelance",
            role="Full-Stack Developer",
            location="Remote",
            start_date="2024",
            end_date="Present",
            description="Building and maintaining web applications for small business clients.",
            display_order=1,
        ),
        Experience(
            company="Jovian",
            role="Web Development Trainee",
            location="Remote",
            start_date="2023",
            end_date="2024",
            description="Completed hands-on projects covering Python, Flask, SQL, and deployment.",
            display_order=2,
        ),
    ]
    db.session.add_all(experiences)

    db.session.commit()
    print("Database seeded successfully.")
