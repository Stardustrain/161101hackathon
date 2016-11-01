from django.shortcuts import render,reverse,redirect
from django.http import HttpResponse
from django.conf import settings
import requests
from .models import ServiceUser
from django.contrib.auth import authenticate as auth, login as auth_login, logout as auth_logout


def login(request):
    return render(request, 'member/login.html', {})


def fb_login(request):
    code = request.GET.get('code')


    redirect_uri = 'https://graph.facebook.com/v2'\
    '.8/oauth/access_token?'\
    'client_id={app_id}'\
    '&redirect_uri={redirect_url}'\
    '&client_secret={app_secret}'\
    '&code={code_parameter}'.format(app_id=settings.FACEBOOK_APP_ID,
                                   redirect_url='http://127.0.0.1:8000/member/fb_login/',
                                   app_secret=settings.APP_SECRET_CODE,
                                   code_parameter=code)
    r = requests.get(redirect_uri)
    dic_r = r.json()
    access_token = dic_r['access_token']
    app_secret_code = '{}|{}'.format(settings.FACEBOOK_APP_ID,settings.APP_SECRET_CODE)
    debug_redirect_uri = 'https://graph.facebook.com/debug_token?'\
                         'input_token={access_token}'\
                         '&access_token={app_secret_code}'.format(access_token=access_token,
                                                                 app_secret_code=app_secret_code)

    r = requests.get(debug_redirect_uri)
    dic_r = r.json()
    user_id = dic_r['data']['user_id']

    user_info_uri = 'https://graph.facebook.com/{user_id}?'\
                    'fields=id,email,first_name,last_name'\
                    '&access_token={access_token}'.format(user_id=user_id,
                                                          access_token=access_token)
    r = requests.get(user_info_uri)
    dic_r = r.json()
    user_info = dic_r

    try:
        user_id = ServiceUser.objects.get(email=dic_r['email'])
    except:
        user_id = ServiceUser.objects.create_user(dic_r)


    user = auth(user_info=user_info)
    auth_login(request,user)
    if user.is_teacher :
        return redirect('poll:poll_edit')
    else:
        return redirect('poll:poll_list')


def logout(request):
    auth_logout(request)
    return redirect('poll:poll_list')