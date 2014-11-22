weixin_pay
==========

####微信支付接口(V3.3.7)类库

##一、支持接口：
此类库目前只提供了三种接口的操作类：

* 统一支付接口
* 订单查询接口
* JSAPI 支付

##二、使用说明
1. 统一支付接口
用于获取预支付ID和查询支付链接地址，可以使用二维码类库将支付链接地址生成二维码后供付款人扫描付款。

```python
from weixin_pay.weixin_pay import UnifiedOrderPay


pay = UnifiedOrderPay("WXPAY_APPID", "WXPAY_MCHID", "WXPAY_API_KEY")
response = pay.post("body", "out_trade_no", "total_fee", "127.0.0.1", "http://www.xxxx.com/pay/notify/url/")
if response and response["return_code"] == "SUCCESS" and response["result_code"] == "SUCCESS":
    prepay_id = response["prepay_id"] #预支付ID
    code_url = response["code_url"]   #二维码链接
else:
    if response["return_code"] == "FAIL":
        err_code_des = response["return_msg"]
        #通信失败处理
    if response["result_code"] == "FAIL":
        err_code = response["err_code"]
        err_code_des = pay.get_error_code_desc(response["err_code"])
        #交易失败处理
```

2. 订单查询接口
使用外部订单号查询订单的支付状态。

```python
from weixin_pay.weixin_pay import OrderQuery


pay = OrderQuery("WXPAY_APPID", "WXPAY_MCHID", "WXPAY_API_KEY")
response = wx_pay.post("out_trade_no")
if response and response["return_code"] == "SUCCESS" and response["result_code"] == "SUCCESS":
    trade_state = response["trade_state"]
    if trade_state == "SUCCESS": #支付成功
        pass #处理支付成功的情况
    else:
        pass #处理支付未完成的情况，trade_state的枚举值参见微信官方文档说明
```


