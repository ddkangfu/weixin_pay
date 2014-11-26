微信支付接口(V3.3.7)类库
==========

####weixin_pay

##支持接口：
此类库目前只提供了三种接口的操作类：

* 统一支付接口
* 订单查询接口
* JSAPI 支付

##使用方法

####1. 统一支付接口

用于获取预支付ID和查询支付链接地址，可以使用二维码类库将支付链接地址生成二维码后供付款人扫描付款。

注意：同一个out_trade_no发送不同的数据内容(如金额、body发生变化，但是out_trade_no未变)时会报OUT_TRADE_NO_USED(商户订单号重复)错误。

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

####2. 订单查询接口

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

####3. JSAPI 支付

在微信浏览器里面打开 H5 网页中执行 JS 调起支付。接口输入输出数据格式为 JSON。

注意：同一个out_trade_no发送不同的数据内容(如金额、body发生变化，但是out_trade_no未变)时会报OUT_TRADE_NO_USED(商户订单号重复)错误。

```python
from weixin_pay.weixin_pay import JsAPIOrderPay, UnifiedOrderPay


pay = JsAPIOrderPay("WXPAY_APPID", "WXPAY_MCHID", "WXPAY_API_KEY", "WXPAY_API_SECRET")

#先判断request.GET中是否有code参数，如果没有，需要使用create_oauth_url_for_code函数获取OAuth2授权地址后重定向到该地址并取得code值
oauth_url = pay.create_oauth_url_for_code("http://www.xxxx.com/pay/url/")
#重定向到oauth_url后，获得code值
code = request.GET('code', None)

if code:
    #使用code获取H5页面JsAPI所需的所有参数，类型为字典
    josn_pay_info = pay.post("body", "out_trade_no", "total_fee", "127.0.0.1", "http://www.xxxx.com/pay/notify/url/", code)
```

例如在Django模板中可以这样调用：

```javascript
    function jsApiCall(){  
        WeixinJSBridge.invoke(
            'getBrandWCPayRequest',
            {
                "appId":"{{ app_id }}",
                "timeStamp": "{{ time_stamp }}",
                "nonceStr": "{{ nonce_str }}",
                "package": "{{ package }}",
                "signType": "MD5",
                "paySign": "{{ sign }}"
            },
            function(res){
                WeixinJSBridge.log(res.err_msg);
                //以下对调用结果进行处理
            }
        );
    }

    function callpay() {
        if (typeof WeixinJSBridge == "undefined"){
            if( document.addEventListener ) {
                document.addEventListener('WeixinJSBridgeReady', jsApiCall, false);
            } else if ( document.attachEvent ) {
                document.attachEvent('WeixinJSBridgeReady', jsApiCall); 
                document.attachEvent('onWeixinJSBridgeReady', jsApiCall);
            }
        } else {
            jsApiCall();
        }
    }    
    //其余部分参见官方的JsAPI调用示例
```

##说明

目前还是开发版本，只是在公司网站上应用了一下，还不是一个完全稳定的版本，希望有能力的同学可以贡献代码，一起完善这个类库。

如有问题请联系 ddkangfu(AT)gmail.com

