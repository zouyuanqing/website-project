from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """客户端用户模型"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # 关联提交记录
    submissions = db.relationship('Submission', backref='user', lazy=True)
    
    def __init__(self, name, email=None, phone=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.email = email
        self.phone = phone
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email or self.phone}>'

class Admin(UserMixin, db.Model):
    """管理员模型"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return f"admin_{self.id}"
    
    def __repr__(self):
        return f'<Admin {self.email}>'

class Form(db.Model):
    """表单模型"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    allow_multiple_submissions = db.Column(db.Boolean, default=False)  # 是否允许多次填写
    created_by = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    
    # 关联字段和提交记录
    fields = db.relationship('FormField', backref='form', lazy=True, cascade='all, delete-orphan')
    submissions = db.relationship('Submission', backref='form', lazy=True, cascade='all, delete-orphan')
    
    def get_share_url(self):
        return f"/form/{self.id}"
    
    def __repr__(self):
        return f'<Form {self.title}>'

class FormField(db.Model):
    """表单字段模型"""
    id = db.Column(db.Integer, primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('form.id'), nullable=False)
    field_name = db.Column(db.String(100), nullable=False)
    field_label = db.Column(db.String(200), nullable=False)
    field_type = db.Column(db.String(50), nullable=False)  # text, email, tel, textarea, select, radio, checkbox, file, wechat_pay, alipay
    field_options = db.Column(db.Text)  # JSON格式存储选项
    is_required = db.Column(db.Boolean, default=False)
    order_index = db.Column(db.Integer, default=0)
    placeholder = db.Column(db.String(200))
    payment_account_id = db.Column(db.Integer, db.ForeignKey('payment_account.id'))  # 关联收款账户（仅限支付字段）
    
    # 关联收款账户
    payment_account = db.relationship('PaymentAccount', backref='form_fields', lazy=True)
    
    def get_options(self):
        if self.field_options:
            try:
                return json.loads(self.field_options)
            except:
                return []
        return []
    
    def set_options(self, options):
        self.field_options = json.dumps(options, ensure_ascii=False)
    
    def __repr__(self):
        return f'<FormField {self.field_label}>'

class Submission(db.Model):
    """提交记录模型"""
    id = db.Column(db.Integer, primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('form.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='submitted')  # submitted, reviewed, approved, rejected
    
    # 关联提交数据
    data = db.relationship('SubmissionData', backref='submission', lazy=True, cascade='all, delete-orphan')
    files = db.relationship('UploadFile', backref='submission', lazy=True, cascade='all, delete-orphan')
    
    def get_data_dict(self):
        result = {}
        for data in self.data:
            result[data.field_name] = data.field_value
        return result
    
    def __repr__(self):
        return f'<Submission {self.id}>'

class SubmissionData(db.Model):
    """提交数据模型"""
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id'), nullable=False)
    field_name = db.Column(db.String(100), nullable=False)
    field_value = db.Column(db.Text)
    
    def __repr__(self):
        return f'<SubmissionData {self.field_name}>'

class UploadFile(db.Model):
    """上传文件模型"""
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id'), nullable=False)
    field_name = db.Column(db.String(100), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    saved_filename = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer)
    file_type = db.Column(db.String(100))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<UploadFile {self.original_filename}>'

class PaymentOrder(db.Model):
    """支付订单模型"""
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id'), nullable=False)
    field_name = db.Column(db.String(100), nullable=False)  # 支付字段名称
    payment_type = db.Column(db.String(20), nullable=False)  # wechat_pay, alipay
    amount = db.Column(db.Numeric(10, 2), nullable=False)  # 支付金额
    order_no = db.Column(db.String(64), unique=True, nullable=False)  # 订单号
    trade_no = db.Column(db.String(64))  # 第三方交易号
    status = db.Column(db.String(20), default='pending')  # pending, paid, failed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    paid_at = db.Column(db.DateTime)
    payment_data = db.Column(db.Text)  # JSON格式存储支付相关数据
    payment_account_id = db.Column(db.Integer, db.ForeignKey('payment_account.id'))  # 关联收款账户
    
    # 关联提交记录和收款账户
    submission = db.relationship('Submission', backref='payment_orders', lazy=True)
    payment_account = db.relationship('PaymentAccount', backref='orders', lazy=True)
    
    def get_payment_data(self):
        if self.payment_data:
            try:
                return json.loads(self.payment_data)
            except:
                return {}
        return {}
    
    def set_payment_data(self, data):
        self.payment_data = json.dumps(data, ensure_ascii=False)
    
    def __repr__(self):
        return f'<PaymentOrder {self.order_no}>'

class PaymentAccount(db.Model):
    """收款账户模型"""
    id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(100), nullable=False)  # 账户名称
    account_type = db.Column(db.String(20), nullable=False)  # wechat, alipay, bank_card
    account_number = db.Column(db.String(50), nullable=False)  # 账号/卡号
    account_holder = db.Column(db.String(100), nullable=False)  # 收款人姓名
    bank_name = db.Column(db.String(100))  # 银行名称（仅限银行卡）
    bank_branch = db.Column(db.String(200))  # 开户行（仅限银行卡）
    is_active = db.Column(db.Boolean, default=True)  # 是否启用
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    notes = db.Column(db.Text)  # 备注
    
    # 关联创建者
    creator = db.relationship('Admin', backref='payment_accounts', lazy=True)
    
    def get_account_display(self):
        """获取账户显示信息"""
        if self.account_type == 'bank_card':
            masked_number = self.account_number[:4] + '*' * (len(self.account_number) - 8) + self.account_number[-4:]
            return f"{self.bank_name} {masked_number}"
        else:
            # 对于微信和支付宝，只显示部分信息
            if len(self.account_number) > 6:
                masked_number = self.account_number[:3] + '*' * (len(self.account_number) - 6) + self.account_number[-3:]
            else:
                masked_number = '*' * len(self.account_number)
            return f"{self.account_holder} ({masked_number})"
    
    def __repr__(self):
        return f'<PaymentAccount {self.account_name}>'
