# DiplomatFlow Deployment Guide

## Prerequisites
- Git installed on your computer
- GitHub account
- Basic command line knowledge

---

## OPTION 1: Railway.app Deployment (RECOMMENDED - Free & Easy)

### Step 1: Push Code to GitHub

1. **Create a new repository on GitHub**
   - Go to https://github.com/new
   - Name it: `DiplomatFlow`
   - Make it public or private
   - Don't initialize with README (we already have one)
   - Click "Create repository"

2. **Push your code to GitHub**
   ```bash
   cd DiplomatFlow-main
   git init
   git add .
   git commit -m "Initial commit - DiplomatFlow application"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/DiplomatFlow.git
   git push -u origin main
   ```

### Step 2: Sign Up for Railway

1. Go to https://railway.app
2. Click "Login" or "Start a New Project"
3. Sign in with your GitHub account
4. Authorize Railway to access your repositories

### Step 3: Deploy from GitHub

1. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `DiplomatFlow` repository
   - Railway will automatically detect it's a Django app

2. **Add PostgreSQL Database**
   - In your project dashboard, click "+ New"
   - Select "Database" → "PostgreSQL"
   - Railway will automatically create and link the database
   - The DATABASE_URL will be automatically set

3. **Configure Environment Variables**
   - Click on your Django service
   - Go to "Variables" tab
   - Add these variables:
   
   ```
   SECRET_KEY = your-secret-key-here-make-it-long-and-random
   DEBUG = False
   ALLOWED_HOSTS = .railway.app
   DJANGO_SETTINGS_MODULE = mofa_task_tracker.settings
   ```

   To generate a secure SECRET_KEY, use:
   ```python
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

4. **Deploy**
   - Railway will automatically build and deploy
   - Wait for the build to complete (2-5 minutes)
   - You'll see a green checkmark when done

### Step 4: Run Database Migrations

1. In your Railway project, click on your Django service
2. Click "Settings" → "Deployments"
3. Find the latest deployment and click the three dots → "View Logs"
4. Or go to "Settings" → "Service" and enable "Run Command"
5. Run these commands in Railway's terminal:

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

### Step 5: Access Your Application

1. Go to "Settings" → "Networking"
2. Click "Generate Domain"
3. Your app will be available at: `https://your-app-name.railway.app`
4. Visit the URL and log in with your superuser credentials

### Step 6: Update ALLOWED_HOSTS (if needed)

If you get a "DisallowedHost" error:
1. Go to Variables
2. Update ALLOWED_HOSTS to include your Railway domain:
   ```
   ALLOWED_HOSTS = .railway.app,your-app-name.railway.app
   ```

---

## OPTION 2: Heroku Deployment

### Step 1: Install Heroku CLI

**Windows:**
Download from: https://devcenter.heroku.com/articles/heroku-cli

**Mac:**
```bash
brew tap heroku/brew && brew install heroku
```

**Linux:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

### Step 2: Prepare Your Code

1. **Navigate to project directory**
   ```bash
   cd DiplomatFlow-main
   ```

2. **Initialize Git (if not already done)**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

### Step 3: Create Heroku App

1. **Login to Heroku**
   ```bash
   heroku login
   ```
   This will open your browser for authentication

2. **Create a new Heroku app**
   ```bash
   heroku create diplomatflow
   ```
   Replace `diplomatflow` with your preferred name (must be unique)

3. **Add PostgreSQL database**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

### Step 4: Configure Environment Variables

```bash
# Generate a secret key (or use your own)
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Set environment variables
heroku config:set SECRET_KEY="your-generated-secret-key-here"
heroku config:set DEBUG=False
heroku config:set DJANGO_SETTINGS_MODULE=mofa_task_tracker.settings
```

### Step 5: Deploy to Heroku

1. **Deploy your code**
   ```bash
   git push heroku main
   ```

2. **Run migrations**
   ```bash
   heroku run python manage.py migrate
   ```

3. **Create superuser**
   ```bash
   heroku run python manage.py createsuperuser
   ```

4. **Collect static files**
   ```bash
   heroku run python manage.py collectstatic --noinput
   ```

### Step 6: Open Your Application

```bash
heroku open
```

Or visit: `https://your-app-name.herokuapp.com`

