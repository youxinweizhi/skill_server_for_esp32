#!/usr/bin/env python
# coding: utf-8
'''
@File   :main.py
@Author :youxinweizhi
@Date   :2020/7/16
@Github :https://github.com/youxinweizhi
'''

from microWebSrv import MicroWebSrv
from machine import Pin

#控制esp32开发板led的示例
#0 off 1 on
def set_led(n=0):
    p2=Pin(2,Pin.OUT)
    p2.value(n)
    

#更换成天猫精灵技能认证文件，key:文件名  value:文件内容（一个技能一个认证文件）
zhengshu={}
zhengshu['url']='75c463e1d56ca9ca250c232bb83c5ffd.txt'
zhengshu['key']='Jfc4Z4Ur15JwUBuvUQD5wg7Nu8+l+HscqYlfofbyJdZpUywKEiamk2BzVIb1KIjo'


@MicroWebSrv.route('/',"GET")
def auth(httpClient, httpResponse) :
    httpResponse.WriteResponseOk( headers = None,
                                contentType = "text/html",
                                contentCharset = "UTF-8",
                                content = '<p style="color: #00a0e9;font-size: 32px">skill_server_for_esp32</p>' )

@MicroWebSrv.route('/aligenie/{}'.format(zhengshu['url']),"GET")
def auth(httpClient, httpResponse) :
    httpResponse.WriteResponseOk( headers = None,
                                contentType = "text/html",
                                contentCharset = "UTF-8",
                                content = zhengshu['key'] )


@MicroWebSrv.route('/skill/',"POST")
def skill(httpClient, httpResponse) :
    data=httpClient.ReadRequestContentAsJSON()
    print(data)
    #固定响应格式
    RETURN_DATA = {
        "returnCode": "0","returnErrorSolution": "","returnMessage": "","returnValue":{"reply": "","resultType": "RESULT","actions":[{"name": "audioPlayGenieSource","properties": {"audioGenieId": "123"}}],"properties": {},
        "executeCode": "SUCCESS",
        "msgInfo": ""
    }}

    if data['skillName']=="小助手":
        if data['intentName']=="小助手":
            if data['slotEntities'][0]['originalValue']=="打开":
                set_led(1)
                RETURN_DATA['returnValue']['reply'] = "打开指令已执行"
            elif data['slotEntities'][0]['originalValue']=="关闭":
                set_led(0)
                RETURN_DATA['returnValue']['reply'] = "关闭指令已执行"

    else:
        RETURN_DATA['returnValue']['reply'] = "技能不存在，或暂时无法查询！"

    httpResponse.WriteResponseJSONOk(obj=RETURN_DATA)



if __name__ == '__main__':
  srv = MicroWebSrv(webPath='/')
  srv.Start(threaded=True)
