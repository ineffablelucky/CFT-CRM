import os

BASE_URL = 'http://localhost:8000/'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SETTINGS_DIR = os.path.dirname(__file__)
# print(SETTINGS_DIR)
PROJECT_PATH = os.path.join(SETTINGS_DIR, os.pardir)
# print(os.pardir)
# print(PROJECT_PATH)
PROJECT_PATH = os.path.abspath(PROJECT_PATH)
# print(PROJECT_PATH)
TEMPLATE_PATH = os.path.join(PROJECT_PATH, '')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8ynr_%1ly_!ga)jn9pil%lrny6i8@#clf!#)frj%lg-0dx(9(o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.leads.apps.LeadsConfig',
    'apps.attendance.apps.AttendanceConfig',
    'apps.client.apps.ClientConfig',
    'apps.leave.apps.LeaveConfig',
    'apps.ctc.apps.CtcConfig',
    'apps.meeting.apps.MeetingConfig',
    'apps.module.apps.ModuleConfig',
    'apps.monthly_salary.apps.MonthlySalaryConfig',
    'apps.opportunity.apps.OpportunityConfig',
    'apps.salary_percentages.apps.SalaryPercentagesConfig',
    'apps.task.apps.TaskConfig',
    'apps.time_entry.apps.TimeEntryConfig',
    'apps.users.apps.UsersConfig',
    'apps.project.apps.ProjectConfig',
    'apps.complaints.apps.ComplaintsConfig',
    'rest_framework',
    'rest_framework.authtoken',
    #'apps.salary_percentages.apps.SalaryPercentagesConfig',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'configs.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_PATH,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'configs.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = False
DATE_INPUT_FORMATS = ('%d/%m/%Y')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR , 'static'),
)

MEDIA_URL = '/media/'

MEDIA_ROOT = (
    os.path.join(BASE_DIR, 'media'),
)
print(MEDIA_ROOT)



STATICFILES_FINDERS = [
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

#STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = [
    'apps.users.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
    'apps.users.backends.MobileBackend',
]

AUTH_USER_MODEL = 'users.MyUser'

try:
    from configs.local_settings import *
except ImportError as e:
    pass

