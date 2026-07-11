# Personal Portfolio — Flask + MySQL (Aiven) + Render

A full-stack personal portfolio site: Flask backend, MySQL database hosted on
Aiven, Bootstrap 5 frontend, SQLAlchemy ORM, deployed on Render, edited in
VS Code, versioned on GitHub, with MySQL Workbench for database access.

Pages: Home, About, Projects (list + detail), Contact (form saves to DB).

```
portfolio-app/
├── app/
│   ├── __init__.py          # app factory
│   ├── models.py            # Profile, Skill, Project, Experience, ContactMessage
│   ├── routes.py            # all page routes + contact form logic
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/script.js
│   └── templates/           # Jinja2 + Bootstrap templates
├── config.py                 # reads DB config from environment variables
├── run.py                    # local dev server
├── wsgi.py                   # production entry point (used by gunicorn)
├── seed.py                   # populates starter content
├── requirements.txt
├── .env.example
├── .gitignore
├── Procfile                  # tells Render how to start the app
└── render.yaml                # optional infra-as-code for Render
```

---

## 1. Open the project in VS Code

```bash
cd portfolio-app
code .
```

Recommended extensions: Python (Microsoft), Jinja, MySQL (optional, for
querying without leaving the editor).

Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 2. Create the MySQL database on Aiven

1. Sign in at [aiven.io](https://aiven.io) and create a new **MySQL**
   service (the free plan is fine to start).
2. Once it's running, open the service's **Overview** tab and note:
   - **Host**
   - **Port**
   - **User** (usually `avnadmin`)
   - **Password**
   - **Service URI** (a ready-made connection string)
3. Download the **CA Certificate** from the same Overview page. Save it as
   `ca.pem` in the project root (this file is already excluded from git via
   `.gitignore` — don't commit it).
4. Under **Allowed IP Addresses**, temporarily allow your current IP (or
   `0.0.0.0/0` while testing) so you can connect locally. Tighten this later.

---

## 3. Connect with MySQL Workbench

1. Open MySQL Workbench → **Database → Manage Connections → New**.
2. Fill in Hostname, Port, Username from the Aiven Overview tab.
3. Go to the **SSL** tab, set **Use SSL** to "Require", and point
   **SSL CA File** to the `ca.pem` you downloaded.
4. Test Connection → it should succeed. Use Workbench to inspect tables
   after the app creates them (step 5), or to edit content directly (e.g.
   updating your bio or adding a project row) without redeploying.

---

## 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your real Aiven values:

```
SECRET_KEY=some-long-random-string
DATABASE_URL=mysql+pymysql://avnadmin:yourpassword@your-host.aivencloud.com:12345/defaultdb
DB_USE_SSL=true
SSL_CA_PATH=ca.pem
```

`DATABASE_URL` is the simplest option — take Aiven's Service URI and just
change `mysql://` to `mysql+pymysql://` at the start.

---

## 5. Create tables and seed starter content

The app automatically creates tables on first run (via `db.create_all()`).
To also populate them with editable starter content:

```bash
python run.py &          # starts the app briefly to build tables, or just:
python -c "from app import create_app; create_app()"   # creates tables only
python seed.py            # inserts sample profile / skills / projects / experience
```

Open **MySQL Workbench** any time afterward to edit your name, bio, skills,
and projects directly in the `profile`, `skill`, `project`, and
`experience` tables — no redeploy needed.

---

## 6. Run locally

```bash
python run.py
```

Visit `http://localhost:5000`.

---

## 7. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: Flask portfolio app"
git branch -M main
git remote add origin https://github.com/yourusername/portfolio-app.git
git push -u origin main
```

`.env` and `ca.pem` are already git-ignored so your credentials never get
committed. Commit as you make changes:

```bash
git add .
git commit -m "Add project X"
git push
```

---

## 8. Deploy on Render

1. Go to [render.com](https://render.com) → **New → Web Service** → connect
   your GitHub repo.
2. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn wsgi:app`
3. Under **Environment**, add the same variables from your `.env`:
   - `SECRET_KEY`
   - `DATABASE_URL`
   - `DB_USE_SSL=true`
   - `SSL_CA_PATH=ca.pem`
4. Since `ca.pem` isn't committed to git, either:
   - **Option A (simplest):** paste the certificate contents into a Render
     **Secret File** at path `ca.pem` (Render dashboard → Environment →
     Secret Files), or
   - **Option B:** base64-encode the cert, store it in an env var, and
     write it to disk in `wsgi.py` on startup.
5. In Aiven, add Render's outbound IPs (or `0.0.0.0/0` if you're not
   worried about IP restriction) to **Allowed IP Addresses** so Render can
   reach the database.
6. Deploy. Render will build and give you a live URL
   (`https://your-app.onrender.com`).

`render.yaml` is included if you'd rather deploy via Render's Blueprint
(Infrastructure as Code) feature instead of the manual dashboard flow.

---

## Making it yours

- Edit `seed.py` with your real name, bio, skills, and projects, then
  re-run `python seed.py` (locally, pointed at your Aiven DB) — or just
  edit the rows directly in MySQL Workbench.
- Replace `image_url` / `avatar_url` values with links to real images
  (e.g. hosted on GitHub, Cloudinary, or Render's static files).
- Colors, fonts, and layout live in `app/static/css/style.css` if you want
  to adjust the look.

## Troubleshooting

- **`Can't connect to MySQL server` / timeout** — almost always an Aiven
  "Allowed IP Addresses" restriction, or the service is paused. Check the
  Aiven console first.
- **SSL errors** — make sure `ca.pem` exists at the path set in
  `SSL_CA_PATH` and that `DB_USE_SSL=true`.
- **`ModuleNotFoundError`** — make sure your virtual environment is
  activated and `pip install -r requirements.txt` completed successfully.
