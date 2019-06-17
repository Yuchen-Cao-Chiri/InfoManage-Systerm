from django.db import models

# Create your models here.

class Cominfo(models.Model):

    status_gender = (
        ('存续', '存续'),
        ('注销', '注销'),
    )

    style_gender = (
        ('有限责任公司', '有限责任公司'),
        ('股份有限公司', '股份有限公司'),
        ('个体工商户', '个体工商户'),
        ('个人独资企业', '个人独资企业'),
        ('合伙企业', '合伙企业'),
    )

    # id = models.AutoField(primary_key=True);
    name = models.CharField(max_length=40);
    credit_code = models.CharField(max_length=40);
    organization_code = models.CharField(max_length=40);
    registration_num = models.CharField(max_length=40);
    status = models.CharField(max_length=40, choices=status_gender, default='存续');
    trade = models.CharField(max_length=40,null=True);
    e_date = models.CharField(max_length=40,null=True);
    style = models.CharField(max_length=40, choices=style_gender, default='有限责任公司');
    term = models.CharField(max_length=40,null=True);
    legal_person = models.CharField(max_length=40,null=True);
    f_date = models.CharField(max_length=40,null=True);
    capital = models.CharField(max_length=40,null=True);
    authority = models.CharField(max_length=40,null=True);
    address = models.CharField(max_length=40,null=True);

    class Meta:
        managed = True
        db_table = 'imformation'

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

class QueryUser(models.Model):
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    queryContent = models.CharField(max_length=100)

    def __str__(self):              # __unicode__ on Python 2
        return self.condition

class User(models.Model):

    gender = (
        ('male', '男'),
        ('female', '女'),
    )

    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='男')
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'

