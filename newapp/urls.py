from django.urls import path

from newapp import views

urlpatterns = [
    path('regview/',views.regview,name="regview" ),
    path('reglogic/',views.reglogic,name="reglogic" ),
    path('logview/',views.logview,name="logview" ),
    path('loglogic/',views.loglogic,name="loglogic" ),
    path('deptview/',views.deptview,name="deptview" ),
    path('empbydept/',views.empbydept,name="empbydept" ),
    path('updatedeptview/',views.updatedeptview,name="updatedeptview" ),
    path('updatelogic/',views.updatelogic,name="updatelogic" ),
    path('addeptview/',views.addeptview,name="addeptview" ),
    path('addeptlogic/',views.addeptlogic,name="addeptlogic" ),
    path('addempview/',views.addempview,name="addempview" ),
    path('addemplogic/',views.addemplogic,name="addemplogic" ),
    path('updateempview/',views.updateempview,name="updateempview" ),
    path('updateemplogic/',views.updateemplogic,name="updateemplogic" ),
    path('deleteemp/',views.deleteemp,name="deleteemp" ),
    path('captcha/',views.getcaptcha,name="captcha" ),
    path('ajax_username/',views.ajax_username,name="namecheck" ),
    path('ajax_captcha/',views.ajax_captcha,name="ajax_captcha" ),
]
