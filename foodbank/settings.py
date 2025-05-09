
import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!tr#s^vr&gg)be1s$sm5hafkvh*7h_4xpq6b&r5cph**2gwy7v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CSRF_TRUSTED_ORIGINS = [
    'https://micro-foodbank-backend-44tkf.kinsta.app',
    # Keep any existing origins
]

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'micro-foodbank-backend-44tkf.kinsta.app'
]


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 3rd Party Apps
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'django_filters',
    'rest_framework_swagger',
    'drf_yasg',
    
    
    # Local Apps
    'accounts.apps.AccountsConfig',
    'farmerDashBoard.apps.FarmerdashboardConfig',
    'investorDashBoard.apps.InvestordashboardConfig',
    'support.apps.SupportConfig',
    'loans.apps.LoansConfig',  
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'foodbank.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'foodbank.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # For development
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'accounts.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    
    'JTI_CLAIM': 'jti',
}




JAZZMIN_SETTINGS = {
    
     # Custom CSS/JS
    "custom_css": "css/jazzmin_custom.css",
    # "custom_js": "js/jazzmin_custom.js",
    "use_google_fonts_cdn": True,
    
    
    # Core Settings
    "site_title": "Micro Foodbank",
    "site_header": "Foodbank",
    "site_brand": "Foodbank",
    "site_logo": "logo/logo.jpg",  
    # "login_logo": None,   
    "site_logo_classes": "img-circle",
    
     
    # "site_icon": "logo/favicon.ico", 
    "welcome_sign": "Welcome to Micro Foodbank Administration",
    "copyright": "Micro Foodbank © 2025",
    
    # UI Configuration
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
    # "language_chooser": None,
    "show_sidebar": True,
    "navigation_expanded": False,  # Start with collapsed navigation for cleaner look
    "related_modal_active": True,  # Enable related modal for better UX when selecting related objects
    
    # Menu Structure
    "topmenu_links": [
        {"name": "Dashboard", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "API Documentation", "url": "/api/schema/swagger-ui/", "new_window": True},
        {"name": "Support", "url": "mailto:support@agriloan.com", "new_window": True},
        {"model": "auth.User"},
    ],
    
    # User Menu (top right)
    "usermenu_links": [
        {"name": "Support", "url": "mailto:support@agriloan.com", "new_window": True},
        {"name": "Change Password", "url": "admin:password_change", "permissions": ["auth.view_user"]},
    ],
    
    # App/Model Organization
    "hide_apps": ["auth_token"],
    "hide_models": [],
    "order_with_respect_to": ["users", "users.User", "farmers", "investors", "agents", "loans", "transactions"],
    
    # Search Configuration
    "search_model": ["users.User", "farmers.FarmerProfile", "investors.InvestorProfile", "agents.AgentProfile"],
    
    # Icons (using Font Awesome 5)
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "users": "fas fa-users",
        "users.User": "fas fa-user",
        "farmers.FarmerProfile": "fas fa-tractor",
        "investors.InvestorProfile": "fas fa-chart-line",
        "agents.AgentProfile": "fas fa-user-tie",
        "loans.Loan": "fas fa-hand-holding-usd",
        "transactions.Transaction": "fas fa-exchange-alt",
    },
    
    # Default Icons
    "default_icon_parents": "fas fa-folder",
    "default_icon_children": "fas fa-file",
    
    # Custom Links
    "custom_links": {
        "farmers": [{
            "name": "Export Farmers Data",
            "url": "admin:export_farmers_data",
            "icon": "fas fa-file-export",
            "permissions": ["farmers.view_farmerprofile"]
        }],
        "investors": [{
            "name": "Export Investors Data",
            "url": "admin:export_investors_data",
            "icon": "fas fa-file-export",
            "permissions": ["investors.view_investorprofile"]
        }],
        "loans": [{
            "name": "Export Loan Report",
            "url": "admin:export_loan_report",
            "icon": "fas fa-file-csv",
            "permissions": ["loans.view_loan"]
        }],
    },
    
   
}

# Dark Mode Settings
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-success",
    "accent": "accent-success",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-success",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'DEFAULT_AUTO_SCHEMA_CLASS': 'accounts.utils.SafeSwaggerAutoSchema'
}