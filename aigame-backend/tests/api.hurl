# 服务状态
GET {{server}}/status
HTTP 200
[Asserts]
body =="AI GAME CREATOR!"

# 用户登录
POST {{server}}/user/login
{
  username: admin,
  password: aigame-25
}
HTTP 200
[Asserts]
jsonpath "$.code" == 200

#上传附件PPT
POST {{server}}/attach?file_type=ppt
[Multipart]
files: file,1.pptx;
HTTP 200
[Asserts]
jsonpath "$.code" == 200


#查询附件PPT
GET {{server}}/attach?file_type=ppt
HTTP 200
[Asserts]
jsonpath "$.code" == 200


#查询指定附件PPT
GET {{server}}/attach?file_type=ppt&&attach_id=1
HTTP 200
[Asserts]
jsonpath "$.code" == 200
jsonpath "$.result[0].id" == 1 


#上传素材图片
POST {{server}}/attach?file_type=image&&attach_id=1
[Multipart]
files: file,1.jpg;
HTTP 200
[Asserts]
jsonpath "$.code" == 200


# 查询素材图片
GET {{server}}/attach?file_type=image
HTTP 200
[Asserts]
jsonpath "$.code" == 200


# 查询指定素材图片
GET {{server}}/attach?file_type=image&&attach_id=1
HTTP 200
[Asserts]
jsonpath "$.code" == 200
jsonpath "$.result[0].attach_id" == 1 

#上传素材音频
POST {{server}}/attach?file_type=audio&&attach_id=1
[Multipart]
files: file,1.mp3;
HTTP 200
[Asserts]
jsonpath "$.code" == 200


# 查询中间配置, module_type可选值 parse, goal, design, plan, asset
GET {{server}}/attach/module?id=1&&module_type=parse
HTTP 200
[Asserts]
jsonpath "$.code" == 200

# 查询素材音频
GET {{server}}/attach?file_type=audio
HTTP 200
[Asserts]
jsonpath "$.code" == 200


# 查询指定素材音频
GET {{server}}/attach?file_type=audio&&attach_id=1
HTTP 200
[Asserts]
jsonpath "$.code" == 200
jsonpath "$.result[0].attach_id" == 1 



# 开始生成游戏 
POST {{server}}/game/generate
{
  id:4
}
HTTP 200
[Asserts]
jsonpath "$.code" == 200

#更新PPT状态
POST {{server}}/attach/update_status
{
  id:4
  status:goal
}
HTTP 200
[Asserts]
jsonpath "$.code" == 200

#更新游戏状态
POST {{server}}/game/update_status
{
  id:4
  status:goal
}
HTTP 200
[Asserts]
jsonpath "$.code" == 200


#查询ppt截图
GET {{server}}/attach/screenshot?attach_id=1
HTTP 200
[Asserts]
jsonpath "$.code" == 200

### # chat(sse)
### POST {{server}}/chat
### HTTP 200