### Step 7: View Logs (if there are issues)

```bash
heroku logs --tail
```

---

## OPTION 3: DigitalOcean/VPS Deployment (Advanced)

### Requirements
- A DigitalOcean droplet or VPS (Ubuntu 22.04)
- SSH access to your server
- Domain name (optional)

### Quick Steps:

1. **SSH into your server**
   ```bash
   ssh root@your-server-ip
   ```

2. **Update system**
   ```bash
   apt update && apt upgrade -y
   ```

3. **Install dependencies**
   ```bash
   apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl -y
   ```

4. **Create PostgreSQL database**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE diplomatflow;
   CREATE USER diplomatflow_user WITH PASSWORD 'your_password';
   ALTER ROLE diplomatflow_user SET client_encoding TO 'utf8';
   ALTER ROLE diplomatflow_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE diplomatflow_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE diplomatflow TO diplomatflow_user;
   \q
   ```

5. **Clone your repository**
   ```bash
   cd /var/www
   git clone https://github.com/YOUR-USERNAME/DiplomatFlow.git
   cd DiplomatFlow
   ```

6. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

7. **Configure environment variables**
   Create a `.env` file:
   ```bash
   nano .env
   ```
   
   Add:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=False
   DATABASE_URL=postgresql://diplomatflow_user:your_password@localhost/diplomatflow
   ALLOWED_HOSTS=your-domain.com,your-server-ip
   ```

8. **Run migrations**
   ```bash
   python manage.py migrate
   python manage.py collectstatic
   python manage.py createsuperuser
   ```

9. **Configure Gunicorn**
   ```bash
   gunicorn --bind 0.0.0.0:8000 mofa_task_tracker.wsgi:application
   ```

10. **Setup Nginx and Systemd** (detailed configuration needed)

---

## Post-Deployment Checklist

✅ **Security**
- [ ] DEBUG is set to False
- [ ] SECRET_KEY is unique and secure
- [ ] ALLOWED_HOSTS is properly configured
- [ ] SSL/HTTPS is enabled
- [ ] Database credentials are secure

✅ **Functionality**
- [ ] Can access the homepage
- [ ] Can log in with superuser
- [ ] Static files are loading (CSS/JS)
- [ ] Can create tasks
- [ ] Can manage equipment
- [ ] Database is working

✅ **Performance**
- [ ] Static files are being served correctly
- [ ] Database queries are optimized
- [ ] No 500 errors in logs

---

## Troubleshooting Common Issues

### Issue: "DisallowedHost at /"
**Solution:** Add your domain to ALLOWED_HOSTS in environment variables

### Issue: Static files not loading
**Solution:** 
```bash
python manage.py collectstatic --noinput
```
Ensure STATIC_ROOT and STATICFILES_DIRS are configured

### Issue: Database connection error
**Solution:** Check DATABASE_URL is set correctly

### Issue: 500 Internal Server Error
**Solution:** 
- Set DEBUG=True temporarily to see the error
- Check logs: `heroku logs --tail` (Heroku) or Railway logs
- Ensure all migrations are run

### Issue: "No module named 'psycopg2'"
**Solution:** Make sure requirements.txt includes psycopg2-binary

---

## Updating Your Deployment

### Railway
- Just push to GitHub, Railway auto-deploys:
  ```bash
  git add .
  git commit -m "Update message"
  git push origin main
  ```

### Heroku
```bash
git add .
git commit -m "Update message"
git push heroku main
heroku run python manage.py migrate  # if models changed
```

---

## Custom Domain Setup

### Railway
1. Go to your service Settings
2. Click "Networking" → "Custom Domain"
3. Add your domain
4. Update DNS records as instructed

### Heroku
```bash
heroku domains:add www.yourdomain.com
heroku domains:add yourdomain.com
```
Then update your DNS records

---

## Monitoring & Maintenance

- Check logs regularly for errors
- Monitor database usage
- Backup database periodically
- Keep dependencies updated
- Monitor application performance

---

## Support

If you encounter issues:
1. Check the error logs
2. Verify environment variables
3. Ensure all dependencies are installed
4. Check Django documentation
5. Railway/Heroku support documentation

---

**Your application is now deployed and ready to use!** 🎉
