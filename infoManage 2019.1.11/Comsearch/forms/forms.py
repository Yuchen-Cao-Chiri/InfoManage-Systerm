from django import forms

from django.forms import ModelForm, Select, TextInput

from Comsearch.models import QueryUser

'''
@Desc
    表单
@Author monkey
@Date 2018-04-03
'''
# ======  另一种写法  ========
''''''
CONDITION_CHOICES = (
    ('name', '公司名称'),
    ('credit_code', '统一社会信用代码'),
    ('organization_code', '组织机构代码'),
    ('registration_num', '公司注册号'),
    ('trade', '所属行业'),
    ('style', '公司类型'),
    ('legal_person', '公司法人'),
    ('capital', '注册资本'),
    ('address', '公司地址'),
)

# class QueryUserForm(forms.Form):
#     condition = forms.CharField(  # 也可以定义为 ChoiceField
#         max_length=20,
#         widget=forms.Select(choices=CONDITION_CHOICES,
#                             attrs={'class':"form-control",
#                                     'title':"query condition",
#                                     'name':'condition',
#                                     }),
#         localize=('username', '用户名')
#     )
#
#     queryContent = forms.CharField(
#         max_length=100,
#         widget=forms.TextInput(attrs={'class': 'form-control is-invalid',
#                                       'name': 'queryContent',
#                                       'placeholder': '请输入需要要查询的内容...'
#                                       }),
#         error_messages={'required': '查询内容不能为空 !'}
#     )


# 上面的代码等同于 下面的表单 QueryUserForm + 模型 QueryUser

class QueryUserForm(ModelForm):

    class Meta:
        model = QueryUser
        fields = ['condition', 'queryContent', ]
        # 指定呈现样式字段、指定 CSS 样式
        widgets = {
            'condition': Select(attrs={'class':"form-control",
                                    'title':"query condition",
                                    'name':'condition',
                                    }),
            'queryContent':TextInput(attrs={'class': 'form-control is-invalid',
                                      'name': 'queryContent',
                                      'placeholder': '请输入需要要查询的内容...'
                                      })
        }

        localized = {
            'condition':('username', '用户名'),
            'queryContent':123
        }

        # 自定义错误信息
        error_messages = {
            'queryContent':{
                'required': '查询内容不能为空 !',
            }
        }



class UserForm(forms.Form):

    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
