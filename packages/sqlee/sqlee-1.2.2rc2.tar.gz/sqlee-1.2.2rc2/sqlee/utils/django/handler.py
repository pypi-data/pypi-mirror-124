from django.db import models
import os
import sqlee
import sys
import json
import requests

if 'DJANGO_SETTINGS_MODULE' in os.environ:
    settings = __import__(os.environ['DJANGO_SETTINGS_MODULE']).settings
else:
    raise ImportError("Django工程未被执行，请在Django工程中导入Sqlee的Django组件.")
try:
    if not settings.ENABLE_SQLEE or settings.SQLEE_NAME.replace(" ", "") == "":
        raise ImportError('Sqlee未在Django被正确配置.')
except Exception as exc:
    raise ImportError('Sqlee未在Django被正确配置.') from exc

def init():
    url = json.loads(requests.get("https://gitee.com/api/v5/repos/{user}/{name}?access_token={token}".format(
        user = settings.SQLEE_SETTINGS["OWNER"],
        name = settings.SQLEE_SETTINGS["NAME"],
        token = settings.SQLEE_SETTINGS["TOKEN"]
        )).text)
    if "message" in url:
        if url["message"] == "Not Found Project":
            print("开始创建数据库...")
            sqlee.utils.gitee.make_repo(token=settings.SQLEE_SETTINGS["TOKEN"], user=settings.SQLEE_SETTINGS["OWNER"], name=settings.SQLEE_SETTINGS["NAME"]).text
        else:
            raise Exception(url["message"])
    else:
        return True
            
def migrate():
    repo = sqlee.connect(token=settings.SQLEE_SETTINGS["TOKEN"], repo=settings.SQLEE_SETTINGS["NAME"], owner=settings.SQLEE_SETTINGS["OWNER"])
    sys.path.append(settings.BASE_DIR)

    for app in settings.INSTALLED_APPS:
        if app.split["."][0] != "django":
            models = "%s.%s.models" % (os.environ['DJANGO_SETTINGS_MODULE'].split["."][0], app)
            models = __import__(model)
            for model in dir(eval(models)):
                if model.__base__ is models.Model:
                    namespaces = []
                    for namespace in dir(model):
                        if model.__base__ is models.Field:
                            namespaces.append(namespace)
                    repo.objects.create(name='%s_%s' % (app, model.__class__.__name__), namespace=namespace)
    return True
                
