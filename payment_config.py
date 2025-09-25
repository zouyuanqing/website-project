# -*- coding: utf-8 -*-
"""
支付配置和处理类
集成微信支付和支付宝官方接口
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass

# 微信支付相关
from wechatpy.pay import WeChatPay
from wechatpy.exceptions import WeChatPayException

# 支付宝相关
from alipay import AliPay
from alipay.utils import AliPayConfig

logger = logging.getLogger(__name__)


@dataclass
class PaymentResult:
    """支付结果数据类"""
    success: bool
    message: str
    data: Dict[str, Any] = None
    error_code: str = None
    trade_no: str = None
    payment_url: str = None
    qr_code: str = None  # 支付二维码内容


class WeChatPayConfig:
    """微信支付配置类"""
    
    def __init__(self):
        # 从环境变量或配置文件读取
        self.app_id = os.getenv('WECHAT_APP_ID', 'wx1234567890abcdef')
        self.mch_id = os.getenv('WECHAT_MCH_ID', '1234567890')
        self.mch_key = os.getenv('WECHAT_MCH_KEY', 'test32digitmerchantkeyherexxxxxxxx')
        self.notify_url = os.getenv('WECHAT_NOTIFY_URL', 'http://localhost:5000/payment/wechat/notify')
        self.return_url = os.getenv('WECHAT_RETURN_URL', 'http://localhost:5000/payment/return')
        
        # 证书路径（生产环境需要）
        self.cert_path = os.getenv('WECHAT_CERT_PATH', '')
        self.key_path = os.getenv('WECHAT_KEY_PATH', '')
        
        # 是否为沙箱环境
        self.sandbox = os.getenv('WECHAT_SANDBOX', 'true').lower() == 'true'
    
    def get_wechat_pay_client(self) -> Optional[WeChatPay]:
        """获取微信支付客户端"""
        try:
            return WeChatPay(
                appid=self.app_id,
                mch_id=self.mch_id,
                api_key=self.mch_key,  # 使用api_key参数
                sandbox=self.sandbox
            )
        except Exception as e:
            logger.warning(f"微信支付客户端初始化失败: {str(e)}")
            return None


class AlipayConfig:
    """支付宝配置类"""
    
    def __init__(self):
        # 从环境变量或配置文件读取
        self.app_id = os.getenv('ALIPAY_APP_ID', '2021000000000000')
        self.app_private_key = os.getenv('ALIPAY_PRIVATE_KEY', '')
        self.alipay_public_key = os.getenv('ALIPAY_PUBLIC_KEY', '')
        self.notify_url = os.getenv('ALIPAY_NOTIFY_URL', 'http://localhost:5000/payment/alipay/notify')
        self.return_url = os.getenv('ALIPAY_RETURN_URL', 'http://localhost:5000/payment/return')
        
        # 是否为沙箱环境
        self.sandbox = os.getenv('ALIPAY_SANDBOX', 'true').lower() == 'true'
        
        # 签名类型
        self.sign_type = 'RSA2'
        
        # 如果没有配置私钥，使用默认测试私钥（仅限开发环境）
        if not self.app_private_key:
            self.app_private_key = self._get_default_private_key()
        
        if not self.alipay_public_key:
            self.alipay_public_key = self._get_default_public_key()
    
    def _get_default_private_key(self) -> str:
        """获取默认测试私钥（仅限开发环境使用）"""
        # 在实际开发环境中，这里返回空字符串，让支付功能不可用但不会崩溃
        logger.info("支付宝配置缺失，运行在模拟模式下")
        return ""
    
    def _get_default_public_key(self) -> str:
        """获取默认公钥（仅限开发环境使用）"""
        # 在实际开发环境中，这里返回空字符串，让支付功能不可用但不会崩溃
        return ""
    
    def get_alipay_client(self) -> Optional[AliPay]:
        """获取支付宝客户端"""
        try:
            # 如果没有配置私钥，直接返回None
            if not self.app_private_key or not self.alipay_public_key:
                logger.info("支付宝私钥未配置，跳过支付宝客户端初始化")
                return None
            
            return AliPay(
                appid=self.app_id,
                app_notify_url=self.notify_url,
                app_private_key_string=self.app_private_key,
                alipay_public_key_string=self.alipay_public_key,
                sign_type=self.sign_type,
                debug=self.sandbox  # 开启调试模式，输出详细日志
            )
        except Exception as e:
            logger.warning(f"支付宝客户端初始化失败: {str(e)}")
            return None


class PaymentProcessor:
    """支付处理器主类"""
    
    def __init__(self):
        self.wechat_config = WeChatPayConfig()
        self.alipay_config = AlipayConfig()
        
        # 初始化支付客户端
        self.wechat_client = None
        self.alipay_client = None
        
        try:
            self.wechat_client = self.wechat_config.get_wechat_pay_client()
            if self.wechat_client:
                logger.info("微信支付客户端初始化成功")
            else:
                logger.warning("微信支付客户端初始化失败，将使用模拟模式")
        except Exception as e:
            logger.warning(f"微信支付客户端初始化失败: {str(e)}")
        
        try:
            self.alipay_client = self.alipay_config.get_alipay_client()
            if self.alipay_client:
                logger.info("支付宝客户端初始化成功")
            else:
                logger.warning("支付宝客户端初始化失败，将使用模拟模式")
        except Exception as e:
            logger.warning(f"支付宝客户端初始化失败: {str(e)}")
    
    def create_wechat_payment(self, order_no: str, amount: float, description: str, 
                             user_openid: str = None) -> PaymentResult:
        """创建微信支付订单"""
        try:
            if not self.wechat_client:
                return PaymentResult(
                    success=False,
                    message="微信支付客户端未初始化",
                    error_code="CLIENT_ERROR"
                )
            
            # 将金额转换为分
            total_fee = int(amount * 100)
            
            # 构建订单数据
            order_data = {
                'body': description,
                'out_trade_no': order_no,
                'total_fee': total_fee,
                'spbill_create_ip': '127.0.0.1',  # 实际应用中应该获取真实IP
                'notify_url': self.wechat_config.notify_url,
                'trade_type': 'NATIVE',  # 二维码支付
            }
            
            # 如果有用户openid，使用JSAPI支付
            if user_openid:
                order_data['trade_type'] = 'JSAPI'
                order_data['openid'] = user_openid
            
            # 调用微信支付API
            result = self.wechat_client.order.create(**order_data)
            
            if result.get('return_code') == 'SUCCESS' and result.get('result_code') == 'SUCCESS':
                payment_url = result.get('code_url')  # 二维码支付链接
                
                return PaymentResult(
                    success=True,
                    message="微信支付订单创建成功",
                    data=result,
                    trade_no=result.get('prepay_id'),
                    payment_url=payment_url,
                    qr_code=payment_url  # 对于微信支付，二维码内容就是payment_url
                )
            else:
                error_msg = result.get('err_code_des', result.get('return_msg', '未知错误'))
                return PaymentResult(
                    success=False,
                    message=f"微信支付订单创建失败: {error_msg}",
                    error_code=result.get('err_code', 'UNKNOWN_ERROR'),
                    data=result
                )
                
        except WeChatPayException as e:
            logger.error(f"微信支付异常: {str(e)}")
            return PaymentResult(
                success=False,
                message=f"微信支付异常: {str(e)}",
                error_code="WECHAT_PAY_ERROR"
            )
        except Exception as e:
            logger.error(f"创建微信支付订单异常: {str(e)}")
            return PaymentResult(
                success=False,
                message=f"系统异常: {str(e)}",
                error_code="SYSTEM_ERROR"
            )
    
    def create_alipay_payment(self, order_no: str, amount: float, description: str) -> PaymentResult:
        """创建支付宝支付订单"""
        try:
            if not self.alipay_client:
                return PaymentResult(
                    success=False,
                    message="支付宝客户端未初始化",
                    error_code="CLIENT_ERROR"
                )
            
            # 构建订单数据
            order_data = {
                'out_trade_no': order_no,
                'total_amount': str(amount),
                'subject': description,
                'return_url': self.alipay_config.return_url,
                'notify_url': self.alipay_config.notify_url,
            }
            
            # 调用支付宝API生成支付URL
            payment_url = self.alipay_client.api_alipay_trade_page_pay(**order_data)
            
            # 完整的支付链接
            if self.alipay_config.sandbox:
                base_url = "https://openapi.alipaydev.com/gateway.do?"
            else:
                base_url = "https://openapi.alipay.com/gateway.do?"
            
            full_payment_url = base_url + payment_url
            
            return PaymentResult(
                success=True,
                message="支付宝支付订单创建成功",
                data=order_data,
                trade_no=order_no,
                payment_url=full_payment_url
            )
            
        except Exception as e:
            logger.error(f"创建支付宝支付订单异常: {str(e)}")
            return PaymentResult(
                success=False,
                message=f"支付宝支付异常: {str(e)}",
                error_code="ALIPAY_ERROR"
            )
    
    def verify_wechat_callback(self, callback_data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """验证微信支付回调"""
        try:
            if not self.wechat_client:
                return False, {"error": "微信支付客户端未初始化"}
            
            # 验证签名
            if self.wechat_client.check_signature(callback_data):
                return True, callback_data
            else:
                return False, {"error": "签名验证失败"}
                
        except Exception as e:
            logger.error(f"验证微信支付回调异常: {str(e)}")
            return False, {"error": str(e)}
    
    def verify_alipay_callback(self, callback_data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """验证支付宝支付回调"""
        try:
            if not self.alipay_client:
                return False, {"error": "支付宝客户端未初始化"}
            
            # 验证签名
            sign = callback_data.pop('sign', None)
            sign_type = callback_data.pop('sign_type', None)
            
            if self.alipay_client.verify(callback_data, sign):
                return True, callback_data
            else:
                return False, {"error": "签名验证失败"}
                
        except Exception as e:
            logger.error(f"验证支付宝支付回调异常: {str(e)}")
            return False, {"error": str(e)}
    
    def query_wechat_payment(self, order_no: str) -> PaymentResult:
        """查询微信支付订单状态"""
        try:
            if not self.wechat_client:
                return PaymentResult(
                    success=False,
                    message="微信支付客户端未初始化",
                    error_code="CLIENT_ERROR"
                )
            
            result = self.wechat_client.order.query(out_trade_no=order_no)
            
            if result.get('return_code') == 'SUCCESS':
                trade_state = result.get('trade_state')
                
                return PaymentResult(
                    success=True,
                    message="查询成功",
                    data=result,
                    trade_no=result.get('transaction_id')
                )
            else:
                return PaymentResult(
                    success=False,
                    message=result.get('return_msg', '查询失败'),
                    error_code=result.get('err_code', 'QUERY_ERROR'),
                    data=result
                )
                
        except Exception as e:
            logger.error(f"查询微信支付订单异常: {str(e)}")
            return PaymentResult(
                success=False,
                message=f"查询异常: {str(e)}",
                error_code="SYSTEM_ERROR"
            )
    
    def query_alipay_payment(self, order_no: str) -> PaymentResult:
        """查询支付宝支付订单状态"""
        try:
            if not self.alipay_client:
                return PaymentResult(
                    success=False,
                    message="支付宝客户端未初始化",
                    error_code="CLIENT_ERROR"
                )
            
            result = self.alipay_client.api_alipay_trade_query(out_trade_no=order_no)
            
            if result.get('code') == '10000':
                return PaymentResult(
                    success=True,
                    message="查询成功",
                    data=result,
                    trade_no=result.get('trade_no')
                )
            else:
                return PaymentResult(
                    success=False,
                    message=result.get('msg', '查询失败'),
                    error_code=result.get('code', 'QUERY_ERROR'),
                    data=result
                )
                
        except Exception as e:
            logger.error(f"查询支付宝支付订单异常: {str(e)}")
            return PaymentResult(
                success=False,
                message=f"查询异常: {str(e)}",
                error_code="SYSTEM_ERROR"
            )


# 全局支付处理器实例
payment_processor = PaymentProcessor()


def get_payment_processor() -> PaymentProcessor:
    """获取全局支付处理器实例"""
    return payment_processor