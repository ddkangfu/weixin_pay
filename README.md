weixin_pay
==========

####微信支付接口(V3.3.7)类库

##一、支持接口：
此类库目前只提供了三种接口的操作类：

>-统一支付接口
>-订单查询接口
>-JSAPI 支付

##二、使用说明
1. 初始化支付类

```python
from weixin_pay.weixin_pay import UnifiedOrderPay

pay = UnifiedOrderPay("WXPAY_APPID", "WXPAY_MCHID", "WXPAY_API_KEY")
response = pay.post("body", "out_trade_no", "total_fee", "127.0.0.1", "http://www.xxxx.com/pay/notify/url/")
if (response["return_code"] == "SUCCESS" and response["result_code"] == "SUCCESS"):
    prepay_id = response["prepay_id"] #预支付ID
    code_url = response["code_url"]   #二维码链接
else:
    if response["return_code"] == "FAIL":
        pass #通信失败处理
    if response["result_code"] == "FAIL":
        passs #交易失败处理
```


