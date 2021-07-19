"""vulscan_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from . import test, scan, json

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', test.test),
    path('scan/tasklist/', scan.task_list),
    path('scan/fofalist/', scan.fofa_list),
    path('scan/poclist/', scan.poc_list),
    path('scan/iplist/', scan.ip_list),
    path('scan/service/', scan.service_scan),
    path('scan/vuln/', scan.vuln_scan),
    path('scan/start/', scan.start_scan),
    path('scan/repeat/', scan.repeat_scan),
    path('scan/export/', scan.export_file),
    path('scan/delete/', scan.delete_task),
    path('scan/stop/', scan.stop_task),
    path('scan/fofa/', scan.fofa_scan),
    path('scan/poc/add/', scan.add_poc),
    path('scan/exp/', scan.exp),
    path('scan/ip/', scan.ip_scan),
    path('json/refresh/', json.get_async_result),
    path('json/id/', json.get_task_id),
    path('json/edit/', json.edit),
    path('json/poc/', json.use_poc),
    path('json/exp/', json.get_exp),
    path('json/switch/service/', json.switch_service),
    path('json/add/note/', json.add_note),
    path('json/clear/note/', json.clear_note),
    path('json/switch/poc/', json.switch_poc),
]
