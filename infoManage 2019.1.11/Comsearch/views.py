from django.template import loader
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import connection
from django.shortcuts import render,reverse
from Comsearch import models
from django.http import HttpResponseRedirect,HttpResponse
from .forms.forms import QueryUserForm, UserForm,RegisterForm
from django.views.decorators.csrf import csrf_exempt
import json


def login(request):
    # if request.session.get('is_login', None):
    #     return HttpResponseRedirect(reverse('login'))

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(username=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.username
                    return HttpResponseRedirect(reverse('index'))
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login.html', locals())

    login_form = UserForm()
    return render(request, 'login.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return HttpResponseRedirect(reverse('login'))
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return HttpResponseRedirect(reverse('login'))


def register(request):
    # if request.session.get('is_login', None):
    #     # 登录状态不允许注册。你可以修改这条原则！
    #     return HttpResponseRedirect(reverse('login'))
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'register.html', locals())
            else:
                same_name_user = models.User.objects.filter(username=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.User.objects.create()
                new_user.username = username
                new_user.password = password1
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return HttpResponseRedirect(reverse('login'))
    register_form = RegisterForm()
    return render(request, 'register.html', locals())


def index(request):
    return render(request, 'index.html')

def welcome(request):
    cominfo_list_obj = models.Cominfo.objects.all()
    return render(request, 'welcome.html', {'cominfo_list': cominfo_list_obj})

def information(request):
    cominfo_list_obj = models.Cominfo.objects.all()
    paginator = Paginator(cominfo_list_obj, 5)
    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            coms = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            coms = paginator.page(1)
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            coms = paginator.page(paginator.num_pages)

    return render(request, 'information.html', {'coms': coms})

def add_cominfo(request):
    if request.method == "POST":
        name = request.POST['name']
        credit_code = request.POST['credit_code']
        organization_code = request.POST['organization_code']
        registration_num = request.POST['registration_num']
        status = request.POST['status']
        trade = request.POST['trade']
        e_date = request.POST['e_date']
        style = request.POST['style']
        term = request.POST['term']
        legal_person = request.POST['legal_person']
        f_date = request.POST['f_date']
        capital = request.POST['capital']
        authority = request.POST['authority']
        address = request.POST['address']
        models.Cominfo.objects.create(name=name, credit_code=credit_code, organization_code=organization_code, registration_num=registration_num,status=status,trade=trade,  e_date=e_date,style=style,term=term,legal_person=legal_person,f_date=f_date,capital=capital,authority=authority,address=address)
        return HttpResponseRedirect(reverse('information'))
    elif request.method == "GET":
        return render(request, 'information_add.html')

@csrf_exempt
def del_cominfo(request):
    if request.method == "POST":
        id = request.POST.get('id')
        print("id  =  %s" %id)
        status = "删除成功！"
        result = "Error!"
        deletesql = models.Cominfo.objects.filter(id=id) # 执行删除操作
        if deletesql.delete():
            # return HttpResponseRedirect(reverse('information'))
            return HttpResponse(json.dumps({
                "status": status
            }))
        else:
            return HttpResponse(json.dumps({
                "result": result
            }))

@csrf_exempt
def deleteSelect(request):
    # if request.method == "POST":
    print('开始进行批量删除！')
    ids = request.POST["ids"]
    print(ids)
    # idstring = ','.join(ids)
    deletesql = models.Cominfo.objects.extra(where=['id IN (' + ids + ')'])
    # models.Cominfo.objects.extra(where=['id IN (' + idstring + ')']).delete()
    context = {
        "success": '删除成功',
        "error": '删除失败'
    }
    if deletesql.delete():
        # return render(request, "home.html", context=context)
        return HttpResponse(json.dumps({
            "success": '删除成功'
        }))
    else:
        return HttpResponse(json.dumps({
            "error": '删除失败'
        }))

def mod_cominfo(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        com_detail = models.Cominfo.objects.get(id=id)
        context = {'com_detail': com_detail}
        return render(request, 'information_mod.html', context=context)
    if request.method == "POST":
        id = request.POST.get('id')
        name = request.POST.get('name')
        credit_code = request.POST.get('credit_code')
        organization_code = request.POST.get('organization_code')
        registration_num = request.POST.get('registration_num')
        status = request.POST.get('status')
        trade = request.POST.get('trade')
        e_date = request.POST.get('e_date')
        style = request.POST.get('style')
        term = request.POST.get('term')
        legal_person = request.POST.get('legal_person')
        f_date = request.POST.get('f_date')
        capital = request.POST.get('capital')
        authority = request.POST.get('authority')
        address = request.POST.get('address')
        models.Cominfo.objects.filter(id=id).update(name=name, credit_code=credit_code, organization_code=organization_code, registration_num=registration_num,status=status,trade=trade,  e_date=e_date,style=style,term=term,legal_person=legal_person,f_date=f_date,capital=capital,authority=authority,address=address)
        return HttpResponseRedirect(reverse('information'))


def search(request):
    templateView = 'search.html'
    countNum = -1
    keywords = ''
    time = 0

    if request.method == 'GET':

        form = QueryUserForm(request.GET)
        '''
            没有使用 Django 内置组件的验证表单的作用
        # 获得用户输入值
        if 'q' in request.GET and request.GET['q']:

            keywords = request.GET['q']
            print('keywords == ' + keywords)

            # 查询结果
            results = 3
            countNum = 3
            # 查询不到数据, 显示浮窗
            if countNum == 0:
                return render(request, templateView, {
                    'countNum': countNum,
                    'keywords': keywords,
                })
            # 查询到数据, 显示结果
            elif countNum == 3:
                return render(request, templateView, {
                    'countNum': countNum,
                    'keywords': keywords,
                })
        # 直接访问主页, 显示的内容
        else:
            return render(request, templateView, {'countNum': countNum,  'form': form})
        '''
        # 验证表单
        if form.is_valid():
            # 过滤需要的数据
            condition = form.cleaned_data['condition']
            keywords = form.cleaned_data['queryContent']

            print('condition == ' + condition)
            print('keywords == ' + keywords)

            countNum = 0
            # 查询结果
            if condition == 'name':
                user_list = models.Cominfo.objects.filter(name__icontains=keywords)
                countNum = user_list.count()
                time = (connection.queries)[0].get('time')
                print('user_list size=== ', user_list.count())
                print('time === ', time)

                # 显示分页操作, 每页显示 20 条
                paginator = Paginator(user_list, 20)
                page = request.GET.get('page')
                try:
                    users = paginator.page(page)
                except PageNotAnInteger:
                    # 如果请求的页数不是整数，返回第一页。
                    users = paginator.page(1)
                except EmptyPage:
                    # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                    users = paginator.page(paginator.num_pages)

                return render(request, templateView, {
                        'countNum': countNum,
                        'condition': condition,
                        'keywords': keywords,
                        'form': form,
                        'users': users,
                        'time': time,
                    })
            elif condition == 'credit_code':
                user_list = models.Cominfo.objects.filter(credit_code__icontains=keywords)
                countNum = user_list.count()
                time = (connection.queries)[0].get('time')
                print('user_list size=== ', user_list.count())
                print('time === ', time)

                # 显示分页操作, 每页显示 20 条
                paginator = Paginator(user_list, 20)
                page = request.GET.get('page')
                try:
                    users = paginator.page(page)
                except PageNotAnInteger:
                    # 如果请求的页数不是整数，返回第一页。
                    users = paginator.page(1)
                except EmptyPage:
                    # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                    users = paginator.page(paginator.num_pages)

                return render(request, templateView, {
                        'countNum': countNum,
                        'condition': condition,
                        'keywords': keywords,
                        'form': form,
                        'users': users,
                        'time': time,
                    })
            elif condition == 'organization_code':
                user_list = models.Cominfo.objects.filter(organization_code__icontains=keywords)
                countNum = user_list.count()
                time = (connection.queries)[0].get('time')
                print('user_list size=== ', user_list.count())
                print('time === ', time)

                # 显示分页操作, 每页显示 20 条
                paginator = Paginator(user_list, 20)
                page = request.GET.get('page')
                try:
                    users = paginator.page(page)
                except PageNotAnInteger:
                    # 如果请求的页数不是整数，返回第一页。
                    users = paginator.page(1)
                except EmptyPage:
                    # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                    users = paginator.page(paginator.num_pages)

                return render(request, templateView, {
                        'countNum': countNum,
                        'condition': condition,
                        'keywords': keywords,
                        'form': form,
                        'users': users,
                        'time': time,
                    })
            elif condition == 'registration_num':
                user_list = models.Cominfo.objects.filter(registration_num__icontains=keywords)
                countNum = user_list.count()
                time = (connection.queries)[0].get('time')
                print('user_list size=== ', user_list.count())
                print('time === ', time)

                # 显示分页操作, 每页显示 20 条
                paginator = Paginator(user_list, 20)
                page = request.GET.get('page')
                try:
                    users = paginator.page(page)
                except PageNotAnInteger:
                    # 如果请求的页数不是整数，返回第一页。
                    users = paginator.page(1)
                except EmptyPage:
                    # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                    users = paginator.page(paginator.num_pages)

                return render(request, templateView, {
                        'countNum': countNum,
                        'condition': condition,
                        'keywords': keywords,
                        'form': form,
                        'users': users,
                        'time': time,
                    })
            elif condition == 'trade':
                user_list = models.Cominfo.objects.filter(trade__icontains=keywords)
                countNum = user_list.count()
                time = (connection.queries)[0].get('time')
                print('user_list size=== ', user_list.count())
                print('time === ', time)

                # 显示分页操作, 每页显示 20 条
                paginator = Paginator(user_list, 20)
                page = request.GET.get('page')
                try:
                    users = paginator.page(page)
                except PageNotAnInteger:
                    # 如果请求的页数不是整数，返回第一页。
                    users = paginator.page(1)
                except EmptyPage:
                    # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                    users = paginator.page(paginator.num_pages)

                return render(request,templateView, {
                        'countNum': countNum,
                        'condition': condition,
                        'keywords': keywords,
                        'form': form,
                        'users': users,
                        'time': time,
                    })
            elif condition == 'style':
                user_list = models.Cominfo.objects.filter(style__icontains=keywords)
                countNum = user_list.count()
                time = (connection.queries)[0].get('time')
                print('user_list size=== ', user_list.count())
                print('time === ', time)

                # 显示分页操作, 每页显示 20 条
                paginator = Paginator(user_list, 20)
                page = request.GET.get('page')
                try:
                    users = paginator.page(page)
                except PageNotAnInteger:
                    # 如果请求的页数不是整数，返回第一页。
                    users = paginator.page(1)
                except EmptyPage:
                    # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                    users = paginator.page(paginator.num_pages)

                return render(request, templateView, {
                        'countNum': countNum,
                        'condition': condition,
                        'keywords': keywords,
                        'form': form,
                        'users': users,
                        'time': time,
                    })
            elif condition == 'legal_person':
                user_list = models.Cominfo.objects.filter(legal_person__icontains=keywords)
                countNum = user_list.count()
                time = (connection.queries)[0].get('time')
                print('user_list size=== ', user_list.count())
                print('time === ', time)

                # 显示分页操作, 每页显示 20 条
                paginator = Paginator(user_list, 20)
                page = request.GET.get('page')
                try:
                    users = paginator.page(page)
                except PageNotAnInteger:
                    # 如果请求的页数不是整数，返回第一页。
                    users = paginator.page(1)
                except EmptyPage:
                    # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                    users = paginator.page(paginator.num_pages)

                return render(request, templateView, {
                        'countNum': countNum,
                        'condition': condition,
                        'keywords': keywords,
                        'form': form,
                        'users': users,
                        'time': time,
                    })
            elif condition == 'capital':
                user_list = models.Cominfo.objects.filter(capital__icontains=keywords)
                countNum = user_list.count()
                time = (connection.queries)[0].get('time')
                print('user_list size=== ', user_list.count())
                print('time === ', time)

                # 显示分页操作, 每页显示 20 条
                paginator = Paginator(user_list, 20)
                page = request.GET.get('page')
                try:
                    users = paginator.page(page)
                except PageNotAnInteger:
                    # 如果请求的页数不是整数，返回第一页。
                    users = paginator.page(1)
                except EmptyPage:
                    # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                    users = paginator.page(paginator.num_pages)

                return render(request, templateView, {
                        'countNum': countNum,
                        'condition': condition,
                        'keywords': keywords,
                        'form': form,
                        'users': users,
                        'time': time,
                    })
            elif condition == 'address':
                user_list = models.Cominfo.objects.filter(address__icontains=keywords)
                countNum = user_list.count()
                time = (connection.queries)[0].get('time')
                print('user_list size=== ', user_list.count())
                print('time === ', time)

                # 显示分页操作, 每页显示 20 条
                paginator = Paginator(user_list, 20)
                page = request.GET.get('page')
                try:
                    users = paginator.page(page)
                except PageNotAnInteger:
                    # 如果请求的页数不是整数，返回第一页。
                    users = paginator.page(1)
                except EmptyPage:
                    # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                    users = paginator.page(paginator.num_pages)

                return render(request, templateView, {
                        'countNum': countNum,
                        'condition': condition,
                        'keywords': keywords,
                        'form': form,
                        'users': users,
                        'time': time,
                    })

            # 查询不到数据, 显示没有数据的浮窗
            if countNum == 0:
                return render(request, templateView, {
                    'countNum': countNum,
                    'keywords': keywords,
                    'form': form,
                })
        # 直接访问主页, 显示的内容
        else:
            return render(request, templateView, {'countNum': countNum,  'form': form})


