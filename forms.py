from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, SelectField, BooleanField, IntegerField, FieldList, FormField, RadioField, SelectMultipleField, DecimalField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, NumberRange
from wtforms.widgets import CheckboxInput, ListWidget
import re

class LoginForm(FlaskForm):
    """用户登录表单"""
    login_id = StringField('手机号码或邮箱', validators=[DataRequired(), Length(min=5, max=120)])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    
    def validate_login_id(self, field):
        # 验证是否为有效的手机号或邮箱
        phone_pattern = r'^1[3-9]\d{9}$'
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not (re.match(phone_pattern, field.data) or re.match(email_pattern, field.data)):
            raise ValueError('请输入有效的手机号码或邮箱地址')

class RegisterForm(FlaskForm):
    """用户注册表单"""
    name = StringField('姓名', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('邮箱', validators=[Optional(), Email(), Length(max=120)])
    phone = StringField('手机号码', validators=[Optional(), Length(min=11, max=11)])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6, max=20)])
    password2 = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password', message='密码不一致')])
    
    def validate_phone(self, field):
        if field.data:
            phone_pattern = r'^1[3-9]\d{9}$'
            if not re.match(phone_pattern, field.data):
                raise ValueError('请输入有效的手机号码')
    
    def validate(self, extra_validators=None):
        if not super().validate(extra_validators=extra_validators):
            return False
        
        # 至少需要填写邮箱或手机号中的一个
        if not self.email.data and not self.phone.data:
            self.email.errors.append('请至少填写邮箱或手机号中的一个')
            self.phone.errors.append('请至少填写邮箱或手机号中的一个')
            return False
        
        return True

class AdminLoginForm(FlaskForm):
    """管理员登录表单"""
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])

class FormFieldForm(FlaskForm):
    """表单字段子表单"""
    field_name = StringField('字段名称', validators=[DataRequired(), Length(max=100)])
    field_label = StringField('字段标签', validators=[DataRequired(), Length(max=200)])
    field_type = SelectField('字段类型', choices=[
        ('text', '单行文本'),
        ('textarea', '多行文本'),
        ('email', '邮箱'),
        ('tel', '电话'),
        ('select', '下拉选择'),
        ('radio', '单选框'),
        ('checkbox', '多选框'),
        ('file', '文件上传'),
        ('number', '数字'),
        ('date', '日期'),
        ('wechat_pay', '微信支付'),
        ('alipay', '支付宝支付')
    ], validators=[DataRequired()])
    placeholder = StringField('占位符', validators=[Optional(), Length(max=200)])
    is_required = BooleanField('是否必填')
    options = TextAreaField('选项（每行一个，适用于选择类字段）', validators=[Optional()])
    order_index = IntegerField('排序', default=0)

class CreateFormForm(FlaskForm):
    """创建表单"""
    title = StringField('表单标题', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('表单描述', validators=[Optional()])
    fields = FieldList(FormField(FormFieldForm), min_entries=1)

class EditFormForm(FlaskForm):
    """编辑表单"""
    title = StringField('表单标题', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('表单描述', validators=[Optional()])
    is_active = BooleanField('是否启用')

class DynamicForm(FlaskForm):
    """动态表单基类"""
    def __init__(self, form_fields=None, formdata=None, **kwargs):
        # 先调用父类初始化，这会处理CSRF保护
        super().__init__(formdata=formdata, **kwargs)
        
        # 保存表单字段定义
        self.form_fields = form_fields
        
        # 在父类初始化后再创建自定义字段
        if form_fields:
            self.create_fields(form_fields, formdata)
    
    def create_fields(self, form_fields, formdata=None):
        """根据表单字段定义动态创建字段"""
        for field in form_fields:
            validators = []
            if field.is_required:
                validators.append(DataRequired())
            
            field_kwargs = {
                'label': field.field_label,
                'validators': validators
            }
            
            if field.placeholder:
                field_kwargs['render_kw'] = {'placeholder': field.placeholder}
            
            # 创建字段类型
            field_class = None
            if field.field_type == 'text':
                field_class = StringField
            elif field.field_type == 'textarea':
                field_class = TextAreaField
            elif field.field_type == 'email':
                if field.is_required:
                    field_kwargs['validators'].append(Email())
                field_class = StringField
            elif field.field_type == 'tel':
                field_class = StringField
            elif field.field_type == 'number':
                field_class = IntegerField
            elif field.field_type == 'select':
                options = [(opt, opt) for opt in field.get_options()]
                options.insert(0, ('', '请选择...'))
                field_kwargs['choices'] = options
                field_class = SelectField
            elif field.field_type == 'radio':
                options = [(opt, opt) for opt in field.get_options()]
                field_kwargs['choices'] = options
                field_class = RadioField
            elif field.field_type == 'checkbox':
                options = [(opt, opt) for opt in field.get_options()]
                field_kwargs['choices'] = options
                field_kwargs['widget'] = ListWidget(prefix_label=False)
                field_kwargs['option_widget'] = CheckboxInput()
                field_class = SelectMultipleField
            elif field.field_type == 'file':
                allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'pdf', 'doc', 'docx', 'mp4', 'avi', 'mov']
                field_kwargs['validators'] = [FileAllowed(allowed_extensions, '不支持的文件格式')] + field_kwargs['validators']
                field_class = FileField
            elif field.field_type in ['wechat_pay', 'alipay']:
                # 支付字段使用数字字段来输入金额
                field_kwargs['validators'].append(NumberRange(min=0.01, message='支付金额必须大于0'))
                field_kwargs['render_kw'] = {
                    'step': '0.01',
                    'min': '0.01',
                    'placeholder': '请输入支付金额（元）',
                    'class': 'form-control payment-amount'
                }
                field_class = DecimalField
            else:
                field_class = StringField
            
            # 创建绑定字段实例
            if field_class:
                # 获取初始数据
                initial_data = None
                if formdata and hasattr(formdata, 'get'):
                    initial_data = formdata.get(field.field_name)
                elif formdata and hasattr(formdata, '__getitem__'):
                    try:
                        initial_data = formdata[field.field_name]
                    except KeyError:
                        initial_data = None
                
                # 使用最简单的方式创建字段实例
                field_instance = field_class(**field_kwargs)
                
                # 设置字段的必要属性
                field_instance.name = field.field_name
                field_instance.object_data = None
                
                # 手动绑定表单和处理数据
                field_instance = field_instance.bind(self, field.field_name)
                
                # 正确处理表单数据
                if formdata:
                    field_instance.process(formdata)
                elif initial_data is not None:
                    field_instance.data = initial_data
                else:
                    # 为没有数据的情况提供空的formdata
                    field_instance.process({})
                
                # 将字段添加到表单
                setattr(self, field.field_name, field_instance)
                self._fields[field.field_name] = field_instance
