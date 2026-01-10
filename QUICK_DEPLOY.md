# DiplomatFlow - Quick Deployment Reference

## Railway (EASIEST - RECOMMENDED)

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR-USERNAME/DiplomatFlow.git
git push -u origin main
```

### 2. Deploy on Railway
- Go to https://railway.app
- Sign in with GitHub
- Click "New Project" → "Deploy from GitHub"
- Select DiplomatFlow repository
- Add PostgreSQL database (+ New → Database → PostgreSQL)

### 3. Set Environment Variables
```
SECRET_KEY = (generate one using command below)
DEBUG = False
ALLOWED_HOSTS = .railway.app
```

### 4. Generate Secret Key
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Railway will auto-deploy
- Wait 2-5 minutes
- Generate domain in Settings → Networking
- Access at: https://your-app.railway.app

---

## Heroku

### Commands
```bash
# Login
heroku login

# Create app
heroku create diplomatflow

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set SECRET_KEY="your-key"
heroku config:set DEBUG=False

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create admin user
heroku run python manage.py createsuperuser

# Open app
heroku open

# View logs
heroku logs --tail
```

---

## Local Testing

### Setup
```bash
cd DiplomatFlow-main
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Access at: http://127.0.0.1:8000

---

## Common Commands

### Database
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Static Files
```bash
python manage.py collectstatic --noinput
```

### Testing
```bash
python manage.py test
python manage.py check
```

---

## Troubleshooting

### DisallowedHost Error
Add your domain to ALLOWED_HOSTS environment variable

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### Database Issues
Check DATABASE_URL is set correctly

### View Logs
**Railway:** Click on service → View logs
**Heroku:** `heroku logs --tail`

---

## Update Deployed App

### Railway
```bash
git add .
git commit -m "Update"
git push origin main
# Auto-deploys
```

### Heroku
```bash
git add .
git commit -m "Update"
git push heroku main
heroku run python manage.py migrate  # if needed
```

---

## Important URLs

- Railway: https://railway.app
- Heroku: https://dashboard.heroku.com
- Django Admin: /admin/
- Task Dashboard: /tasks/dashboard/

---

## Environment Variables Needed

```
SECRET_KEY = (generate unique key)
DEBUG = False
ALLOWED_HOSTS = your-domain.com
DATABASE_URL = (auto-provided by Railway/Heroku)
```

---

## Default Login

After creating superuser, access:
- Admin panel: https://your-app.com/admin/
- Task dashboard: https://your-app.com/tasks/dashboard/

---

**Need help?** Check DEPLOYMENT_GUIDE.md for detailed instructions.
