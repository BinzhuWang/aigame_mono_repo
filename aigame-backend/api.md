---
title: api
language_tabs:
  - shell: Shell
  - http: HTTP
  - javascript: JavaScript
  - ruby: Ruby
  - python: Python
  - php: PHP
  - java: Java
  - go: Go
toc_footers: []
includes: []
search: true
code_clipboard: true
highlight_theme: darkula
headingLevel: 2
generator: "@tarslib/widdershins v4.0.30"

---

# api

Base URLs:

# Authentication

# Default

## GET 状态测试

GET /status

> 返回示例

> 200 Response

```json
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

## POST 用户登录

POST /user/login

> Body 请求参数

```json
{
  "username": "string",
  "password": "string"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|object| 否 |none|
|» username|body|string| 是 |none|
|» password|body|string| 是 |none|

> 返回示例

> 200 Response

```json
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

## POST 文件上传

POST /attach

> Body 请求参数

```yaml
files: file:///Users/dfine/Documents/nnk_daemon/test/ppt.pptx

```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|file_type|query|string| 否 |none|
|Authorization|header|string| 否 |none|
|body|body|object| 否 |none|
|» files|body|string(binary)| 否 |none|

> 返回示例

> 200 Response

```json
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

## GET 文件查询

GET /attach

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|file_type|query|string| 是 |none|
|attach_id|query|number| 否 |可选，不填则为查询所有|
|Authorization|header|string| 否 |none|

> 返回示例

> 200 Response

```json
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

## DELETE PPT删除

DELETE /attach

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|file_type|query|string| 是 |ppt/image/audio|
|id|query|number| 否 |可选，不填则为查询所有|
|Authorization|header|string| 否 |none|

> 返回示例

> 200 Response

```json
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

## POST 聊天

POST /chat/code

> Body 请求参数

```json
{
  "game_id": 0,
  "content": [
    {
      "feedback_type": "sandbox_debug",
      "content": "string"
    }
  ]
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|Authorization|header|string| 是 |none|
|body|body|object| 否 |none|
|» game_id|body|number| 是 |游戏id|
|» content|body|[object]| 是 |none|
|»» feedback_type|body|any| 是 |反馈类型|
|»»» *anonymous*|body|string| 否 |none|
|»»» *anonymous*|body|string| 否 |none|
|»»» *anonymous*|body|string| 否 |none|
|»» content|body|string| 是 |反馈内容|

> 返回示例

> 200 Response

```json
{
  "code": 0,
  "msg": "string",
  "result": {
    "code": "string"
  }
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||none|
|» msg|string|true|none||none|
|» result|object|true|none||none|
|»» code|string|true|none||none|

## GET 游戏查询

GET /game/query

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|attach_id|query|number| 否 |ppt id，不加参数则查询所有|
|Authorization|header|string| 否 |none|

> 返回示例

> 200 Response

```json
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

## GET PPT截图查询

GET /attach/screenshot

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|attach_id|query|string| 否 |none|
|Authorization|header|string| 否 |none|

> 返回示例

> 200 Response

```json
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

## GET 游戏生成模块查询

GET /game/module

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|query|number| 否 |ID 编号|
|module_type|query|string| 否 |可选值:goal,plan,code|
|Authorization|header|string| 否 |none|

> 返回示例

> 200 Response

```json
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

## POST 游戏生成模块修改

POST /game/module

修改游戏的module json。query传递id和module_type。body直接发送要修改的json即可。

> Body 请求参数

```json
[
  {
    "end_page": 10,
    "evidence": [
      {
        "image_summary": "Digital illustration of a soccer goal on a field and multiple soccer players in action poses",
        "page": 2,
        "text_excerpt": "Warm up, warm up, everybody warm up. There are 8 soccer balls. Click to have one ball bounce in..."
      },
      {
        "image_summary": "Animation of a martial arts character performing a high kick",
        "page": 3,
        "text_excerpt": "Can you kick like her? Kick four times."
      },
      {
        "image_summary": "Cartoon boy jumping over two tires",
        "page": 4,
        "text_excerpt": "Can you jump like him? Jump over six tyres."
      },
      {
        "image_summary": "Cartoon girl in a playful pose with vibrant colors",
        "page": 5,
        "text_excerpt": "Can you hop like her? Hop fives times."
      },
      {
        "image_summary": "Cartoon boy catching a ball with playful background",
        "page": 6,
        "text_excerpt": "Can you catch like him? Catch a ball three times."
      },
      {
        "image_summary": "Boy in cricket playing pose",
        "page": 7,
        "text_excerpt": "Can you throw like him? Throw the ball twice."
      },
      {
        "image_summary": "Cartoon boy joyfully jumping rope",
        "page": 8,
        "text_excerpt": "Can you skip like him? Skip eight times."
      },
      {
        "image_summary": "Cartoon style illustration of a girl running",
        "page": 9,
        "text_excerpt": "Can you run like her? Run on the spot for 10 counts."
      },
      {
        "image_summary": "Child in climbing pose on a colorful background",
        "page": 10,
        "text_excerpt": "Can you climb like her? Climb up one rock."
      }
    ],
    "game_goal": "Design an interactive soccer warm-up game where learners mimic soccer actions such as kicking, jumping, hopping, catching, throwing, skipping, running, and climbing. The goal is to develop physical agility and coordination through engaging pretend play.",
    "module_id": 0,
    "start_page": 2
  },
  {
    "end_page": 21,
    "evidence": [
      {
        "image_summary": "",
        "page": 11,
        "text_excerpt": "Follow the leader. The learners take turns choosing a number around the body..."
      },
      {
        "image_summary": "",
        "page": 12,
        "text_excerpt": "Follow the leader. ...And pick up your pencil."
      },
      {
        "image_summary": "Educational illustration depicting human body parts with labels",
        "page": 13,
        "text_excerpt": "The learners need to figure out what they must touch."
      },
      {
        "image_summary": "Children's illustration, labeled body parts",
        "page": 14,
        "text_excerpt": "And skip around three times on the spot."
      },
      {
        "image_summary": "Illustration emphasizing human anatomy with labels",
        "page": 15,
        "text_excerpt": "Hold it and walk around in a circle."
      },
      {
        "image_summary": "Cartoon boy with labeled body parts for educational purposes",
        "page": 16,
        "text_excerpt": "And criss cross your legs four times."
      },
      {
        "image_summary": "Body parts illustration for educational learning",
        "page": 17,
        "text_excerpt": "And do seven jumping jacks."
      },
      {
        "image_summary": "Illustration with labeled human body parts",
        "page": 18,
        "text_excerpt": "And touch your toes, then put your hands on your hips."
      },
      {
        "image_summary": "Educational illustration of human body parts",
        "page": 19,
        "text_excerpt": "And stick out your tongue, then bend to your left side."
      },
      {
        "image_summary": "Cartoon-style educational illustration",
        "page": 20,
        "text_excerpt": "And nod your head twice, then sit back down."
      },
      {
        "image_summary": "Body parts educational illustration",
        "page": 21,
        "text_excerpt": "And touch your shoulders, then do a little dance."
      }
    ],
    "game_goal": "Conduct a sequential game 'Follow the Leader' where learners follow physical instructions related to body part actions to promote body awareness and coordination.",
    "module_id": 1,
    "start_page": 11
  }
]
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|query|number| 否 |ID 编号|
|module_type|query|string| 否 |可选值:goal,plan,code|
|Authorization|header|string| 否 |none|
|body|body|array[object]| 否 |none|

> 返回示例

> 200 Response

```json
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

## POST 生成游戏

POST /game/generate

生成游戏，会自动根据当前game的状态执行下一步。如果已经生成了code，则重新生成。

> Body 请求参数

```json
{
  "id": 0
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|Authorization|header|string| 否 |none|
|body|body|object| 否 |none|
|» id|body|number| 是 |ID 编号|

> 返回示例

> 200 Response

```json
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

## GET PPT处理模块查询

GET /attach/module

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|query|number| 否 |ID 编号|
|module_type|query|string| 否 |目前可选值只有parse|
|Authorization|header|string| 否 |none|

> 返回示例

> 200 Response

```json
{
  "code": 200,
  "msg": "query module json finished",
  "result": {
    "code": 200,
    "message": "parse ppt finished",
    "res": {
      "document_info": [
        {
          "audios": [],
          "images": [],
          "notes": "",
          "page": 1,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_1.png",
          "text": [],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image depicts a digital illustration of a soccer goal on a field. The goal is centrally positioned, featuring a white frame and a net with a grid pattern. The field is shown with a vibrant green color, marked with white lines indicating the penalty area and the penalty spot in front of the goal. The background is a gradient transitioning from dark blue to black, suggesting a night setting, possibly under stadium lights. The composition is symmetrical, focusing on the goal, and the style is clean and modern, suitable for use in sports-related digital media or games.",
              "height": 570.3156692913386,
              "left": 29.690236220472443,
              "ori_height": 1211,
              "ori_width": 2422,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_2_3.png",
              "tag": "Soccer Goal, Green Field, Night Setting",
              "top": -62.526299212598424,
              "width": 717.8088976377953
            },
            {
              "desp": "The image depicts an illustrated character of a young soccer player in mid-action. The player is wearing a maroon and light blue soccer uniform, consisting of a short-sleeved jersey and matching shorts. The jersey has light blue sleeves and a maroon body. The player is also wearing maroon knee-high socks and bright green soccer cleats with studs. The character is in a dynamic pose, balancing a soccer ball on their right knee, suggesting they are juggling or controlling the ball. The soccer ball is classic in design, featuring a pattern of black pentagons and white hexagons. The player's hair is brown and styled in a casual, slightly tousled manner. The background is plain, emphasizing the character and their action.",
              "height": 73.1076377952756,
              "left": 980.571496062992,
              "ori_height": 1920,
              "ori_width": 1920,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_2_5.png",
              "tag": "Soccer Player, Dynamic Pose, Maroon Uniform",
              "top": 59.219212598425194,
              "width": 76.4307874015748
            },
            {
              "desp": "The image depicts an illustrated character of a young soccer player in mid-action. The player is wearing a maroon and light blue soccer uniform, consisting of a short-sleeved jersey and shorts. The jersey features light blue sleeves and a maroon body, while the shorts are entirely maroon. The player is also wearing maroon knee-high socks and bright green soccer cleats with studs. The character is posed with one knee raised, balancing a classic black and white soccer ball on the thigh. The illustration style is clean and cartoonish, with simple lines and flat colors, suitable for animation or digital media use.",
              "height": 73.1076377952756,
              "left": 1073.8611023622047,
              "ori_height": 1920,
              "ori_width": 1920,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_2_6.png",
              "tag": "Soccer Player, Cartoon Style, Maroon Uniform",
              "top": 59.21913385826772,
              "width": 76.4307874015748
            },
            {
              "desp": "The image depicts an animated character of a young soccer player in mid-action. The player is wearing a maroon and light blue soccer uniform, consisting of a short-sleeved jersey and shorts. The jersey has light blue sleeves and a maroon body, while the shorts are entirely maroon. The player is also wearing maroon knee-high socks and bright green soccer cleats with white studs. The character is posed with one knee raised, balancing a soccer ball on the knee. The soccer ball is designed with a classic black and white hexagonal pattern. The overall style of the image is cartoonish and colorful, suitable for animation or digital media related to sports or children's content.",
              "height": 73.1076377952756,
              "left": 1167.1507086614174,
              "ori_height": 1920,
              "ori_width": 1920,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_2_7.png",
              "tag": "Soccer Player, Cartoon Style, Sports Animation",
              "top": 59.219055118110234,
              "width": 76.4307874015748
            },
            {
              "desp": "The image depicts an illustration of a young soccer player in mid-action, performing a juggling move with a soccer ball. The player is wearing a sports uniform consisting of a maroon jersey with light blue sleeves, matching maroon shorts, and maroon knee-high socks. The player is also wearing bright green soccer cleats with studs. The soccer ball is depicted in mid-air, just above the player's knee, suggesting a dynamic motion. The overall style of the illustration is cartoon-like, with clean lines and solid colors, suitable for use in animation or educational materials related to sports.",
              "height": 73.1076377952756,
              "left": 1257.228818897638,
              "ori_height": 1920,
              "ori_width": 1920,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_2_8.png",
              "tag": "Soccer Player, Juggling Move, Cartoon Illustration",
              "top": 59.219055118110234,
              "width": 76.4307874015748
            },
            {
              "desp": "The image depicts an illustrated character of a young soccer player in mid-action. The character is wearing a sports uniform consisting of a maroon jersey with light blue sleeves, matching maroon shorts, and maroon knee-high socks. The player is poised with one knee raised, balancing a classic black and white soccer ball on the knee. The character's footwear includes bright green soccer cleats with visible studs. The illustration style is clean and cartoon-like, suitable for animation or educational content related to sports.",
              "height": 73.1076377952756,
              "left": 993.0726771653544,
              "ori_height": 1920,
              "ori_width": 1920,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_2_9.png",
              "tag": "Soccer Player, Sports Uniform, Cartoon Illustration",
              "top": 233.30220472440945,
              "width": 76.4307874015748
            },
            {
              "desp": "The image depicts an illustrated character of a young soccer player in mid-action, performing a juggling move with a soccer ball. The player is wearing a sports uniform consisting of a maroon jersey with light blue sleeves, matching maroon shorts, and maroon knee-high socks. The character's shoes are bright green soccer cleats with visible studs. The soccer ball is designed with a classic black and white hexagonal pattern and is positioned near the player's raised knee, suggesting a juggling or dribbling motion. The overall style is cartoonish and colorful, suitable for animation or digital media aimed at a younger audience.",
              "height": 73.1076377952756,
              "left": 1073.8611023622047,
              "ori_height": 1920,
              "ori_width": 1920,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_2_10.png",
              "tag": "Soccer Player, Juggling Move, Cartoon Style",
              "top": 233.30212598425197,
              "width": 76.4307874015748
            },
            {
              "desp": "The image depicts an illustration of a young soccer player in mid-action, performing a juggling move with a soccer ball. The player is wearing a sports uniform consisting of a maroon jersey with light blue sleeves, matching maroon shorts, and maroon knee-high socks. The player is also wearing bright green soccer cleats with studs, suitable for playing on grass. The soccer ball is depicted in mid-air, featuring a classic black and white hexagonal pattern. The player's posture suggests they are balancing the ball on their knee, with one leg raised and both arms slightly bent at the elbows, indicating movement and coordination. The overall style of the illustration is cartoon-like, with bold colors and clean lines.",
              "height": 73.1076377952756,
              "left": 1167.1507086614174,
              "ori_height": 1920,
              "ori_width": 1920,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_2_11.png",
              "tag": "Soccer Player, Juggling Move, Cartoon Illustration",
              "top": 233.7427559055118,
              "width": 76.4307874015748
            },
            {
              "desp": "The image depicts an illustrated character of a young soccer player in mid-action. The player is wearing a sports uniform consisting of a maroon jersey with light blue sleeves, matching maroon shorts, and maroon knee-high socks. The character is poised with one knee raised, balancing a classic black and white soccer ball on the knee. The player is also wearing bright green soccer cleats with visible studs. The illustration style is simple and cartoon-like, with clean lines and solid colors, suitable for use in animation or educational materials related to sports.",
              "height": 73.1076377952756,
              "left": 1257.2287401574804,
              "ori_height": 1920,
              "ori_width": 1920,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_2_12.png",
              "tag": "Soccer Player, Sports Uniform, Cartoon Illustration",
              "top": 231.17133858267715,
              "width": 76.4307874015748
            }
          ],
          "notes": null,
          "page": 2,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_2.png",
          "text": [
            "Warm up, warm up, everybody warm up.",
            "There are 8 soccer balls. Click to have one ball bounce in.  \nClick on the ball to be directed to an action slide. When you return to this slide, repeat the clicks.\nOnce 8 balls have been actioned, click the arrow to continue. ",
            "",
            ""
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image depicts a digital illustration of a soccer goal on a field. The goal is centrally positioned and features a white frame with a net that is neatly divided into a grid pattern. The field is a vibrant green with clearly marked white lines, including the penalty arc and the penalty spot in front of the goal. The background is a dark gradient, transitioning from black at the top to a deep blue behind the goal, suggesting a night setting. The composition is symmetrical, focusing on the goal, and the lighting creates a subtle spotlight effect on the field, enhancing the centrality of the goal. This image could be used as a background or asset in a sports-related digital media project, such as a video game or animation.",
              "height": 570.3156692913386,
              "left": 29.690236220472443,
              "ori_height": 1211,
              "ori_width": 2422,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_3_3.png",
              "tag": "Soccer Goal, Night Setting, Digital Illustration",
              "top": -62.526299212598424,
              "width": 717.8088976377953
            },
            {
              "desp": "The image depicts a cartoon-style illustration of a martial artist performing a dynamic jumping kick. The character is wearing a traditional white karate gi with a black belt, indicating a high level of proficiency. The gi has long sleeves and pants, with the belt tied around the waist. The character's arms are bent with fists clenched, suggesting readiness and focus. The left leg is extended forward in a kicking motion, while the right leg is bent backward, contributing to the sense of movement and action. The character's hair is styled in a neat bun, secured with a pink hair tie. The overall style is clean and vibrant, suitable for animation or digital media focused on martial arts themes.",
              "height": 311.81102362204723,
              "left": 167.4448818897638,
              "ori_height": 1639,
              "ori_width": 2416,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_3_4.png",
              "tag": "Martial Artist, Jumping Kick, Karate Gi",
              "top": 78.48929133858267,
              "width": 459.5121259842519
            }
          ],
          "notes": null,
          "page": 3,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_3.png",
          "text": [
            "Warm up, warm up, everybody warm up.",
            "Read the question / action to the learners.\nThey pretend to be doing the action. \nClick Back to main slide to continue. ",
            "",
            "Can you kick like her? Kick four times.",
            "Back to main slide"
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image depicts a digital illustration of a soccer goal on a field. The goal is centrally positioned and features a white frame with a net composed of a grid pattern. The field is shown with a vibrant green surface, marked with white lines indicating the penalty area and the center circle. The perspective is from the viewpoint of a player approaching the goal, emphasizing the goal's prominence. The background is a dark gradient, transitioning from black at the top to a subtle blue near the goal, suggesting a stadium setting under artificial lighting. The overall style is clean and modern, suitable for use in sports-related digital media or UI design, such as a game interface or sports app.",
              "height": 570.3156692913386,
              "left": 29.690236220472443,
              "ori_height": 1211,
              "ori_width": 2422,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_4_3.png",
              "tag": "Soccer Goal, Digital Illustration, Sports UI Design",
              "top": -62.526299212598424,
              "width": 717.8088976377953
            },
            {
              "desp": "The image is a cartoon-style illustration featuring a young boy energetically jumping over two tires. The boy has short brown hair and is wearing a bright blue t-shirt, brown shorts, and red shoes. His expression is cheerful and animated, suggesting excitement or playfulness. The two tires are positioned on the ground, slightly apart from each other, and are depicted in a realistic style with visible treads. The background is transparent, indicating that this image could be used as an animation asset or in digital media where the character and objects can be placed over different backgrounds. The overall style is colorful and playful, suitable for children's content or educational materials.",
              "height": 311.81102362204723,
              "left": 302.3056692913386,
              "ori_height": 1651,
              "ori_width": 1659,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_4_4.png",
              "tag": "Cartoon Boy, Jumping Tires, Children's Illustration",
              "top": 119.14551181102362,
              "width": 177.69433070866145
            }
          ],
          "notes": null,
          "page": 4,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_4.png",
          "text": [
            "Warm up, warm up, everybody warm up.",
            "Read the question / action to the learners.\nThey pretend to be doing the action. \nClick Back to main slide to continue. ",
            "",
            "Can you jump like him? Jump over six tyres.",
            "Back to main slide"
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image depicts a digital illustration of a soccer goal set against a dark background, likely intended for use in sports-related digital media or a video game. The scene is centered on a standard soccer goal with a white frame and net, positioned on a green soccer field. The field is marked with white lines, including the penalty arc and spot, indicating the area in front of the goal. The perspective is from the center of the field, directly facing the goal, creating a symmetrical composition. The lighting is focused on the goal and the immediate area of the field, with the background fading into darkness, suggesting a spotlight effect often used in sports graphics to emphasize the goal area.",
              "height": 570.3156692913386,
              "left": 29.690236220472443,
              "ori_height": 1211,
              "ori_width": 2422,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_5_3.png",
              "tag": "Soccer Goal, Digital Illustration, Spotlight Effect",
              "top": -62.526299212598424,
              "width": 717.8088976377953
            },
            {
              "desp": "The image features a cartoon-style illustration of a young girl with a cheerful expression. She has bright orange hair styled in a bob cut with a small hair tuft on top. Her eyes are large and blue, adding to her animated appearance. She is wearing a yellow shirt with a blue bow at the collar and a short red skirt. Her outfit is completed with purple shoes and matching socks. The girl is depicted in a playful pose, standing on one leg with her arms outstretched to the sides, suggesting a sense of balance or dance. The background is transparent, making the character suitable for use as an animation asset or in digital media where she can be placed over various backgrounds.",
              "height": 311.81102362204723,
              "left": 323.2340157480315,
              "ori_height": 1651,
              "ori_width": 1659,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_5_4.png",
              "tag": "Cartoon Girl, Orange Hair, Playful Pose",
              "top": 171.93897637795277,
              "width": 156.7659842519685
            }
          ],
          "notes": null,
          "page": 5,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_5.png",
          "text": [
            "Warm up, warm up, everybody warm up.",
            "Read the question / action to the learners.\nThey pretend to be doing the action. \nClick Back to main slide to continue. ",
            "",
            "Can you hop like her? Hop fives times.",
            "Back to main slide"
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image depicts a stylized representation of a soccer field focusing on the goal area. The foreground features a well-defined, green grass pitch with white markings indicating the penalty box and the goal area. The central focus is on the soccer goal, which is prominently displayed with a white frame and netting. The net is detailed with a grid pattern, and the goalposts are positioned centrally within the image. The background is a gradient transitioning from dark blue to black, suggesting a night setting or an indoor stadium environment. The composition is symmetrical, emphasizing the goal as the main element, suitable for use in sports-related digital media or as a background for soccer-themed applications.",
              "height": 570.3156692913386,
              "left": 29.690236220472443,
              "ori_height": 1211,
              "ori_width": 2422,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_6_3.png",
              "tag": "Soccer Field, Goal Area, Night Setting",
              "top": -62.526299212598424,
              "width": 717.8088976377953
            },
            {
              "desp": "The image depicts a cartoon-style illustration of a young boy standing on a small patch of grass. He is wearing a blue baseball cap with an orange underside, a yellow and white striped t-shirt, dark blue shorts, and blue sneakers with green soles. The boy is positioned as if he is about to catch a red cricket ball, which is shown in mid-air with a motion line indicating its trajectory. The grass patch is oval-shaped with a few small flowers and leaves scattered on it, adding a playful outdoor setting to the scene.",
              "height": 311.81102362204723,
              "left": 122.7903937007874,
              "ori_height": 1639,
              "ori_width": 2416,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_6_4.png",
              "tag": "Cartoon Boy, Cricket Ball, Outdoor Scene",
              "top": 137.1,
              "width": 459.51141732283463
            }
          ],
          "notes": null,
          "page": 6,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_6.png",
          "text": [
            "Warm up, warm up, everybody warm up.",
            "Read the question / action to the learners.\nThey pretend to be doing the action. \nClick Back to main slide to continue. ",
            "",
            "Can you catch like him? Catch a ball three times.",
            "Back to main slide"
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image depicts a digital illustration of a soccer goal set against a dark background, which creates a dramatic contrast. The goal is centrally positioned and features a white frame with a net composed of evenly spaced squares. The netting is detailed with a subtle gradient, suggesting depth and dimension. In front of the goal, the foreground shows a section of a soccer field with a vibrant green color and white markings, including the penalty spot and part of the penalty arc. The field is illuminated, highlighting the goal area, while the surrounding area fades into darkness, emphasizing the focus on the goal itself. This image could be used as a background or asset in sports-related digital media or animation.",
              "height": 570.3156692913386,
              "left": 29.690236220472443,
              "ori_height": 1211,
              "ori_width": 2422,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_7_3.png",
              "tag": "Soccer Goal, Dark Background, Soccer Field",
              "top": -62.526299212598424,
              "width": 717.8088976377953
            },
            {
              "desp": "The image depicts a cartoon-style illustration of a young boy engaged in a playful activity. He is positioned on a small patch of grass, which is adorned with simple floral designs. The boy is wearing a dark navy blue t-shirt with a bold yellow geometric design on the chest. His attire includes light blue denim shorts with rolled-up cuffs and visible yellow stitching details. He is also wearing white socks and blue sneakers with yellow laces and soles. The boy is in a dynamic pose, with his arms extended as if he is about to catch or throw a red cricket ball that is in mid-air in front of him. The illustration is colorful and vibrant, with a playful and energetic theme suitable for animation or children's media.",
              "height": 311.81102362204723,
              "left": 160.1420472440945,
              "ori_height": 1639,
              "ori_width": 2416,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_7_4.png",
              "tag": "Cartoon Boy, Playful Activity, Cricket Ball, Colorful Illustration",
              "top": 159.41346456692912,
              "width": 456.9052755905512
            }
          ],
          "notes": null,
          "page": 7,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_7.png",
          "text": [
            "Warm up, warm up, everybody warm up.",
            "Read the question / action to the learners.\nThey pretend to be doing the action. \nClick Back to main slide to continue. ",
            "",
            "Can you throw like him? Throw the ball twice.",
            "Back to main slide"
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image depicts a digital illustration of a soccer goal on a field. The goal is centrally positioned and features a white frame with a net composed of evenly spaced horizontal and vertical lines, creating a grid pattern. The background is a dark gradient transitioning from black at the top to a deep blue, suggesting a nighttime or indoor setting. The soccer field is shown in a vibrant green color, with white markings indicating the penalty area, the penalty spot, and the arc of the penalty box. The perspective is from the center of the field facing the goal, emphasizing the goal's structure and the field's layout. The image is likely designed for use in sports-related digital media, such as a game or animation asset, focusing on the goal area.",
              "height": 570.3156692913386,
              "left": 29.690236220472443,
              "ori_height": 1211,
              "ori_width": 2422,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_8_3.png",
              "tag": "Soccer Goal, Digital Illustration, Nighttime Setting",
              "top": -62.526299212598424,
              "width": 717.8088976377953
            },
            {
              "desp": "The image is a cartoon-style illustration of a cheerful young boy jumping rope. The boy has curly brown hair and is depicted with a wide, joyful smile, with his eyes closed in delight. He is wearing a green sleeveless shirt and blue pants, along with brown shoes. The jump rope is orange with blue handles, and the boy is holding it in both hands, mid-jump, with his legs spread apart in a playful manner. The illustration has a bright and lively color palette, emphasizing a sense of fun and energy, suitable for children's media or educational content.",
              "height": 311.81102362204723,
              "left": 217.6596850393701,
              "ori_height": 1092,
              "ori_width": 1092,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_8_4.png",
              "tag": "Cartoon Boy, Jump Rope, Children's Illustration",
              "top": 119.14551181102362,
              "width": 311.81102362204723
            }
          ],
          "notes": null,
          "page": 8,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_8.png",
          "text": [
            "Warm up, warm up, everybody warm up.",
            "Read the question / action to the learners.\nThey pretend to be doing the action. \nClick Back to main slide to continue. ",
            "",
            "Can you skip like him? Skip eight times.",
            "Back to main slide"
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image depicts a digital illustration of a soccer goal set against a dark background. The goal is centrally positioned, featuring a white frame and a net composed of evenly spaced squares. The netting is detailed with a subtle gradient, suggesting depth and dimension. In front of the goal is a section of a soccer field, characterized by a vibrant green color and marked with white lines indicating the penalty area and the penalty spot. The field lines include the arc of the penalty area and the center circle, providing context for the goal's placement within a soccer field. The overall composition is simple and focused, with the goal and field elements prominently displayed against the stark black background, which enhances the contrast and visibility of the soccer elements. This image could be used in sports-related digital media, such as a game interface or animation asset.",
              "height": 570.3156692913386,
              "left": 29.690236220472443,
              "ori_height": 1211,
              "ori_width": 2422,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_9_3.png",
              "tag": "Soccer Goal, Penalty Area, Digital Illustration",
              "top": -62.526299212598424,
              "width": 717.8088976377953
            },
            {
              "desp": "The image is a cartoon-style illustration of a young girl in motion, depicted as if she is running or skipping. She has bright orange hair styled in a high ponytail, secured with a purple hair tie. Her facial expression is joyful, with a wide smile showing her teeth and her eyes looking forward. The girl is wearing a pink t-shirt with a darker pink outline, purple shorts, and blue sneakers with white soles. Her socks are white and visible above her shoes. The illustration includes motion lines near her feet, emphasizing her movement. The overall style is vibrant and playful, suitable for use in children's animation or educational content. The background is transparent, allowing for easy integration into various digital media.",
              "height": 311.81102362204723,
              "left": 266.5249606299213,
              "ori_height": 1649,
              "ori_width": 2361,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_9_4.png",
              "tag": "Cartoon Girl, Running, Vibrant Illustration",
              "top": 119.14551181102362,
              "width": 244.13937007874017
            }
          ],
          "notes": null,
          "page": 9,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_9.png",
          "text": [
            "Warm up, warm up, everybody warm up.",
            "Read the question / action to the learners.\nThey pretend to be doing the action. \nClick Back to main slide to continue. ",
            "",
            "Can you run like her? Run on the spot for 10 counts.",
            "Back to main slide"
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image depicts a stylized soccer field with a focus on the goal area. The foreground features a green grass pitch with white markings, including the penalty arc and spot, indicating the area directly in front of the goal. The goal itself is centrally positioned, with a white frame and netting, creating a grid pattern. The background is a dark gradient transitioning from black at the top to a deep blue near the goal, suggesting a night-time setting or an indoor stadium environment. The composition is symmetrical, emphasizing the goal as the central element, and the lighting effect adds depth and focus to the scene. This image could be used in digital media related to sports, such as a video game or animation asset, where the goal area is a key visual component.",
              "height": 570.3156692913386,
              "left": 29.690236220472443,
              "ori_height": 1211,
              "ori_width": 2422,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_10_3.png",
              "tag": "Soccer Field, Goal Area, Night Setting",
              "top": -62.526299212598424,
              "width": 717.8088976377953
            },
            {
              "desp": "The image depicts an animated character of a young child from a rear view, appearing to be in a climbing or reaching pose. The child is wearing a colorful, segmented cap with red, blue, and yellow sections. The child has brown hair styled in a single braid that extends down the back. They are dressed in a white t-shirt and light blue shorts. The child is also wearing bright green sneakers with white soles and yellow socks. The character's arms are raised, and one knee is bent, suggesting movement or an action-oriented pose. The illustration style is cartoonish, with bold outlines and vibrant colors, suitable for use in children's media or educational animations.",
              "height": 311.81102362204723,
              "left": 277.38818897637793,
              "ori_height": 892,
              "ori_width": 1185,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_10_5.png",
              "tag": "Animated Character, Colorful Cap, Cartoon Style",
              "top": 105.47763779527558,
              "width": 207.95661417322836
            }
          ],
          "notes": null,
          "page": 10,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_10.png",
          "text": [
            "Warm up, warm up, everybody warm up.",
            "Read the question / action to the learners.\nThey pretend to be doing the action. \nClick Back to main slide to continue. ",
            "",
            "Back to main slide",
            "Can you climb like her? Climb up one rock."
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [],
          "notes": null,
          "page": 11,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_11.png",
          "text": [
            "Follow the leader.",
            "The learners take turns choosing a number around the body. Click on the number chosen to be directed to a slide with an action.  \nContinue playing until all numbers have been selected and the children are able to follow all the instructions.  \n\nClick the arrow to end.\nThis is the last slide.",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            ""
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [],
          "notes": null,
          "page": 12,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_12.png",
          "text": [
            "Follow the leader.",
            "The learners need to figure out what they must touch. Read the added instruction to them. They wait until the instructions have been read and then they complete them.\nClick Back to main slide to continue.",
            "1",
            "Back to main slide",
            "And pick up your pencil.."
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image is an educational illustration designed to teach children about different body parts. It features a cartoon-style depiction of a young boy standing with arms outstretched, wearing red shorts. The boy has brown hair, large blue eyes, and a cheerful expression. Surrounding the boy are labeled boxes, each containing an illustration of a specific body part. \n\n- At the top, a blue banner with red accents displays the title \"BODY PARTS\" in bold white letters.\n- On the left side, boxes labeled \"EYE,\" \"NOSE,\" \"ARM,\" \"LEG,\" and \"KNEE\" are connected to the corresponding parts on the boy's body with red lines.\n- On the right side, boxes labeled \"HEAD,\" \"EAR,\" \"MOUTH,\" \"HAND,\" and \"FOOT\" similarly connect to the respective body parts.\n- Each box contains a simple illustration of the body part, matching the cartoon style of the central figure.\n\nThe image uses bright colors and clear labeling to make it engaging and easy for children to understand and identify different body parts.",
              "height": 180.49330708661415,
              "left": 414.38732283464566,
              "ori_height": 1125,
              "ori_width": 1125,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_13_0.png",
              "tag": "Body Parts, Educational Illustration, Cartoon Boy",
              "top": 182.74346456692913,
              "width": 175.5828346456693
            }
          ],
          "notes": null,
          "page": 13,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_13.png",
          "text": [
            "Follow the leader.",
            "",
            "",
            "nose",
            "2",
            "The learners need to figure out what they must touch. Read the added instruction to them. They wait until the instructions have been read and then they complete them.\nClick Back to main slide to continue.",
            "Back to main slide",
            "And put your right hand behind your back.."
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image is an educational illustration designed to teach children about human body parts. It features a cartoon-style depiction of a young boy with short dark hair, standing with arms outstretched. The boy is wearing red shorts with a white drawstring. Surrounding the boy are labeled boxes, each containing an illustration of a specific body part. These boxes are connected to the corresponding parts on the boy's body with red lines. \n\nThe body parts identified include:\n\n- **Head**: Illustrated with a smaller version of the boy's face.\n- **Eye**: A large, cartoon-style eye with eyelashes.\n- **Ear**: A simplified illustration of an ear.\n- **Nose**: A basic depiction of a nose.\n- **Mouth**: A smiling mouth showing teeth.\n- **Arm**: A simplified illustration of an arm.\n- **Hand**: A cartoon-style hand with fingers spread.\n- **Leg**: A depiction of legs wearing shorts.\n- **Knee**: A basic illustration of a knee.\n- **Foot**: A simplified depiction of a foot.\n\nAt the top of the image, there is a banner with a blue background and orange ribbon ends, containing the text \"BODY PARTS\" in bold white letters. The overall style is colorful and playful, suitable for educational purposes aimed at young children.",
              "height": 186.6892125984252,
              "left": 405.5370866141732,
              "ori_height": 1125,
              "ori_width": 1125,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_14_0.png",
              "tag": "Human Body Parts, Educational Illustration, Cartoon Style",
              "top": 177.91425196850395,
              "width": 185.5076377952756
            }
          ],
          "notes": null,
          "page": 14,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_14.png",
          "text": [
            "Follow the leader.",
            "",
            "",
            "left arm",
            "3",
            "The learners need to figure out what they must touch. Read the added instruction to them. They wait until the instructions have been read and then they complete them.\nClick Back to main slide to continue.",
            "Back to main slide",
            "And skip around three times on the spot."
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image is an educational illustration designed to teach children about different body parts. It features a cartoon-style depiction of a young boy with short brown hair, standing with arms outstretched. The boy is wearing red shorts with a white drawstring, and he is barefoot.\n\nSurrounding the boy are labeled boxes, each containing an illustration of a specific body part. Lines connect each box to the corresponding part on the boy's body. The labeled body parts include:\n\n1. **Head**: A smaller image of the boy's head.\n2. **Eye**: A single eye with eyelashes.\n3. **Nose**: A simple depiction of a nose.\n4. **Ear**: An illustration of an ear.\n5. **Mouth**: A smiling mouth with visible teeth.\n6. **Arm**: A single arm extended outward.\n7. **Hand**: An open hand with fingers spread.\n8. **Leg**: A pair of legs wearing shorts.\n9. **Knee**: A bent knee.\n10. **Foot**: A single foot.\n\nAt the top of the image, there is a blue banner with orange accents that reads \"BODY PARTS\" in bold white letters. The overall style is colorful and playful, making it suitable for educational purposes aimed at young children.",
              "height": 190.0976377952756,
              "left": 405.790157480315,
              "ori_height": 1125,
              "ori_width": 1125,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_15_0.png",
              "tag": "Body Parts, Educational Illustration, Cartoon Boy",
              "top": 179.43212598425197,
              "width": 185.25464566929136
            }
          ],
          "notes": null,
          "page": 15,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_15.png",
          "text": [
            "Follow the leader.",
            "",
            "",
            "upper leg",
            "4",
            "The learners need to figure out what they must touch. Read the added instruction to them. They wait until the instructions have been read and then they complete them.\nClick Back to main slide to continue.",
            "Back to main slide",
            "Hold it and walk around in a circle."
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image is an educational illustration designed to teach children about different body parts. It features a cartoon-style drawing of a young boy with a cheerful expression, standing with arms outstretched. The boy is wearing red shorts with a white drawstring and is depicted with short, dark hair and blue eyes.\n\nSurrounding the boy are labeled boxes, each containing an illustration of a specific body part. These boxes are connected to the corresponding parts on the boy's body with red lines. The labeled body parts include:\n\n- **Head**: A smaller illustration of the boy's head.\n- **Eye**: A close-up of a single eye.\n- **Nose**: A depiction of a nose.\n- **Ear**: An illustration of an ear.\n- **Mouth**: A drawing of an open mouth with visible teeth.\n- **Arm**: An image of an arm.\n- **Hand**: A depiction of a hand.\n- **Leg**: An illustration of legs wearing red shorts.\n- **Knee**: A drawing of a knee.\n- **Foot**: An image of a foot.\n\nAt the top of the image, there is a blue banner with the text \"BODY PARTS\" in white, flanked by red ribbon-like accents. The overall style is colorful and playful, suitable for a young audience, with clear and simple illustrations to aid in learning.",
              "height": 188.8404724409449,
              "left": 405.790157480315,
              "ori_height": 1125,
              "ori_width": 1125,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_16_0.png",
              "tag": "Body Parts, Educational Illustration, Cartoon Boy, Labeled Diagram, Children's Learning",
              "top": 179.22283464566928,
              "width": 185.25464566929136
            }
          ],
          "notes": null,
          "page": 16,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_16.png",
          "text": [
            "Follow the leader.",
            "",
            "",
            "right knee",
            "5",
            "The learners need to figure out what they must touch. Read the added instruction to them. They wait until the instructions have been read and then they complete them.\nClick Back to main slide to continue.",
            "Back to main slide",
            "And criss cross your legs four times."
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image is an educational illustration designed to teach children about different body parts. It features a cartoon-style, smiling boy with short dark hair, standing with arms outstretched. The boy is wearing red shorts with a white drawstring. Surrounding the boy are labeled boxes, each connected to a specific body part with a red line. \n\nThe labels and corresponding body parts are as follows:\n- \"HEAD\" with an illustration of a head.\n- \"EYE\" with an illustration of an eye.\n- \"NOSE\" with an illustration of a nose.\n- \"EAR\" with an illustration of an ear.\n- \"MOUTH\" with an illustration of a mouth.\n- \"ARM\" with an illustration of an arm.\n- \"HAND\" with an illustration of a hand.\n- \"LEG\" with an illustration of legs.\n- \"KNEE\" with an illustration of a knee.\n- \"FOOT\" with an illustration of a foot.\n\nAt the top of the image, there is a blue banner with the text \"BODY PARTS\" in bold white letters, flanked by orange ribbon-like accents. The overall style is colorful and playful, suitable for a young audience, and aims to visually associate each body part with its name.",
              "height": 185.04818897637796,
              "left": 405.790157480315,
              "ori_height": 1125,
              "ori_width": 1125,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_17_0.png",
              "tag": "Body Parts, Educational Illustration, Cartoon Boy",
              "top": 179.2063779527559,
              "width": 184.28692913385828
            }
          ],
          "notes": null,
          "page": 17,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_17.png",
          "text": [
            "Follow the leader.",
            "",
            "",
            "head",
            "6",
            "The learners need to figure out what they must touch. Read the added instruction to them. They wait until the instructions have been read and then they complete them.\nClick Back to main slide to continue.",
            "Back to main slide",
            "And do seven jumping jacks."
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image is an educational illustration designed to teach children about different body parts. It features a cartoon-style depiction of a young boy with short dark hair, standing with arms outstretched. The boy is wearing red shorts with a white drawstring and is barefoot. Surrounding the boy are labeled boxes that identify various body parts. Each box contains an illustration of the specific body part and is connected to the corresponding part on the boy's body with a red line. The labeled body parts include:\n\n- **Head**: A smaller illustration of the boy's head.\n- **Eye**: A close-up of a single eye.\n- **Nose**: An illustration of a nose.\n- **Ear**: A depiction of an ear.\n- **Mouth**: An image showing a smiling mouth with teeth.\n- **Arm**: An illustration of an arm.\n- **Hand**: A depiction of a hand with fingers spread.\n- **Leg**: An illustration of legs wearing shorts.\n- **Knee**: A depiction of a knee.\n- **Foot**: An illustration of a foot.\n\nAt the top of the image, there is a blue banner with the text \"BODY PARTS\" in bold white letters, flanked by red ribbon-like accents. The overall style is colorful and playful, suitable for a young audience, and aims to make learning about body parts engaging and accessible.",
              "height": 190.22669291338585,
              "left": 410.5299212598425,
              "ori_height": 1125,
              "ori_width": 1125,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_18_0.png",
              "tag": "Body Parts, Educational Illustration, Cartoon Style",
              "top": 178.46795275590551,
              "width": 177.29110236220473
            }
          ],
          "notes": null,
          "page": 18,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_18.png",
          "text": [
            "Follow the leader.",
            "",
            "",
            "left ear",
            "",
            "Touch\nyour\n",
            "",
            "7",
            "The learners need to figure out what they must touch. Read the added instruction to them. They wait until the instructions have been read and then they complete them.\nClick Back to main slide to continue.",
            "Back to main slide",
            "And touch your toes, then put your hands on your hips."
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image is an educational illustration designed to teach children about different body parts. It features a cartoon-style depiction of a young boy standing with arms outstretched, wearing red shorts. The boy has a cheerful expression with large eyes, a wide smile, and short brown hair. Surrounding the boy are labeled boxes, each containing an illustration of a specific body part and its corresponding label. The body parts highlighted include:\n\n- **Eye**: Illustrated with a large eye and labeled \"EYE.\"\n- **Nose**: Depicted with a simple nose illustration and labeled \"NOSE.\"\n- **Arm**: Shown with an extended arm and labeled \"ARM.\"\n- **Leg**: Illustrated with a pair of legs wearing shorts and labeled \"LEG.\"\n- **Knee**: Depicted with a bent knee and labeled \"KNEE.\"\n- **Head**: Illustrated with a smaller version of the boy's head and labeled \"HEAD.\"\n- **Ear**: Shown with a detailed ear illustration and labeled \"EAR.\"\n- **Mouth**: Depicted with a smiling mouth showing teeth and labeled \"MOUTH.\"\n- **Hand**: Illustrated with an open hand and labeled \"HAND.\"\n- **Foot**: Shown with a foot illustration and labeled \"FOOT.\"\n\nAt the top of the image, there is a banner with a blue background and red accents, displaying the title \"BODY PARTS\" in bold white letters. The image uses bright colors and simple shapes",
              "height": 119.7472440944882,
              "left": 426.4974015748032,
              "ori_height": 1125,
              "ori_width": 1125,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_19_6.png",
              "tag": "Body Parts, Educational Illustration, Cartoon Boy",
              "top": 192.41496062992127,
              "width": 150.30787401574804
            }
          ],
          "notes": null,
          "page": 19,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_19.png",
          "text": [
            "Follow the leader.",
            "",
            "",
            "mouth",
            "8",
            "The learners need to figure out what they must touch. Read the added instruction to them. They wait until the instructions have been read and then they complete them.\nClick Back to main slide to continue.",
            "Back to main slide",
            "And stick out your tongue, then bend to your left side."
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image is an educational illustration designed to teach children about different body parts. It features a cartoon-style depiction of a young boy with short dark hair, standing with his arms outstretched. The boy is wearing red shorts with a white drawstring. Surrounding the boy are labeled boxes, each containing an illustration of a specific body part. \n\n- At the top, a blue banner with orange accents reads \"BODY PARTS\" in bold white letters.\n- The body parts labeled include:\n  - \"HEAD\" with a small illustration of the boy's head.\n  - \"EYE\" with a close-up of an eye.\n  - \"NOSE\" with an illustration of a nose.\n  - \"EAR\" with an illustration of an ear.\n  - \"MOUTH\" with an illustration of a smiling mouth showing teeth.\n  - \"ARM\" with an illustration of an arm.\n  - \"HAND\" with an illustration of a hand.\n  - \"LEG\" with an illustration of legs wearing red shorts.\n  - \"KNEE\" with an illustration of a knee.\n  - \"FOOT\" with an illustration of a foot.\n\nEach body part is connected to the corresponding area on the boy's body with a red line, helping to visually associate the label with the actual body part. The overall style is colorful, friendly, and engaging, suitable for a young audience.",
              "height": 121.22338582677165,
              "left": 414.38732283464566,
              "ori_height": 1125,
              "ori_width": 1125,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_20_6.png",
              "tag": "Body Parts, Educational Illustration, Cartoon Boy",
              "top": 183.88551181102363,
              "width": 180.49307086614172
            }
          ],
          "notes": null,
          "page": 20,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_20.png",
          "text": [
            "Follow the leader.",
            "",
            "",
            "hand",
            "9",
            "The learners need to figure out what they must touch. Read the added instruction to them. They wait until the instructions have been read and then they complete them.\nClick Back to main slide to continue.",
            "Back to main slide",
            "And nod your head twice, then sit back down."
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image is an educational illustration designed to teach children about different body parts. It features a cartoon-style depiction of a young boy with short dark hair, standing with arms outstretched. The boy is wearing red shorts with a white drawstring. Surrounding the boy are labeled boxes, each containing an illustration of a specific body part, connected to the corresponding part on the boy's body with red lines.\n\nAt the top, a blue banner with red ends displays the title \"BODY PARTS\" in bold white letters. The labeled body parts include:\n\n- **Head**: A smaller illustration of the boy's head.\n- **Eye**: A detailed drawing of an eye.\n- **Nose**: A simple depiction of a nose.\n- **Ear**: An illustration of an ear.\n- **Mouth**: A drawing of an open mouth with visible teeth.\n- **Arm**: A representation of an arm.\n- **Hand**: An illustration of an open hand.\n- **Leg**: A depiction of legs wearing red shorts.\n- **Knee**: A simple drawing of a knee.\n- **Foot**: An illustration of a foot.\n\nThe overall style is colorful and playful, making it suitable for educational purposes aimed at young children.",
              "height": 124.49385826771652,
              "left": 422.8572440944882,
              "ori_height": 1125,
              "ori_width": 1125,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_21_6.png",
              "tag": "Body Parts, Educational Illustration, Cartoon Style",
              "top": 182.4540157480315,
              "width": 159.59055118110237
            }
          ],
          "notes": null,
          "page": 21,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_21.png",
          "text": [
            "Follow the leader.",
            "",
            "",
            "feet",
            "10",
            "The learners need to figure out what they must touch. Read the added instruction to them. They wait until the instructions have been read and then they complete them.\nClick Back to main slide to continue.",
            "Back to main slide",
            "And touch your shoulders, then do a little dance."
          ],
          "title": null,
          "videos": []
        }
      ]
    },
    "status": "succeed"
  }
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

## POST PPT修改

POST /attach/module

> Body 请求参数

```json
{}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|query|number| 否 |ID 编号|
|module_type|query|string| 否 |目前可选值只有parse|
|Authorization|header|string| 否 |none|
|body|body|object| 否 |none|

> 返回示例

> 200 Response

```json
{
  "code": 200,
  "msg": "query module json finished",
  "result": {
    "code": 200,
    "message": "parse ppt finished",
    "res": {
      "document_info": [
        {
          "audios": [],
          "images": [],
          "notes": "",
          "page": 1,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_1.png",
          "text": [],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image depicts a digital illustration of a soccer goal on a field. The goal is centrally positioned, featuring a white frame and a net with a grid pattern. The field is shown with a vibrant green color, marked with white lines indicating the penalty area and the penalty spot in front of the goal. The background is a gradient transitioning from dark blue to black, suggesting a night setting, possibly under stadium lights. The composition is symmetrical, focusing on the goal, and the style is clean and modern, suitable for use in sports-related digital media or games.",
              "height": 570.3156692913386,
              "left": 29.690236220472443,
              "ori_height": 1211,
              "ori_width": 2422,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_2_3.png",
              "tag": "Soccer Goal, Green Field, Night Setting",
              "top": -62.526299212598424,
              "width": 717.8088976377953
            },
            {
              "desp": "The image depicts an illustrated character of a young soccer player in mid-action. The player is wearing a maroon and light blue soccer uniform, consisting of a short-sleeved jersey and matching shorts. The jersey has light blue sleeves and a maroon body. The player is also wearing maroon knee-high socks and bright green soccer cleats with studs. The character is in a dynamic pose, balancing a soccer ball on their right knee, suggesting they are juggling or controlling the ball. The soccer ball is classic in design, featuring a pattern of black pentagons and white hexagons. The player's hair is brown and styled in a casual, slightly tousled manner. The background is plain, emphasizing the character and their action.",
              "height": 73.1076377952756,
              "left": 980.571496062992,
              "ori_height": 1920,
              "ori_width": 1920,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_2_5.png",
              "tag": "Soccer Player, Dynamic Pose, Maroon Uniform",
              "top": 59.219212598425194,
              "width": 76.4307874015748
            },
            {
              "desp": "The image depicts an illustrated character of a young soccer player in mid-action. The player is wearing a maroon and light blue soccer uniform, consisting of a short-sleeved jersey and shorts. The jersey features light blue sleeves and a maroon body, while the shorts are entirely maroon. The player is also wearing maroon knee-high socks and bright green soccer cleats with studs. The character is posed with one knee raised, balancing a classic black and white soccer ball on the thigh. The illustration style is clean and cartoonish, with simple lines and flat colors, suitable for animation or digital media use.",
              "height": 73.1076377952756,
              "left": 1073.8611023622047,
              "ori_height": 1920,
              "ori_width": 1920,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_2_6.png",
              "tag": "Soccer Player, Cartoon Style, Maroon Uniform",
              "top": 59.21913385826772,
              "width": 76.4307874015748
            },
            {
              "desp": "The image depicts an animated character of a young soccer player in mid-action. The player is wearing a maroon and light blue soccer uniform, consisting of a short-sleeved jersey and shorts. The jersey has light blue sleeves and a maroon body, while the shorts are entirely maroon. The player is also wearing maroon knee-high socks and bright green soccer cleats with white studs. The character is posed with one knee raised, balancing a soccer ball on the knee. The soccer ball is designed with a classic black and white hexagonal pattern. The overall style of the image is cartoonish and colorful, suitable for animation or digital media related to sports or children's content.",
              "height": 73.1076377952756,
              "left": 1167.1507086614174,
              "ori_height": 1920,
              "ori_width": 1920,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_2_7.png",
              "tag": "Soccer Player, Cartoon Style, Sports Animation",
              "top": 59.219055118110234,
              "width": 76.4307874015748
            },
            {
              "desp": "The image depicts an illustration of a young soccer player in mid-action, performing a juggling move with a soccer ball. The player is wearing a sports uniform consisting of a maroon jersey with light blue sleeves, matching maroon shorts, and maroon knee-high socks. The player is also wearing bright green soccer cleats with studs. The soccer ball is depicted in mid-air, just above the player's knee, suggesting a dynamic motion. The overall style of the illustration is cartoon-like, with clean lines and solid colors, suitable for use in animation or educational materials related to sports.",
              "height": 73.1076377952756,
              "left": 1257.228818897638,
              "ori_height": 1920,
              "ori_width": 1920,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_2_8.png",
              "tag": "Soccer Player, Juggling Move, Cartoon Illustration",
              "top": 59.219055118110234,
              "width": 76.4307874015748
            },
            {
              "desp": "The image depicts an illustrated character of a young soccer player in mid-action. The character is wearing a sports uniform consisting of a maroon jersey with light blue sleeves, matching maroon shorts, and maroon knee-high socks. The player is poised with one knee raised, balancing a classic black and white soccer ball on the knee. The character's footwear includes bright green soccer cleats with visible studs. The illustration style is clean and cartoon-like, suitable for animation or educational content related to sports.",
              "height": 73.1076377952756,
              "left": 993.0726771653544,
              "ori_height": 1920,
              "ori_width": 1920,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_2_9.png",
              "tag": "Soccer Player, Sports Uniform, Cartoon Illustration",
              "top": 233.30220472440945,
              "width": 76.4307874015748
            },
            {
              "desp": "The image depicts an illustrated character of a young soccer player in mid-action, performing a juggling move with a soccer ball. The player is wearing a sports uniform consisting of a maroon jersey with light blue sleeves, matching maroon shorts, and maroon knee-high socks. The character's shoes are bright green soccer cleats with visible studs. The soccer ball is designed with a classic black and white hexagonal pattern and is positioned near the player's raised knee, suggesting a juggling or dribbling motion. The overall style is cartoonish and colorful, suitable for animation or digital media aimed at a younger audience.",
              "height": 73.1076377952756,
              "left": 1073.8611023622047,
              "ori_height": 1920,
              "ori_width": 1920,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_2_10.png",
              "tag": "Soccer Player, Juggling Move, Cartoon Style",
              "top": 233.30212598425197,
              "width": 76.4307874015748
            },
            {
              "desp": "The image depicts an illustration of a young soccer player in mid-action, performing a juggling move with a soccer ball. The player is wearing a sports uniform consisting of a maroon jersey with light blue sleeves, matching maroon shorts, and maroon knee-high socks. The player is also wearing bright green soccer cleats with studs, suitable for playing on grass. The soccer ball is depicted in mid-air, featuring a classic black and white hexagonal pattern. The player's posture suggests they are balancing the ball on their knee, with one leg raised and both arms slightly bent at the elbows, indicating movement and coordination. The overall style of the illustration is cartoon-like, with bold colors and clean lines.",
              "height": 73.1076377952756,
              "left": 1167.1507086614174,
              "ori_height": 1920,
              "ori_width": 1920,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_2_11.png",
              "tag": "Soccer Player, Juggling Move, Cartoon Illustration",
              "top": 233.7427559055118,
              "width": 76.4307874015748
            },
            {
              "desp": "The image depicts an illustrated character of a young soccer player in mid-action. The player is wearing a sports uniform consisting of a maroon jersey with light blue sleeves, matching maroon shorts, and maroon knee-high socks. The character is poised with one knee raised, balancing a classic black and white soccer ball on the knee. The player is also wearing bright green soccer cleats with visible studs. The illustration style is simple and cartoon-like, with clean lines and solid colors, suitable for use in animation or educational materials related to sports.",
              "height": 73.1076377952756,
              "left": 1257.2287401574804,
              "ori_height": 1920,
              "ori_width": 1920,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_2_12.png",
              "tag": "Soccer Player, Sports Uniform, Cartoon Illustration",
              "top": 231.17133858267715,
              "width": 76.4307874015748
            }
          ],
          "notes": null,
          "page": 2,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_2.png",
          "text": [
            "Warm up, warm up, everybody warm up.",
            "There are 8 soccer balls. Click to have one ball bounce in.  \nClick on the ball to be directed to an action slide. When you return to this slide, repeat the clicks.\nOnce 8 balls have been actioned, click the arrow to continue. ",
            "",
            ""
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image depicts a digital illustration of a soccer goal on a field. The goal is centrally positioned and features a white frame with a net that is neatly divided into a grid pattern. The field is a vibrant green with clearly marked white lines, including the penalty arc and the penalty spot in front of the goal. The background is a dark gradient, transitioning from black at the top to a deep blue behind the goal, suggesting a night setting. The composition is symmetrical, focusing on the goal, and the lighting creates a subtle spotlight effect on the field, enhancing the centrality of the goal. This image could be used as a background or asset in a sports-related digital media project, such as a video game or animation.",
              "height": 570.3156692913386,
              "left": 29.690236220472443,
              "ori_height": 1211,
              "ori_width": 2422,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_3_3.png",
              "tag": "Soccer Goal, Night Setting, Digital Illustration",
              "top": -62.526299212598424,
              "width": 717.8088976377953
            },
            {
              "desp": "The image depicts a cartoon-style illustration of a martial artist performing a dynamic jumping kick. The character is wearing a traditional white karate gi with a black belt, indicating a high level of proficiency. The gi has long sleeves and pants, with the belt tied around the waist. The character's arms are bent with fists clenched, suggesting readiness and focus. The left leg is extended forward in a kicking motion, while the right leg is bent backward, contributing to the sense of movement and action. The character's hair is styled in a neat bun, secured with a pink hair tie. The overall style is clean and vibrant, suitable for animation or digital media focused on martial arts themes.",
              "height": 311.81102362204723,
              "left": 167.4448818897638,
              "ori_height": 1639,
              "ori_width": 2416,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_3_4.png",
              "tag": "Martial Artist, Jumping Kick, Karate Gi",
              "top": 78.48929133858267,
              "width": 459.5121259842519
            }
          ],
          "notes": null,
          "page": 3,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_3.png",
          "text": [
            "Warm up, warm up, everybody warm up.",
            "Read the question / action to the learners.\nThey pretend to be doing the action. \nClick Back to main slide to continue. ",
            "",
            "Can you kick like her? Kick four times.",
            "Back to main slide"
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image depicts a digital illustration of a soccer goal on a field. The goal is centrally positioned and features a white frame with a net composed of a grid pattern. The field is shown with a vibrant green surface, marked with white lines indicating the penalty area and the center circle. The perspective is from the viewpoint of a player approaching the goal, emphasizing the goal's prominence. The background is a dark gradient, transitioning from black at the top to a subtle blue near the goal, suggesting a stadium setting under artificial lighting. The overall style is clean and modern, suitable for use in sports-related digital media or UI design, such as a game interface or sports app.",
              "height": 570.3156692913386,
              "left": 29.690236220472443,
              "ori_height": 1211,
              "ori_width": 2422,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_4_3.png",
              "tag": "Soccer Goal, Digital Illustration, Sports UI Design",
              "top": -62.526299212598424,
              "width": 717.8088976377953
            },
            {
              "desp": "The image is a cartoon-style illustration featuring a young boy energetically jumping over two tires. The boy has short brown hair and is wearing a bright blue t-shirt, brown shorts, and red shoes. His expression is cheerful and animated, suggesting excitement or playfulness. The two tires are positioned on the ground, slightly apart from each other, and are depicted in a realistic style with visible treads. The background is transparent, indicating that this image could be used as an animation asset or in digital media where the character and objects can be placed over different backgrounds. The overall style is colorful and playful, suitable for children's content or educational materials.",
              "height": 311.81102362204723,
              "left": 302.3056692913386,
              "ori_height": 1651,
              "ori_width": 1659,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_4_4.png",
              "tag": "Cartoon Boy, Jumping Tires, Children's Illustration",
              "top": 119.14551181102362,
              "width": 177.69433070866145
            }
          ],
          "notes": null,
          "page": 4,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_4.png",
          "text": [
            "Warm up, warm up, everybody warm up.",
            "Read the question / action to the learners.\nThey pretend to be doing the action. \nClick Back to main slide to continue. ",
            "",
            "Can you jump like him? Jump over six tyres.",
            "Back to main slide"
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image depicts a digital illustration of a soccer goal set against a dark background, likely intended for use in sports-related digital media or a video game. The scene is centered on a standard soccer goal with a white frame and net, positioned on a green soccer field. The field is marked with white lines, including the penalty arc and spot, indicating the area in front of the goal. The perspective is from the center of the field, directly facing the goal, creating a symmetrical composition. The lighting is focused on the goal and the immediate area of the field, with the background fading into darkness, suggesting a spotlight effect often used in sports graphics to emphasize the goal area.",
              "height": 570.3156692913386,
              "left": 29.690236220472443,
              "ori_height": 1211,
              "ori_width": 2422,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_5_3.png",
              "tag": "Soccer Goal, Digital Illustration, Spotlight Effect",
              "top": -62.526299212598424,
              "width": 717.8088976377953
            },
            {
              "desp": "The image features a cartoon-style illustration of a young girl with a cheerful expression. She has bright orange hair styled in a bob cut with a small hair tuft on top. Her eyes are large and blue, adding to her animated appearance. She is wearing a yellow shirt with a blue bow at the collar and a short red skirt. Her outfit is completed with purple shoes and matching socks. The girl is depicted in a playful pose, standing on one leg with her arms outstretched to the sides, suggesting a sense of balance or dance. The background is transparent, making the character suitable for use as an animation asset or in digital media where she can be placed over various backgrounds.",
              "height": 311.81102362204723,
              "left": 323.2340157480315,
              "ori_height": 1651,
              "ori_width": 1659,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_5_4.png",
              "tag": "Cartoon Girl, Orange Hair, Playful Pose",
              "top": 171.93897637795277,
              "width": 156.7659842519685
            }
          ],
          "notes": null,
          "page": 5,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_5.png",
          "text": [
            "Warm up, warm up, everybody warm up.",
            "Read the question / action to the learners.\nThey pretend to be doing the action. \nClick Back to main slide to continue. ",
            "",
            "Can you hop like her? Hop fives times.",
            "Back to main slide"
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image depicts a stylized representation of a soccer field focusing on the goal area. The foreground features a well-defined, green grass pitch with white markings indicating the penalty box and the goal area. The central focus is on the soccer goal, which is prominently displayed with a white frame and netting. The net is detailed with a grid pattern, and the goalposts are positioned centrally within the image. The background is a gradient transitioning from dark blue to black, suggesting a night setting or an indoor stadium environment. The composition is symmetrical, emphasizing the goal as the main element, suitable for use in sports-related digital media or as a background for soccer-themed applications.",
              "height": 570.3156692913386,
              "left": 29.690236220472443,
              "ori_height": 1211,
              "ori_width": 2422,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_6_3.png",
              "tag": "Soccer Field, Goal Area, Night Setting",
              "top": -62.526299212598424,
              "width": 717.8088976377953
            },
            {
              "desp": "The image depicts a cartoon-style illustration of a young boy standing on a small patch of grass. He is wearing a blue baseball cap with an orange underside, a yellow and white striped t-shirt, dark blue shorts, and blue sneakers with green soles. The boy is positioned as if he is about to catch a red cricket ball, which is shown in mid-air with a motion line indicating its trajectory. The grass patch is oval-shaped with a few small flowers and leaves scattered on it, adding a playful outdoor setting to the scene.",
              "height": 311.81102362204723,
              "left": 122.7903937007874,
              "ori_height": 1639,
              "ori_width": 2416,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_6_4.png",
              "tag": "Cartoon Boy, Cricket Ball, Outdoor Scene",
              "top": 137.1,
              "width": 459.51141732283463
            }
          ],
          "notes": null,
          "page": 6,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_6.png",
          "text": [
            "Warm up, warm up, everybody warm up.",
            "Read the question / action to the learners.\nThey pretend to be doing the action. \nClick Back to main slide to continue. ",
            "",
            "Can you catch like him? Catch a ball three times.",
            "Back to main slide"
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image depicts a digital illustration of a soccer goal set against a dark background, which creates a dramatic contrast. The goal is centrally positioned and features a white frame with a net composed of evenly spaced squares. The netting is detailed with a subtle gradient, suggesting depth and dimension. In front of the goal, the foreground shows a section of a soccer field with a vibrant green color and white markings, including the penalty spot and part of the penalty arc. The field is illuminated, highlighting the goal area, while the surrounding area fades into darkness, emphasizing the focus on the goal itself. This image could be used as a background or asset in sports-related digital media or animation.",
              "height": 570.3156692913386,
              "left": 29.690236220472443,
              "ori_height": 1211,
              "ori_width": 2422,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_7_3.png",
              "tag": "Soccer Goal, Dark Background, Soccer Field",
              "top": -62.526299212598424,
              "width": 717.8088976377953
            },
            {
              "desp": "The image depicts a cartoon-style illustration of a young boy engaged in a playful activity. He is positioned on a small patch of grass, which is adorned with simple floral designs. The boy is wearing a dark navy blue t-shirt with a bold yellow geometric design on the chest. His attire includes light blue denim shorts with rolled-up cuffs and visible yellow stitching details. He is also wearing white socks and blue sneakers with yellow laces and soles. The boy is in a dynamic pose, with his arms extended as if he is about to catch or throw a red cricket ball that is in mid-air in front of him. The illustration is colorful and vibrant, with a playful and energetic theme suitable for animation or children's media.",
              "height": 311.81102362204723,
              "left": 160.1420472440945,
              "ori_height": 1639,
              "ori_width": 2416,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_7_4.png",
              "tag": "Cartoon Boy, Playful Activity, Cricket Ball, Colorful Illustration",
              "top": 159.41346456692912,
              "width": 456.9052755905512
            }
          ],
          "notes": null,
          "page": 7,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_7.png",
          "text": [
            "Warm up, warm up, everybody warm up.",
            "Read the question / action to the learners.\nThey pretend to be doing the action. \nClick Back to main slide to continue. ",
            "",
            "Can you throw like him? Throw the ball twice.",
            "Back to main slide"
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image depicts a digital illustration of a soccer goal on a field. The goal is centrally positioned and features a white frame with a net composed of evenly spaced horizontal and vertical lines, creating a grid pattern. The background is a dark gradient transitioning from black at the top to a deep blue, suggesting a nighttime or indoor setting. The soccer field is shown in a vibrant green color, with white markings indicating the penalty area, the penalty spot, and the arc of the penalty box. The perspective is from the center of the field facing the goal, emphasizing the goal's structure and the field's layout. The image is likely designed for use in sports-related digital media, such as a game or animation asset, focusing on the goal area.",
              "height": 570.3156692913386,
              "left": 29.690236220472443,
              "ori_height": 1211,
              "ori_width": 2422,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_8_3.png",
              "tag": "Soccer Goal, Digital Illustration, Nighttime Setting",
              "top": -62.526299212598424,
              "width": 717.8088976377953
            },
            {
              "desp": "The image is a cartoon-style illustration of a cheerful young boy jumping rope. The boy has curly brown hair and is depicted with a wide, joyful smile, with his eyes closed in delight. He is wearing a green sleeveless shirt and blue pants, along with brown shoes. The jump rope is orange with blue handles, and the boy is holding it in both hands, mid-jump, with his legs spread apart in a playful manner. The illustration has a bright and lively color palette, emphasizing a sense of fun and energy, suitable for children's media or educational content.",
              "height": 311.81102362204723,
              "left": 217.6596850393701,
              "ori_height": 1092,
              "ori_width": 1092,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_8_4.png",
              "tag": "Cartoon Boy, Jump Rope, Children's Illustration",
              "top": 119.14551181102362,
              "width": 311.81102362204723
            }
          ],
          "notes": null,
          "page": 8,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_8.png",
          "text": [
            "Warm up, warm up, everybody warm up.",
            "Read the question / action to the learners.\nThey pretend to be doing the action. \nClick Back to main slide to continue. ",
            "",
            "Can you skip like him? Skip eight times.",
            "Back to main slide"
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image depicts a digital illustration of a soccer goal set against a dark background. The goal is centrally positioned, featuring a white frame and a net composed of evenly spaced squares. The netting is detailed with a subtle gradient, suggesting depth and dimension. In front of the goal is a section of a soccer field, characterized by a vibrant green color and marked with white lines indicating the penalty area and the penalty spot. The field lines include the arc of the penalty area and the center circle, providing context for the goal's placement within a soccer field. The overall composition is simple and focused, with the goal and field elements prominently displayed against the stark black background, which enhances the contrast and visibility of the soccer elements. This image could be used in sports-related digital media, such as a game interface or animation asset.",
              "height": 570.3156692913386,
              "left": 29.690236220472443,
              "ori_height": 1211,
              "ori_width": 2422,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_9_3.png",
              "tag": "Soccer Goal, Penalty Area, Digital Illustration",
              "top": -62.526299212598424,
              "width": 717.8088976377953
            },
            {
              "desp": "The image is a cartoon-style illustration of a young girl in motion, depicted as if she is running or skipping. She has bright orange hair styled in a high ponytail, secured with a purple hair tie. Her facial expression is joyful, with a wide smile showing her teeth and her eyes looking forward. The girl is wearing a pink t-shirt with a darker pink outline, purple shorts, and blue sneakers with white soles. Her socks are white and visible above her shoes. The illustration includes motion lines near her feet, emphasizing her movement. The overall style is vibrant and playful, suitable for use in children's animation or educational content. The background is transparent, allowing for easy integration into various digital media.",
              "height": 311.81102362204723,
              "left": 266.5249606299213,
              "ori_height": 1649,
              "ori_width": 2361,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_9_4.png",
              "tag": "Cartoon Girl, Running, Vibrant Illustration",
              "top": 119.14551181102362,
              "width": 244.13937007874017
            }
          ],
          "notes": null,
          "page": 9,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_9.png",
          "text": [
            "Warm up, warm up, everybody warm up.",
            "Read the question / action to the learners.\nThey pretend to be doing the action. \nClick Back to main slide to continue. ",
            "",
            "Can you run like her? Run on the spot for 10 counts.",
            "Back to main slide"
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image depicts a stylized soccer field with a focus on the goal area. The foreground features a green grass pitch with white markings, including the penalty arc and spot, indicating the area directly in front of the goal. The goal itself is centrally positioned, with a white frame and netting, creating a grid pattern. The background is a dark gradient transitioning from black at the top to a deep blue near the goal, suggesting a night-time setting or an indoor stadium environment. The composition is symmetrical, emphasizing the goal as the central element, and the lighting effect adds depth and focus to the scene. This image could be used in digital media related to sports, such as a video game or animation asset, where the goal area is a key visual component.",
              "height": 570.3156692913386,
              "left": 29.690236220472443,
              "ori_height": 1211,
              "ori_width": 2422,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_10_3.png",
              "tag": "Soccer Field, Goal Area, Night Setting",
              "top": -62.526299212598424,
              "width": 717.8088976377953
            },
            {
              "desp": "The image depicts an animated character of a young child from a rear view, appearing to be in a climbing or reaching pose. The child is wearing a colorful, segmented cap with red, blue, and yellow sections. The child has brown hair styled in a single braid that extends down the back. They are dressed in a white t-shirt and light blue shorts. The child is also wearing bright green sneakers with white soles and yellow socks. The character's arms are raised, and one knee is bent, suggesting movement or an action-oriented pose. The illustration style is cartoonish, with bold outlines and vibrant colors, suitable for use in children's media or educational animations.",
              "height": 311.81102362204723,
              "left": 277.38818897637793,
              "ori_height": 892,
              "ori_width": 1185,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_10_5.png",
              "tag": "Animated Character, Colorful Cap, Cartoon Style",
              "top": 105.47763779527558,
              "width": 207.95661417322836
            }
          ],
          "notes": null,
          "page": 10,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_10.png",
          "text": [
            "Warm up, warm up, everybody warm up.",
            "Read the question / action to the learners.\nThey pretend to be doing the action. \nClick Back to main slide to continue. ",
            "",
            "Back to main slide",
            "Can you climb like her? Climb up one rock."
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [],
          "notes": null,
          "page": 11,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_11.png",
          "text": [
            "Follow the leader.",
            "The learners take turns choosing a number around the body. Click on the number chosen to be directed to a slide with an action.  \nContinue playing until all numbers have been selected and the children are able to follow all the instructions.  \n\nClick the arrow to end.\nThis is the last slide.",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            ""
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [],
          "notes": null,
          "page": 12,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_12.png",
          "text": [
            "Follow the leader.",
            "The learners need to figure out what they must touch. Read the added instruction to them. They wait until the instructions have been read and then they complete them.\nClick Back to main slide to continue.",
            "1",
            "Back to main slide",
            "And pick up your pencil.."
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image is an educational illustration designed to teach children about different body parts. It features a cartoon-style depiction of a young boy standing with arms outstretched, wearing red shorts. The boy has brown hair, large blue eyes, and a cheerful expression. Surrounding the boy are labeled boxes, each containing an illustration of a specific body part. \n\n- At the top, a blue banner with red accents displays the title \"BODY PARTS\" in bold white letters.\n- On the left side, boxes labeled \"EYE,\" \"NOSE,\" \"ARM,\" \"LEG,\" and \"KNEE\" are connected to the corresponding parts on the boy's body with red lines.\n- On the right side, boxes labeled \"HEAD,\" \"EAR,\" \"MOUTH,\" \"HAND,\" and \"FOOT\" similarly connect to the respective body parts.\n- Each box contains a simple illustration of the body part, matching the cartoon style of the central figure.\n\nThe image uses bright colors and clear labeling to make it engaging and easy for children to understand and identify different body parts.",
              "height": 180.49330708661415,
              "left": 414.38732283464566,
              "ori_height": 1125,
              "ori_width": 1125,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_13_0.png",
              "tag": "Body Parts, Educational Illustration, Cartoon Boy",
              "top": 182.74346456692913,
              "width": 175.5828346456693
            }
          ],
          "notes": null,
          "page": 13,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_13.png",
          "text": [
            "Follow the leader.",
            "",
            "",
            "nose",
            "2",
            "The learners need to figure out what they must touch. Read the added instruction to them. They wait until the instructions have been read and then they complete them.\nClick Back to main slide to continue.",
            "Back to main slide",
            "And put your right hand behind your back.."
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image is an educational illustration designed to teach children about human body parts. It features a cartoon-style depiction of a young boy with short dark hair, standing with arms outstretched. The boy is wearing red shorts with a white drawstring. Surrounding the boy are labeled boxes, each containing an illustration of a specific body part. These boxes are connected to the corresponding parts on the boy's body with red lines. \n\nThe body parts identified include:\n\n- **Head**: Illustrated with a smaller version of the boy's face.\n- **Eye**: A large, cartoon-style eye with eyelashes.\n- **Ear**: A simplified illustration of an ear.\n- **Nose**: A basic depiction of a nose.\n- **Mouth**: A smiling mouth showing teeth.\n- **Arm**: A simplified illustration of an arm.\n- **Hand**: A cartoon-style hand with fingers spread.\n- **Leg**: A depiction of legs wearing shorts.\n- **Knee**: A basic illustration of a knee.\n- **Foot**: A simplified depiction of a foot.\n\nAt the top of the image, there is a banner with a blue background and orange ribbon ends, containing the text \"BODY PARTS\" in bold white letters. The overall style is colorful and playful, suitable for educational purposes aimed at young children.",
              "height": 186.6892125984252,
              "left": 405.5370866141732,
              "ori_height": 1125,
              "ori_width": 1125,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_14_0.png",
              "tag": "Human Body Parts, Educational Illustration, Cartoon Style",
              "top": 177.91425196850395,
              "width": 185.5076377952756
            }
          ],
          "notes": null,
          "page": 14,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_14.png",
          "text": [
            "Follow the leader.",
            "",
            "",
            "left arm",
            "3",
            "The learners need to figure out what they must touch. Read the added instruction to them. They wait until the instructions have been read and then they complete them.\nClick Back to main slide to continue.",
            "Back to main slide",
            "And skip around three times on the spot."
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image is an educational illustration designed to teach children about different body parts. It features a cartoon-style depiction of a young boy with short brown hair, standing with arms outstretched. The boy is wearing red shorts with a white drawstring, and he is barefoot.\n\nSurrounding the boy are labeled boxes, each containing an illustration of a specific body part. Lines connect each box to the corresponding part on the boy's body. The labeled body parts include:\n\n1. **Head**: A smaller image of the boy's head.\n2. **Eye**: A single eye with eyelashes.\n3. **Nose**: A simple depiction of a nose.\n4. **Ear**: An illustration of an ear.\n5. **Mouth**: A smiling mouth with visible teeth.\n6. **Arm**: A single arm extended outward.\n7. **Hand**: An open hand with fingers spread.\n8. **Leg**: A pair of legs wearing shorts.\n9. **Knee**: A bent knee.\n10. **Foot**: A single foot.\n\nAt the top of the image, there is a blue banner with orange accents that reads \"BODY PARTS\" in bold white letters. The overall style is colorful and playful, making it suitable for educational purposes aimed at young children.",
              "height": 190.0976377952756,
              "left": 405.790157480315,
              "ori_height": 1125,
              "ori_width": 1125,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_15_0.png",
              "tag": "Body Parts, Educational Illustration, Cartoon Boy",
              "top": 179.43212598425197,
              "width": 185.25464566929136
            }
          ],
          "notes": null,
          "page": 15,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_15.png",
          "text": [
            "Follow the leader.",
            "",
            "",
            "upper leg",
            "4",
            "The learners need to figure out what they must touch. Read the added instruction to them. They wait until the instructions have been read and then they complete them.\nClick Back to main slide to continue.",
            "Back to main slide",
            "Hold it and walk around in a circle."
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image is an educational illustration designed to teach children about different body parts. It features a cartoon-style drawing of a young boy with a cheerful expression, standing with arms outstretched. The boy is wearing red shorts with a white drawstring and is depicted with short, dark hair and blue eyes.\n\nSurrounding the boy are labeled boxes, each containing an illustration of a specific body part. These boxes are connected to the corresponding parts on the boy's body with red lines. The labeled body parts include:\n\n- **Head**: A smaller illustration of the boy's head.\n- **Eye**: A close-up of a single eye.\n- **Nose**: A depiction of a nose.\n- **Ear**: An illustration of an ear.\n- **Mouth**: A drawing of an open mouth with visible teeth.\n- **Arm**: An image of an arm.\n- **Hand**: A depiction of a hand.\n- **Leg**: An illustration of legs wearing red shorts.\n- **Knee**: A drawing of a knee.\n- **Foot**: An image of a foot.\n\nAt the top of the image, there is a blue banner with the text \"BODY PARTS\" in white, flanked by red ribbon-like accents. The overall style is colorful and playful, suitable for a young audience, with clear and simple illustrations to aid in learning.",
              "height": 188.8404724409449,
              "left": 405.790157480315,
              "ori_height": 1125,
              "ori_width": 1125,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_16_0.png",
              "tag": "Body Parts, Educational Illustration, Cartoon Boy, Labeled Diagram, Children's Learning",
              "top": 179.22283464566928,
              "width": 185.25464566929136
            }
          ],
          "notes": null,
          "page": 16,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_16.png",
          "text": [
            "Follow the leader.",
            "",
            "",
            "right knee",
            "5",
            "The learners need to figure out what they must touch. Read the added instruction to them. They wait until the instructions have been read and then they complete them.\nClick Back to main slide to continue.",
            "Back to main slide",
            "And criss cross your legs four times."
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image is an educational illustration designed to teach children about different body parts. It features a cartoon-style, smiling boy with short dark hair, standing with arms outstretched. The boy is wearing red shorts with a white drawstring. Surrounding the boy are labeled boxes, each connected to a specific body part with a red line. \n\nThe labels and corresponding body parts are as follows:\n- \"HEAD\" with an illustration of a head.\n- \"EYE\" with an illustration of an eye.\n- \"NOSE\" with an illustration of a nose.\n- \"EAR\" with an illustration of an ear.\n- \"MOUTH\" with an illustration of a mouth.\n- \"ARM\" with an illustration of an arm.\n- \"HAND\" with an illustration of a hand.\n- \"LEG\" with an illustration of legs.\n- \"KNEE\" with an illustration of a knee.\n- \"FOOT\" with an illustration of a foot.\n\nAt the top of the image, there is a blue banner with the text \"BODY PARTS\" in bold white letters, flanked by orange ribbon-like accents. The overall style is colorful and playful, suitable for a young audience, and aims to visually associate each body part with its name.",
              "height": 185.04818897637796,
              "left": 405.790157480315,
              "ori_height": 1125,
              "ori_width": 1125,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_17_0.png",
              "tag": "Body Parts, Educational Illustration, Cartoon Boy",
              "top": 179.2063779527559,
              "width": 184.28692913385828
            }
          ],
          "notes": null,
          "page": 17,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_17.png",
          "text": [
            "Follow the leader.",
            "",
            "",
            "head",
            "6",
            "The learners need to figure out what they must touch. Read the added instruction to them. They wait until the instructions have been read and then they complete them.\nClick Back to main slide to continue.",
            "Back to main slide",
            "And do seven jumping jacks."
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image is an educational illustration designed to teach children about different body parts. It features a cartoon-style depiction of a young boy with short dark hair, standing with arms outstretched. The boy is wearing red shorts with a white drawstring and is barefoot. Surrounding the boy are labeled boxes that identify various body parts. Each box contains an illustration of the specific body part and is connected to the corresponding part on the boy's body with a red line. The labeled body parts include:\n\n- **Head**: A smaller illustration of the boy's head.\n- **Eye**: A close-up of a single eye.\n- **Nose**: An illustration of a nose.\n- **Ear**: A depiction of an ear.\n- **Mouth**: An image showing a smiling mouth with teeth.\n- **Arm**: An illustration of an arm.\n- **Hand**: A depiction of a hand with fingers spread.\n- **Leg**: An illustration of legs wearing shorts.\n- **Knee**: A depiction of a knee.\n- **Foot**: An illustration of a foot.\n\nAt the top of the image, there is a blue banner with the text \"BODY PARTS\" in bold white letters, flanked by red ribbon-like accents. The overall style is colorful and playful, suitable for a young audience, and aims to make learning about body parts engaging and accessible.",
              "height": 190.22669291338585,
              "left": 410.5299212598425,
              "ori_height": 1125,
              "ori_width": 1125,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_18_0.png",
              "tag": "Body Parts, Educational Illustration, Cartoon Style",
              "top": 178.46795275590551,
              "width": 177.29110236220473
            }
          ],
          "notes": null,
          "page": 18,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_18.png",
          "text": [
            "Follow the leader.",
            "",
            "",
            "left ear",
            "",
            "Touch\nyour\n",
            "",
            "7",
            "The learners need to figure out what they must touch. Read the added instruction to them. They wait until the instructions have been read and then they complete them.\nClick Back to main slide to continue.",
            "Back to main slide",
            "And touch your toes, then put your hands on your hips."
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image is an educational illustration designed to teach children about different body parts. It features a cartoon-style depiction of a young boy standing with arms outstretched, wearing red shorts. The boy has a cheerful expression with large eyes, a wide smile, and short brown hair. Surrounding the boy are labeled boxes, each containing an illustration of a specific body part and its corresponding label. The body parts highlighted include:\n\n- **Eye**: Illustrated with a large eye and labeled \"EYE.\"\n- **Nose**: Depicted with a simple nose illustration and labeled \"NOSE.\"\n- **Arm**: Shown with an extended arm and labeled \"ARM.\"\n- **Leg**: Illustrated with a pair of legs wearing shorts and labeled \"LEG.\"\n- **Knee**: Depicted with a bent knee and labeled \"KNEE.\"\n- **Head**: Illustrated with a smaller version of the boy's head and labeled \"HEAD.\"\n- **Ear**: Shown with a detailed ear illustration and labeled \"EAR.\"\n- **Mouth**: Depicted with a smiling mouth showing teeth and labeled \"MOUTH.\"\n- **Hand**: Illustrated with an open hand and labeled \"HAND.\"\n- **Foot**: Shown with a foot illustration and labeled \"FOOT.\"\n\nAt the top of the image, there is a banner with a blue background and red accents, displaying the title \"BODY PARTS\" in bold white letters. The image uses bright colors and simple shapes",
              "height": 119.7472440944882,
              "left": 426.4974015748032,
              "ori_height": 1125,
              "ori_width": 1125,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_19_6.png",
              "tag": "Body Parts, Educational Illustration, Cartoon Boy",
              "top": 192.41496062992127,
              "width": 150.30787401574804
            }
          ],
          "notes": null,
          "page": 19,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_19.png",
          "text": [
            "Follow the leader.",
            "",
            "",
            "mouth",
            "8",
            "The learners need to figure out what they must touch. Read the added instruction to them. They wait until the instructions have been read and then they complete them.\nClick Back to main slide to continue.",
            "Back to main slide",
            "And stick out your tongue, then bend to your left side."
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image is an educational illustration designed to teach children about different body parts. It features a cartoon-style depiction of a young boy with short dark hair, standing with his arms outstretched. The boy is wearing red shorts with a white drawstring. Surrounding the boy are labeled boxes, each containing an illustration of a specific body part. \n\n- At the top, a blue banner with orange accents reads \"BODY PARTS\" in bold white letters.\n- The body parts labeled include:\n  - \"HEAD\" with a small illustration of the boy's head.\n  - \"EYE\" with a close-up of an eye.\n  - \"NOSE\" with an illustration of a nose.\n  - \"EAR\" with an illustration of an ear.\n  - \"MOUTH\" with an illustration of a smiling mouth showing teeth.\n  - \"ARM\" with an illustration of an arm.\n  - \"HAND\" with an illustration of a hand.\n  - \"LEG\" with an illustration of legs wearing red shorts.\n  - \"KNEE\" with an illustration of a knee.\n  - \"FOOT\" with an illustration of a foot.\n\nEach body part is connected to the corresponding area on the boy's body with a red line, helping to visually associate the label with the actual body part. The overall style is colorful, friendly, and engaging, suitable for a young audience.",
              "height": 121.22338582677165,
              "left": 414.38732283464566,
              "ori_height": 1125,
              "ori_width": 1125,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_20_6.png",
              "tag": "Body Parts, Educational Illustration, Cartoon Boy",
              "top": 183.88551181102363,
              "width": 180.49307086614172
            }
          ],
          "notes": null,
          "page": 20,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_20.png",
          "text": [
            "Follow the leader.",
            "",
            "",
            "hand",
            "9",
            "The learners need to figure out what they must touch. Read the added instruction to them. They wait until the instructions have been read and then they complete them.\nClick Back to main slide to continue.",
            "Back to main slide",
            "And nod your head twice, then sit back down."
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image is an educational illustration designed to teach children about different body parts. It features a cartoon-style depiction of a young boy with short dark hair, standing with arms outstretched. The boy is wearing red shorts with a white drawstring. Surrounding the boy are labeled boxes, each containing an illustration of a specific body part, connected to the corresponding part on the boy's body with red lines.\n\nAt the top, a blue banner with red ends displays the title \"BODY PARTS\" in bold white letters. The labeled body parts include:\n\n- **Head**: A smaller illustration of the boy's head.\n- **Eye**: A detailed drawing of an eye.\n- **Nose**: A simple depiction of a nose.\n- **Ear**: An illustration of an ear.\n- **Mouth**: A drawing of an open mouth with visible teeth.\n- **Arm**: A representation of an arm.\n- **Hand**: An illustration of an open hand.\n- **Leg**: A depiction of legs wearing red shorts.\n- **Knee**: A simple drawing of a knee.\n- **Foot**: An illustration of a foot.\n\nThe overall style is colorful and playful, making it suitable for educational purposes aimed at young children.",
              "height": 124.49385826771652,
              "left": 422.8572440944882,
              "ori_height": 1125,
              "ori_width": 1125,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_21_6.png",
              "tag": "Body Parts, Educational Illustration, Cartoon Style",
              "top": 182.4540157480315,
              "width": 159.59055118110237
            }
          ],
          "notes": null,
          "page": 21,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_21.png",
          "text": [
            "Follow the leader.",
            "",
            "",
            "feet",
            "10",
            "The learners need to figure out what they must touch. Read the added instruction to them. They wait until the instructions have been read and then they complete them.\nClick Back to main slide to continue.",
            "Back to main slide",
            "And touch your shoulders, then do a little dance."
          ],
          "title": null,
          "videos": []
        }
      ]
    },
    "status": "succeed"
  }
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

## GET PPT解析以及Goal生成

GET /attach/process

生成游戏，会自动根据当前game的状态执行下一步。如果已经生成了code，则重新生成。

> Body 请求参数

```json
{}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|attach_id|query|number| 是 |none|
|Authorization|header|string| 否 |none|
|body|body|object| 否 |none|

> 返回示例

> 200 Response

```json
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

## POST PPT状态更新

POST /attach/update_status

> Body 请求参数

```json
{
  "id": 0,
  "status": "string"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|Authorization|header|string| 否 |none|
|body|body|object| 否 |none|
|» id|body|number| 是 |ID 编号|
|» status|body|string| 是 |状态|

> 返回示例

> 200 Response

```json
{
  "code": 200,
  "msg": "query module json finished",
  "result": {
    "code": 200,
    "message": "parse ppt finished",
    "res": {
      "document_info": [
        {
          "audios": [],
          "images": [],
          "notes": "",
          "page": 1,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_1.png",
          "text": [],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image depicts a digital illustration of a soccer goal on a field. The goal is centrally positioned, featuring a white frame and a net with a grid pattern. The field is shown with a vibrant green color, marked with white lines indicating the penalty area and the penalty spot in front of the goal. The background is a gradient transitioning from dark blue to black, suggesting a night setting, possibly under stadium lights. The composition is symmetrical, focusing on the goal, and the style is clean and modern, suitable for use in sports-related digital media or games.",
              "height": 570.3156692913386,
              "left": 29.690236220472443,
              "ori_height": 1211,
              "ori_width": 2422,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_2_3.png",
              "tag": "Soccer Goal, Green Field, Night Setting",
              "top": -62.526299212598424,
              "width": 717.8088976377953
            },
            {
              "desp": "The image depicts an illustrated character of a young soccer player in mid-action. The player is wearing a maroon and light blue soccer uniform, consisting of a short-sleeved jersey and matching shorts. The jersey has light blue sleeves and a maroon body. The player is also wearing maroon knee-high socks and bright green soccer cleats with studs. The character is in a dynamic pose, balancing a soccer ball on their right knee, suggesting they are juggling or controlling the ball. The soccer ball is classic in design, featuring a pattern of black pentagons and white hexagons. The player's hair is brown and styled in a casual, slightly tousled manner. The background is plain, emphasizing the character and their action.",
              "height": 73.1076377952756,
              "left": 980.571496062992,
              "ori_height": 1920,
              "ori_width": 1920,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_2_5.png",
              "tag": "Soccer Player, Dynamic Pose, Maroon Uniform",
              "top": 59.219212598425194,
              "width": 76.4307874015748
            },
            {
              "desp": "The image depicts an illustrated character of a young soccer player in mid-action. The player is wearing a maroon and light blue soccer uniform, consisting of a short-sleeved jersey and shorts. The jersey features light blue sleeves and a maroon body, while the shorts are entirely maroon. The player is also wearing maroon knee-high socks and bright green soccer cleats with studs. The character is posed with one knee raised, balancing a classic black and white soccer ball on the thigh. The illustration style is clean and cartoonish, with simple lines and flat colors, suitable for animation or digital media use.",
              "height": 73.1076377952756,
              "left": 1073.8611023622047,
              "ori_height": 1920,
              "ori_width": 1920,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_2_6.png",
              "tag": "Soccer Player, Cartoon Style, Maroon Uniform",
              "top": 59.21913385826772,
              "width": 76.4307874015748
            },
            {
              "desp": "The image depicts an animated character of a young soccer player in mid-action. The player is wearing a maroon and light blue soccer uniform, consisting of a short-sleeved jersey and shorts. The jersey has light blue sleeves and a maroon body, while the shorts are entirely maroon. The player is also wearing maroon knee-high socks and bright green soccer cleats with white studs. The character is posed with one knee raised, balancing a soccer ball on the knee. The soccer ball is designed with a classic black and white hexagonal pattern. The overall style of the image is cartoonish and colorful, suitable for animation or digital media related to sports or children's content.",
              "height": 73.1076377952756,
              "left": 1167.1507086614174,
              "ori_height": 1920,
              "ori_width": 1920,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_2_7.png",
              "tag": "Soccer Player, Cartoon Style, Sports Animation",
              "top": 59.219055118110234,
              "width": 76.4307874015748
            },
            {
              "desp": "The image depicts an illustration of a young soccer player in mid-action, performing a juggling move with a soccer ball. The player is wearing a sports uniform consisting of a maroon jersey with light blue sleeves, matching maroon shorts, and maroon knee-high socks. The player is also wearing bright green soccer cleats with studs. The soccer ball is depicted in mid-air, just above the player's knee, suggesting a dynamic motion. The overall style of the illustration is cartoon-like, with clean lines and solid colors, suitable for use in animation or educational materials related to sports.",
              "height": 73.1076377952756,
              "left": 1257.228818897638,
              "ori_height": 1920,
              "ori_width": 1920,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_2_8.png",
              "tag": "Soccer Player, Juggling Move, Cartoon Illustration",
              "top": 59.219055118110234,
              "width": 76.4307874015748
            },
            {
              "desp": "The image depicts an illustrated character of a young soccer player in mid-action. The character is wearing a sports uniform consisting of a maroon jersey with light blue sleeves, matching maroon shorts, and maroon knee-high socks. The player is poised with one knee raised, balancing a classic black and white soccer ball on the knee. The character's footwear includes bright green soccer cleats with visible studs. The illustration style is clean and cartoon-like, suitable for animation or educational content related to sports.",
              "height": 73.1076377952756,
              "left": 993.0726771653544,
              "ori_height": 1920,
              "ori_width": 1920,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_2_9.png",
              "tag": "Soccer Player, Sports Uniform, Cartoon Illustration",
              "top": 233.30220472440945,
              "width": 76.4307874015748
            },
            {
              "desp": "The image depicts an illustrated character of a young soccer player in mid-action, performing a juggling move with a soccer ball. The player is wearing a sports uniform consisting of a maroon jersey with light blue sleeves, matching maroon shorts, and maroon knee-high socks. The character's shoes are bright green soccer cleats with visible studs. The soccer ball is designed with a classic black and white hexagonal pattern and is positioned near the player's raised knee, suggesting a juggling or dribbling motion. The overall style is cartoonish and colorful, suitable for animation or digital media aimed at a younger audience.",
              "height": 73.1076377952756,
              "left": 1073.8611023622047,
              "ori_height": 1920,
              "ori_width": 1920,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_2_10.png",
              "tag": "Soccer Player, Juggling Move, Cartoon Style",
              "top": 233.30212598425197,
              "width": 76.4307874015748
            },
            {
              "desp": "The image depicts an illustration of a young soccer player in mid-action, performing a juggling move with a soccer ball. The player is wearing a sports uniform consisting of a maroon jersey with light blue sleeves, matching maroon shorts, and maroon knee-high socks. The player is also wearing bright green soccer cleats with studs, suitable for playing on grass. The soccer ball is depicted in mid-air, featuring a classic black and white hexagonal pattern. The player's posture suggests they are balancing the ball on their knee, with one leg raised and both arms slightly bent at the elbows, indicating movement and coordination. The overall style of the illustration is cartoon-like, with bold colors and clean lines.",
              "height": 73.1076377952756,
              "left": 1167.1507086614174,
              "ori_height": 1920,
              "ori_width": 1920,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_2_11.png",
              "tag": "Soccer Player, Juggling Move, Cartoon Illustration",
              "top": 233.7427559055118,
              "width": 76.4307874015748
            },
            {
              "desp": "The image depicts an illustrated character of a young soccer player in mid-action. The player is wearing a sports uniform consisting of a maroon jersey with light blue sleeves, matching maroon shorts, and maroon knee-high socks. The character is poised with one knee raised, balancing a classic black and white soccer ball on the knee. The player is also wearing bright green soccer cleats with visible studs. The illustration style is simple and cartoon-like, with clean lines and solid colors, suitable for use in animation or educational materials related to sports.",
              "height": 73.1076377952756,
              "left": 1257.2287401574804,
              "ori_height": 1920,
              "ori_width": 1920,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_2_12.png",
              "tag": "Soccer Player, Sports Uniform, Cartoon Illustration",
              "top": 231.17133858267715,
              "width": 76.4307874015748
            }
          ],
          "notes": null,
          "page": 2,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_2.png",
          "text": [
            "Warm up, warm up, everybody warm up.",
            "There are 8 soccer balls. Click to have one ball bounce in.  \nClick on the ball to be directed to an action slide. When you return to this slide, repeat the clicks.\nOnce 8 balls have been actioned, click the arrow to continue. ",
            "",
            ""
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image depicts a digital illustration of a soccer goal on a field. The goal is centrally positioned and features a white frame with a net that is neatly divided into a grid pattern. The field is a vibrant green with clearly marked white lines, including the penalty arc and the penalty spot in front of the goal. The background is a dark gradient, transitioning from black at the top to a deep blue behind the goal, suggesting a night setting. The composition is symmetrical, focusing on the goal, and the lighting creates a subtle spotlight effect on the field, enhancing the centrality of the goal. This image could be used as a background or asset in a sports-related digital media project, such as a video game or animation.",
              "height": 570.3156692913386,
              "left": 29.690236220472443,
              "ori_height": 1211,
              "ori_width": 2422,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_3_3.png",
              "tag": "Soccer Goal, Night Setting, Digital Illustration",
              "top": -62.526299212598424,
              "width": 717.8088976377953
            },
            {
              "desp": "The image depicts a cartoon-style illustration of a martial artist performing a dynamic jumping kick. The character is wearing a traditional white karate gi with a black belt, indicating a high level of proficiency. The gi has long sleeves and pants, with the belt tied around the waist. The character's arms are bent with fists clenched, suggesting readiness and focus. The left leg is extended forward in a kicking motion, while the right leg is bent backward, contributing to the sense of movement and action. The character's hair is styled in a neat bun, secured with a pink hair tie. The overall style is clean and vibrant, suitable for animation or digital media focused on martial arts themes.",
              "height": 311.81102362204723,
              "left": 167.4448818897638,
              "ori_height": 1639,
              "ori_width": 2416,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_3_4.png",
              "tag": "Martial Artist, Jumping Kick, Karate Gi",
              "top": 78.48929133858267,
              "width": 459.5121259842519
            }
          ],
          "notes": null,
          "page": 3,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_3.png",
          "text": [
            "Warm up, warm up, everybody warm up.",
            "Read the question / action to the learners.\nThey pretend to be doing the action. \nClick Back to main slide to continue. ",
            "",
            "Can you kick like her? Kick four times.",
            "Back to main slide"
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image depicts a digital illustration of a soccer goal on a field. The goal is centrally positioned and features a white frame with a net composed of a grid pattern. The field is shown with a vibrant green surface, marked with white lines indicating the penalty area and the center circle. The perspective is from the viewpoint of a player approaching the goal, emphasizing the goal's prominence. The background is a dark gradient, transitioning from black at the top to a subtle blue near the goal, suggesting a stadium setting under artificial lighting. The overall style is clean and modern, suitable for use in sports-related digital media or UI design, such as a game interface or sports app.",
              "height": 570.3156692913386,
              "left": 29.690236220472443,
              "ori_height": 1211,
              "ori_width": 2422,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_4_3.png",
              "tag": "Soccer Goal, Digital Illustration, Sports UI Design",
              "top": -62.526299212598424,
              "width": 717.8088976377953
            },
            {
              "desp": "The image is a cartoon-style illustration featuring a young boy energetically jumping over two tires. The boy has short brown hair and is wearing a bright blue t-shirt, brown shorts, and red shoes. His expression is cheerful and animated, suggesting excitement or playfulness. The two tires are positioned on the ground, slightly apart from each other, and are depicted in a realistic style with visible treads. The background is transparent, indicating that this image could be used as an animation asset or in digital media where the character and objects can be placed over different backgrounds. The overall style is colorful and playful, suitable for children's content or educational materials.",
              "height": 311.81102362204723,
              "left": 302.3056692913386,
              "ori_height": 1651,
              "ori_width": 1659,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_4_4.png",
              "tag": "Cartoon Boy, Jumping Tires, Children's Illustration",
              "top": 119.14551181102362,
              "width": 177.69433070866145
            }
          ],
          "notes": null,
          "page": 4,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_4.png",
          "text": [
            "Warm up, warm up, everybody warm up.",
            "Read the question / action to the learners.\nThey pretend to be doing the action. \nClick Back to main slide to continue. ",
            "",
            "Can you jump like him? Jump over six tyres.",
            "Back to main slide"
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image depicts a digital illustration of a soccer goal set against a dark background, likely intended for use in sports-related digital media or a video game. The scene is centered on a standard soccer goal with a white frame and net, positioned on a green soccer field. The field is marked with white lines, including the penalty arc and spot, indicating the area in front of the goal. The perspective is from the center of the field, directly facing the goal, creating a symmetrical composition. The lighting is focused on the goal and the immediate area of the field, with the background fading into darkness, suggesting a spotlight effect often used in sports graphics to emphasize the goal area.",
              "height": 570.3156692913386,
              "left": 29.690236220472443,
              "ori_height": 1211,
              "ori_width": 2422,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_5_3.png",
              "tag": "Soccer Goal, Digital Illustration, Spotlight Effect",
              "top": -62.526299212598424,
              "width": 717.8088976377953
            },
            {
              "desp": "The image features a cartoon-style illustration of a young girl with a cheerful expression. She has bright orange hair styled in a bob cut with a small hair tuft on top. Her eyes are large and blue, adding to her animated appearance. She is wearing a yellow shirt with a blue bow at the collar and a short red skirt. Her outfit is completed with purple shoes and matching socks. The girl is depicted in a playful pose, standing on one leg with her arms outstretched to the sides, suggesting a sense of balance or dance. The background is transparent, making the character suitable for use as an animation asset or in digital media where she can be placed over various backgrounds.",
              "height": 311.81102362204723,
              "left": 323.2340157480315,
              "ori_height": 1651,
              "ori_width": 1659,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_5_4.png",
              "tag": "Cartoon Girl, Orange Hair, Playful Pose",
              "top": 171.93897637795277,
              "width": 156.7659842519685
            }
          ],
          "notes": null,
          "page": 5,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_5.png",
          "text": [
            "Warm up, warm up, everybody warm up.",
            "Read the question / action to the learners.\nThey pretend to be doing the action. \nClick Back to main slide to continue. ",
            "",
            "Can you hop like her? Hop fives times.",
            "Back to main slide"
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image depicts a stylized representation of a soccer field focusing on the goal area. The foreground features a well-defined, green grass pitch with white markings indicating the penalty box and the goal area. The central focus is on the soccer goal, which is prominently displayed with a white frame and netting. The net is detailed with a grid pattern, and the goalposts are positioned centrally within the image. The background is a gradient transitioning from dark blue to black, suggesting a night setting or an indoor stadium environment. The composition is symmetrical, emphasizing the goal as the main element, suitable for use in sports-related digital media or as a background for soccer-themed applications.",
              "height": 570.3156692913386,
              "left": 29.690236220472443,
              "ori_height": 1211,
              "ori_width": 2422,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_6_3.png",
              "tag": "Soccer Field, Goal Area, Night Setting",
              "top": -62.526299212598424,
              "width": 717.8088976377953
            },
            {
              "desp": "The image depicts a cartoon-style illustration of a young boy standing on a small patch of grass. He is wearing a blue baseball cap with an orange underside, a yellow and white striped t-shirt, dark blue shorts, and blue sneakers with green soles. The boy is positioned as if he is about to catch a red cricket ball, which is shown in mid-air with a motion line indicating its trajectory. The grass patch is oval-shaped with a few small flowers and leaves scattered on it, adding a playful outdoor setting to the scene.",
              "height": 311.81102362204723,
              "left": 122.7903937007874,
              "ori_height": 1639,
              "ori_width": 2416,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_6_4.png",
              "tag": "Cartoon Boy, Cricket Ball, Outdoor Scene",
              "top": 137.1,
              "width": 459.51141732283463
            }
          ],
          "notes": null,
          "page": 6,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_6.png",
          "text": [
            "Warm up, warm up, everybody warm up.",
            "Read the question / action to the learners.\nThey pretend to be doing the action. \nClick Back to main slide to continue. ",
            "",
            "Can you catch like him? Catch a ball three times.",
            "Back to main slide"
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image depicts a digital illustration of a soccer goal set against a dark background, which creates a dramatic contrast. The goal is centrally positioned and features a white frame with a net composed of evenly spaced squares. The netting is detailed with a subtle gradient, suggesting depth and dimension. In front of the goal, the foreground shows a section of a soccer field with a vibrant green color and white markings, including the penalty spot and part of the penalty arc. The field is illuminated, highlighting the goal area, while the surrounding area fades into darkness, emphasizing the focus on the goal itself. This image could be used as a background or asset in sports-related digital media or animation.",
              "height": 570.3156692913386,
              "left": 29.690236220472443,
              "ori_height": 1211,
              "ori_width": 2422,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_7_3.png",
              "tag": "Soccer Goal, Dark Background, Soccer Field",
              "top": -62.526299212598424,
              "width": 717.8088976377953
            },
            {
              "desp": "The image depicts a cartoon-style illustration of a young boy engaged in a playful activity. He is positioned on a small patch of grass, which is adorned with simple floral designs. The boy is wearing a dark navy blue t-shirt with a bold yellow geometric design on the chest. His attire includes light blue denim shorts with rolled-up cuffs and visible yellow stitching details. He is also wearing white socks and blue sneakers with yellow laces and soles. The boy is in a dynamic pose, with his arms extended as if he is about to catch or throw a red cricket ball that is in mid-air in front of him. The illustration is colorful and vibrant, with a playful and energetic theme suitable for animation or children's media.",
              "height": 311.81102362204723,
              "left": 160.1420472440945,
              "ori_height": 1639,
              "ori_width": 2416,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_7_4.png",
              "tag": "Cartoon Boy, Playful Activity, Cricket Ball, Colorful Illustration",
              "top": 159.41346456692912,
              "width": 456.9052755905512
            }
          ],
          "notes": null,
          "page": 7,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_7.png",
          "text": [
            "Warm up, warm up, everybody warm up.",
            "Read the question / action to the learners.\nThey pretend to be doing the action. \nClick Back to main slide to continue. ",
            "",
            "Can you throw like him? Throw the ball twice.",
            "Back to main slide"
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image depicts a digital illustration of a soccer goal on a field. The goal is centrally positioned and features a white frame with a net composed of evenly spaced horizontal and vertical lines, creating a grid pattern. The background is a dark gradient transitioning from black at the top to a deep blue, suggesting a nighttime or indoor setting. The soccer field is shown in a vibrant green color, with white markings indicating the penalty area, the penalty spot, and the arc of the penalty box. The perspective is from the center of the field facing the goal, emphasizing the goal's structure and the field's layout. The image is likely designed for use in sports-related digital media, such as a game or animation asset, focusing on the goal area.",
              "height": 570.3156692913386,
              "left": 29.690236220472443,
              "ori_height": 1211,
              "ori_width": 2422,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_8_3.png",
              "tag": "Soccer Goal, Digital Illustration, Nighttime Setting",
              "top": -62.526299212598424,
              "width": 717.8088976377953
            },
            {
              "desp": "The image is a cartoon-style illustration of a cheerful young boy jumping rope. The boy has curly brown hair and is depicted with a wide, joyful smile, with his eyes closed in delight. He is wearing a green sleeveless shirt and blue pants, along with brown shoes. The jump rope is orange with blue handles, and the boy is holding it in both hands, mid-jump, with his legs spread apart in a playful manner. The illustration has a bright and lively color palette, emphasizing a sense of fun and energy, suitable for children's media or educational content.",
              "height": 311.81102362204723,
              "left": 217.6596850393701,
              "ori_height": 1092,
              "ori_width": 1092,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_8_4.png",
              "tag": "Cartoon Boy, Jump Rope, Children's Illustration",
              "top": 119.14551181102362,
              "width": 311.81102362204723
            }
          ],
          "notes": null,
          "page": 8,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_8.png",
          "text": [
            "Warm up, warm up, everybody warm up.",
            "Read the question / action to the learners.\nThey pretend to be doing the action. \nClick Back to main slide to continue. ",
            "",
            "Can you skip like him? Skip eight times.",
            "Back to main slide"
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image depicts a digital illustration of a soccer goal set against a dark background. The goal is centrally positioned, featuring a white frame and a net composed of evenly spaced squares. The netting is detailed with a subtle gradient, suggesting depth and dimension. In front of the goal is a section of a soccer field, characterized by a vibrant green color and marked with white lines indicating the penalty area and the penalty spot. The field lines include the arc of the penalty area and the center circle, providing context for the goal's placement within a soccer field. The overall composition is simple and focused, with the goal and field elements prominently displayed against the stark black background, which enhances the contrast and visibility of the soccer elements. This image could be used in sports-related digital media, such as a game interface or animation asset.",
              "height": 570.3156692913386,
              "left": 29.690236220472443,
              "ori_height": 1211,
              "ori_width": 2422,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_9_3.png",
              "tag": "Soccer Goal, Penalty Area, Digital Illustration",
              "top": -62.526299212598424,
              "width": 717.8088976377953
            },
            {
              "desp": "The image is a cartoon-style illustration of a young girl in motion, depicted as if she is running or skipping. She has bright orange hair styled in a high ponytail, secured with a purple hair tie. Her facial expression is joyful, with a wide smile showing her teeth and her eyes looking forward. The girl is wearing a pink t-shirt with a darker pink outline, purple shorts, and blue sneakers with white soles. Her socks are white and visible above her shoes. The illustration includes motion lines near her feet, emphasizing her movement. The overall style is vibrant and playful, suitable for use in children's animation or educational content. The background is transparent, allowing for easy integration into various digital media.",
              "height": 311.81102362204723,
              "left": 266.5249606299213,
              "ori_height": 1649,
              "ori_width": 2361,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_9_4.png",
              "tag": "Cartoon Girl, Running, Vibrant Illustration",
              "top": 119.14551181102362,
              "width": 244.13937007874017
            }
          ],
          "notes": null,
          "page": 9,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_9.png",
          "text": [
            "Warm up, warm up, everybody warm up.",
            "Read the question / action to the learners.\nThey pretend to be doing the action. \nClick Back to main slide to continue. ",
            "",
            "Can you run like her? Run on the spot for 10 counts.",
            "Back to main slide"
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image depicts a stylized soccer field with a focus on the goal area. The foreground features a green grass pitch with white markings, including the penalty arc and spot, indicating the area directly in front of the goal. The goal itself is centrally positioned, with a white frame and netting, creating a grid pattern. The background is a dark gradient transitioning from black at the top to a deep blue near the goal, suggesting a night-time setting or an indoor stadium environment. The composition is symmetrical, emphasizing the goal as the central element, and the lighting effect adds depth and focus to the scene. This image could be used in digital media related to sports, such as a video game or animation asset, where the goal area is a key visual component.",
              "height": 570.3156692913386,
              "left": 29.690236220472443,
              "ori_height": 1211,
              "ori_width": 2422,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_10_3.png",
              "tag": "Soccer Field, Goal Area, Night Setting",
              "top": -62.526299212598424,
              "width": 717.8088976377953
            },
            {
              "desp": "The image depicts an animated character of a young child from a rear view, appearing to be in a climbing or reaching pose. The child is wearing a colorful, segmented cap with red, blue, and yellow sections. The child has brown hair styled in a single braid that extends down the back. They are dressed in a white t-shirt and light blue shorts. The child is also wearing bright green sneakers with white soles and yellow socks. The character's arms are raised, and one knee is bent, suggesting movement or an action-oriented pose. The illustration style is cartoonish, with bold outlines and vibrant colors, suitable for use in children's media or educational animations.",
              "height": 311.81102362204723,
              "left": 277.38818897637793,
              "ori_height": 892,
              "ori_width": 1185,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_10_5.png",
              "tag": "Animated Character, Colorful Cap, Cartoon Style",
              "top": 105.47763779527558,
              "width": 207.95661417322836
            }
          ],
          "notes": null,
          "page": 10,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_10.png",
          "text": [
            "Warm up, warm up, everybody warm up.",
            "Read the question / action to the learners.\nThey pretend to be doing the action. \nClick Back to main slide to continue. ",
            "",
            "Back to main slide",
            "Can you climb like her? Climb up one rock."
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [],
          "notes": null,
          "page": 11,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_11.png",
          "text": [
            "Follow the leader.",
            "The learners take turns choosing a number around the body. Click on the number chosen to be directed to a slide with an action.  \nContinue playing until all numbers have been selected and the children are able to follow all the instructions.  \n\nClick the arrow to end.\nThis is the last slide.",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            ""
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [],
          "notes": null,
          "page": 12,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_12.png",
          "text": [
            "Follow the leader.",
            "The learners need to figure out what they must touch. Read the added instruction to them. They wait until the instructions have been read and then they complete them.\nClick Back to main slide to continue.",
            "1",
            "Back to main slide",
            "And pick up your pencil.."
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image is an educational illustration designed to teach children about different body parts. It features a cartoon-style depiction of a young boy standing with arms outstretched, wearing red shorts. The boy has brown hair, large blue eyes, and a cheerful expression. Surrounding the boy are labeled boxes, each containing an illustration of a specific body part. \n\n- At the top, a blue banner with red accents displays the title \"BODY PARTS\" in bold white letters.\n- On the left side, boxes labeled \"EYE,\" \"NOSE,\" \"ARM,\" \"LEG,\" and \"KNEE\" are connected to the corresponding parts on the boy's body with red lines.\n- On the right side, boxes labeled \"HEAD,\" \"EAR,\" \"MOUTH,\" \"HAND,\" and \"FOOT\" similarly connect to the respective body parts.\n- Each box contains a simple illustration of the body part, matching the cartoon style of the central figure.\n\nThe image uses bright colors and clear labeling to make it engaging and easy for children to understand and identify different body parts.",
              "height": 180.49330708661415,
              "left": 414.38732283464566,
              "ori_height": 1125,
              "ori_width": 1125,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_13_0.png",
              "tag": "Body Parts, Educational Illustration, Cartoon Boy",
              "top": 182.74346456692913,
              "width": 175.5828346456693
            }
          ],
          "notes": null,
          "page": 13,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_13.png",
          "text": [
            "Follow the leader.",
            "",
            "",
            "nose",
            "2",
            "The learners need to figure out what they must touch. Read the added instruction to them. They wait until the instructions have been read and then they complete them.\nClick Back to main slide to continue.",
            "Back to main slide",
            "And put your right hand behind your back.."
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image is an educational illustration designed to teach children about human body parts. It features a cartoon-style depiction of a young boy with short dark hair, standing with arms outstretched. The boy is wearing red shorts with a white drawstring. Surrounding the boy are labeled boxes, each containing an illustration of a specific body part. These boxes are connected to the corresponding parts on the boy's body with red lines. \n\nThe body parts identified include:\n\n- **Head**: Illustrated with a smaller version of the boy's face.\n- **Eye**: A large, cartoon-style eye with eyelashes.\n- **Ear**: A simplified illustration of an ear.\n- **Nose**: A basic depiction of a nose.\n- **Mouth**: A smiling mouth showing teeth.\n- **Arm**: A simplified illustration of an arm.\n- **Hand**: A cartoon-style hand with fingers spread.\n- **Leg**: A depiction of legs wearing shorts.\n- **Knee**: A basic illustration of a knee.\n- **Foot**: A simplified depiction of a foot.\n\nAt the top of the image, there is a banner with a blue background and orange ribbon ends, containing the text \"BODY PARTS\" in bold white letters. The overall style is colorful and playful, suitable for educational purposes aimed at young children.",
              "height": 186.6892125984252,
              "left": 405.5370866141732,
              "ori_height": 1125,
              "ori_width": 1125,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_14_0.png",
              "tag": "Human Body Parts, Educational Illustration, Cartoon Style",
              "top": 177.91425196850395,
              "width": 185.5076377952756
            }
          ],
          "notes": null,
          "page": 14,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_14.png",
          "text": [
            "Follow the leader.",
            "",
            "",
            "left arm",
            "3",
            "The learners need to figure out what they must touch. Read the added instruction to them. They wait until the instructions have been read and then they complete them.\nClick Back to main slide to continue.",
            "Back to main slide",
            "And skip around three times on the spot."
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image is an educational illustration designed to teach children about different body parts. It features a cartoon-style depiction of a young boy with short brown hair, standing with arms outstretched. The boy is wearing red shorts with a white drawstring, and he is barefoot.\n\nSurrounding the boy are labeled boxes, each containing an illustration of a specific body part. Lines connect each box to the corresponding part on the boy's body. The labeled body parts include:\n\n1. **Head**: A smaller image of the boy's head.\n2. **Eye**: A single eye with eyelashes.\n3. **Nose**: A simple depiction of a nose.\n4. **Ear**: An illustration of an ear.\n5. **Mouth**: A smiling mouth with visible teeth.\n6. **Arm**: A single arm extended outward.\n7. **Hand**: An open hand with fingers spread.\n8. **Leg**: A pair of legs wearing shorts.\n9. **Knee**: A bent knee.\n10. **Foot**: A single foot.\n\nAt the top of the image, there is a blue banner with orange accents that reads \"BODY PARTS\" in bold white letters. The overall style is colorful and playful, making it suitable for educational purposes aimed at young children.",
              "height": 190.0976377952756,
              "left": 405.790157480315,
              "ori_height": 1125,
              "ori_width": 1125,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_15_0.png",
              "tag": "Body Parts, Educational Illustration, Cartoon Boy",
              "top": 179.43212598425197,
              "width": 185.25464566929136
            }
          ],
          "notes": null,
          "page": 15,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_15.png",
          "text": [
            "Follow the leader.",
            "",
            "",
            "upper leg",
            "4",
            "The learners need to figure out what they must touch. Read the added instruction to them. They wait until the instructions have been read and then they complete them.\nClick Back to main slide to continue.",
            "Back to main slide",
            "Hold it and walk around in a circle."
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image is an educational illustration designed to teach children about different body parts. It features a cartoon-style drawing of a young boy with a cheerful expression, standing with arms outstretched. The boy is wearing red shorts with a white drawstring and is depicted with short, dark hair and blue eyes.\n\nSurrounding the boy are labeled boxes, each containing an illustration of a specific body part. These boxes are connected to the corresponding parts on the boy's body with red lines. The labeled body parts include:\n\n- **Head**: A smaller illustration of the boy's head.\n- **Eye**: A close-up of a single eye.\n- **Nose**: A depiction of a nose.\n- **Ear**: An illustration of an ear.\n- **Mouth**: A drawing of an open mouth with visible teeth.\n- **Arm**: An image of an arm.\n- **Hand**: A depiction of a hand.\n- **Leg**: An illustration of legs wearing red shorts.\n- **Knee**: A drawing of a knee.\n- **Foot**: An image of a foot.\n\nAt the top of the image, there is a blue banner with the text \"BODY PARTS\" in white, flanked by red ribbon-like accents. The overall style is colorful and playful, suitable for a young audience, with clear and simple illustrations to aid in learning.",
              "height": 188.8404724409449,
              "left": 405.790157480315,
              "ori_height": 1125,
              "ori_width": 1125,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_16_0.png",
              "tag": "Body Parts, Educational Illustration, Cartoon Boy, Labeled Diagram, Children's Learning",
              "top": 179.22283464566928,
              "width": 185.25464566929136
            }
          ],
          "notes": null,
          "page": 16,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_16.png",
          "text": [
            "Follow the leader.",
            "",
            "",
            "right knee",
            "5",
            "The learners need to figure out what they must touch. Read the added instruction to them. They wait until the instructions have been read and then they complete them.\nClick Back to main slide to continue.",
            "Back to main slide",
            "And criss cross your legs four times."
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image is an educational illustration designed to teach children about different body parts. It features a cartoon-style, smiling boy with short dark hair, standing with arms outstretched. The boy is wearing red shorts with a white drawstring. Surrounding the boy are labeled boxes, each connected to a specific body part with a red line. \n\nThe labels and corresponding body parts are as follows:\n- \"HEAD\" with an illustration of a head.\n- \"EYE\" with an illustration of an eye.\n- \"NOSE\" with an illustration of a nose.\n- \"EAR\" with an illustration of an ear.\n- \"MOUTH\" with an illustration of a mouth.\n- \"ARM\" with an illustration of an arm.\n- \"HAND\" with an illustration of a hand.\n- \"LEG\" with an illustration of legs.\n- \"KNEE\" with an illustration of a knee.\n- \"FOOT\" with an illustration of a foot.\n\nAt the top of the image, there is a blue banner with the text \"BODY PARTS\" in bold white letters, flanked by orange ribbon-like accents. The overall style is colorful and playful, suitable for a young audience, and aims to visually associate each body part with its name.",
              "height": 185.04818897637796,
              "left": 405.790157480315,
              "ori_height": 1125,
              "ori_width": 1125,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_17_0.png",
              "tag": "Body Parts, Educational Illustration, Cartoon Boy",
              "top": 179.2063779527559,
              "width": 184.28692913385828
            }
          ],
          "notes": null,
          "page": 17,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_17.png",
          "text": [
            "Follow the leader.",
            "",
            "",
            "head",
            "6",
            "The learners need to figure out what they must touch. Read the added instruction to them. They wait until the instructions have been read and then they complete them.\nClick Back to main slide to continue.",
            "Back to main slide",
            "And do seven jumping jacks."
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image is an educational illustration designed to teach children about different body parts. It features a cartoon-style depiction of a young boy with short dark hair, standing with arms outstretched. The boy is wearing red shorts with a white drawstring and is barefoot. Surrounding the boy are labeled boxes that identify various body parts. Each box contains an illustration of the specific body part and is connected to the corresponding part on the boy's body with a red line. The labeled body parts include:\n\n- **Head**: A smaller illustration of the boy's head.\n- **Eye**: A close-up of a single eye.\n- **Nose**: An illustration of a nose.\n- **Ear**: A depiction of an ear.\n- **Mouth**: An image showing a smiling mouth with teeth.\n- **Arm**: An illustration of an arm.\n- **Hand**: A depiction of a hand with fingers spread.\n- **Leg**: An illustration of legs wearing shorts.\n- **Knee**: A depiction of a knee.\n- **Foot**: An illustration of a foot.\n\nAt the top of the image, there is a blue banner with the text \"BODY PARTS\" in bold white letters, flanked by red ribbon-like accents. The overall style is colorful and playful, suitable for a young audience, and aims to make learning about body parts engaging and accessible.",
              "height": 190.22669291338585,
              "left": 410.5299212598425,
              "ori_height": 1125,
              "ori_width": 1125,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_18_0.png",
              "tag": "Body Parts, Educational Illustration, Cartoon Style",
              "top": 178.46795275590551,
              "width": 177.29110236220473
            }
          ],
          "notes": null,
          "page": 18,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_18.png",
          "text": [
            "Follow the leader.",
            "",
            "",
            "left ear",
            "",
            "Touch\nyour\n",
            "",
            "7",
            "The learners need to figure out what they must touch. Read the added instruction to them. They wait until the instructions have been read and then they complete them.\nClick Back to main slide to continue.",
            "Back to main slide",
            "And touch your toes, then put your hands on your hips."
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image is an educational illustration designed to teach children about different body parts. It features a cartoon-style depiction of a young boy standing with arms outstretched, wearing red shorts. The boy has a cheerful expression with large eyes, a wide smile, and short brown hair. Surrounding the boy are labeled boxes, each containing an illustration of a specific body part and its corresponding label. The body parts highlighted include:\n\n- **Eye**: Illustrated with a large eye and labeled \"EYE.\"\n- **Nose**: Depicted with a simple nose illustration and labeled \"NOSE.\"\n- **Arm**: Shown with an extended arm and labeled \"ARM.\"\n- **Leg**: Illustrated with a pair of legs wearing shorts and labeled \"LEG.\"\n- **Knee**: Depicted with a bent knee and labeled \"KNEE.\"\n- **Head**: Illustrated with a smaller version of the boy's head and labeled \"HEAD.\"\n- **Ear**: Shown with a detailed ear illustration and labeled \"EAR.\"\n- **Mouth**: Depicted with a smiling mouth showing teeth and labeled \"MOUTH.\"\n- **Hand**: Illustrated with an open hand and labeled \"HAND.\"\n- **Foot**: Shown with a foot illustration and labeled \"FOOT.\"\n\nAt the top of the image, there is a banner with a blue background and red accents, displaying the title \"BODY PARTS\" in bold white letters. The image uses bright colors and simple shapes",
              "height": 119.7472440944882,
              "left": 426.4974015748032,
              "ori_height": 1125,
              "ori_width": 1125,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_19_6.png",
              "tag": "Body Parts, Educational Illustration, Cartoon Boy",
              "top": 192.41496062992127,
              "width": 150.30787401574804
            }
          ],
          "notes": null,
          "page": 19,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_19.png",
          "text": [
            "Follow the leader.",
            "",
            "",
            "mouth",
            "8",
            "The learners need to figure out what they must touch. Read the added instruction to them. They wait until the instructions have been read and then they complete them.\nClick Back to main slide to continue.",
            "Back to main slide",
            "And stick out your tongue, then bend to your left side."
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image is an educational illustration designed to teach children about different body parts. It features a cartoon-style depiction of a young boy with short dark hair, standing with his arms outstretched. The boy is wearing red shorts with a white drawstring. Surrounding the boy are labeled boxes, each containing an illustration of a specific body part. \n\n- At the top, a blue banner with orange accents reads \"BODY PARTS\" in bold white letters.\n- The body parts labeled include:\n  - \"HEAD\" with a small illustration of the boy's head.\n  - \"EYE\" with a close-up of an eye.\n  - \"NOSE\" with an illustration of a nose.\n  - \"EAR\" with an illustration of an ear.\n  - \"MOUTH\" with an illustration of a smiling mouth showing teeth.\n  - \"ARM\" with an illustration of an arm.\n  - \"HAND\" with an illustration of a hand.\n  - \"LEG\" with an illustration of legs wearing red shorts.\n  - \"KNEE\" with an illustration of a knee.\n  - \"FOOT\" with an illustration of a foot.\n\nEach body part is connected to the corresponding area on the boy's body with a red line, helping to visually associate the label with the actual body part. The overall style is colorful, friendly, and engaging, suitable for a young audience.",
              "height": 121.22338582677165,
              "left": 414.38732283464566,
              "ori_height": 1125,
              "ori_width": 1125,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_20_6.png",
              "tag": "Body Parts, Educational Illustration, Cartoon Boy",
              "top": 183.88551181102363,
              "width": 180.49307086614172
            }
          ],
          "notes": null,
          "page": 20,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_20.png",
          "text": [
            "Follow the leader.",
            "",
            "",
            "hand",
            "9",
            "The learners need to figure out what they must touch. Read the added instruction to them. They wait until the instructions have been read and then they complete them.\nClick Back to main slide to continue.",
            "Back to main slide",
            "And nod your head twice, then sit back down."
          ],
          "title": null,
          "videos": []
        },
        {
          "audios": [],
          "images": [
            {
              "desp": "The image is an educational illustration designed to teach children about different body parts. It features a cartoon-style depiction of a young boy with short dark hair, standing with arms outstretched. The boy is wearing red shorts with a white drawstring. Surrounding the boy are labeled boxes, each containing an illustration of a specific body part, connected to the corresponding part on the boy's body with red lines.\n\nAt the top, a blue banner with red ends displays the title \"BODY PARTS\" in bold white letters. The labeled body parts include:\n\n- **Head**: A smaller illustration of the boy's head.\n- **Eye**: A detailed drawing of an eye.\n- **Nose**: A simple depiction of a nose.\n- **Ear**: An illustration of an ear.\n- **Mouth**: A drawing of an open mouth with visible teeth.\n- **Arm**: A representation of an arm.\n- **Hand**: An illustration of an open hand.\n- **Leg**: A depiction of legs wearing red shorts.\n- **Knee**: A simple drawing of a knee.\n- **Foot**: An illustration of a foot.\n\nThe overall style is colorful and playful, making it suitable for educational purposes aimed at young children.",
              "height": 124.49385826771652,
              "left": 422.8572440944882,
              "ori_height": 1125,
              "ori_width": 1125,
              "path": "/data/upload/ppt/extract/1745388183.708568/image_21_6.png",
              "tag": "Body Parts, Educational Illustration, Cartoon Style",
              "top": 182.4540157480315,
              "width": 159.59055118110237
            }
          ],
          "notes": null,
          "page": 21,
          "screenshot": "/data/upload/ppt/21c3cd95-3b49-48e2-93c6-01ade09942ec/convert/images/page_21.png",
          "text": [
            "Follow the leader.",
            "",
            "",
            "feet",
            "10",
            "The learners need to figure out what they must touch. Read the added instruction to them. They wait until the instructions have been read and then they complete them.\nClick Back to main slide to continue.",
            "Back to main slide",
            "And touch your shoulders, then do a little dance."
          ],
          "title": null,
          "videos": []
        }
      ]
    },
    "status": "succeed"
  }
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

## POST 文本转语音

POST /proxy/tts

> Body 请求参数

```json
{
  "lang": "en-US",
  "speaker": "en-US-AvaMultilingualNeural",
  "emotion": {
    "style": "cheerful",
    "degree": 0.8,
    "role": "YoungAdultFemale"
  },
  "content": "Welcome to our intelligent game assistant. Let's get started!",
  "rate": "fast",
  "volume": "loud"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|Authorization|header|string| 否 |none|
|body|body|object| 否 |none|
|» lang|body|string| 否 |none|
|» speaker|body|string| 否 |none|
|» emotion|body|object| 否 |none|
|»» style|body|string| 是 |none|
|»» degree|body|number| 是 |none|
|»» role|body|string| 是 |none|
|» content|body|string| 是 |none|
|» rate|body|string| 否 |none|
|» volume|body|string| 否 |none|

> 返回示例

> 200 Response

```json
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

## POST 图像生成

POST /proxy/image/gen

> Body 请求参数

```json
{
  "prompt": "string"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|Authorization|header|string| 否 |none|
|body|body|object| 否 |none|
|» prompt|body|string| 是 |none|

> 返回示例

> 200 Response

```json
{
  "status": "string",
  "code": 0,
  "msg": "string",
  "result": [
    "string"
  ]
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» status|string|true|none||none|
|» code|integer|true|none||none|
|» msg|string|true|none||none|
|» result|[string]|true|none||none|

## DELETE 删除游戏

DELETE /game

支持指定游戏id和指定ppt id删除，指定ppt id删除为删除该ppt生成的所有游戏

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|attach_id|query|number| 否 |ppt id，不加参数则查询所有|
|id|query|number| 否 |ID 编号|
|Authorization|header|string| 否 |none|

> 返回示例

> 200 Response

```json
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

## GET 游戏模块重新生成

GET /game/regen/{id}/{status}

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|number| 是 |game id|
|status|path|string| 是 |game status to generate: plan/code|
|Authorization|header|string| 否 |none|

> 返回示例

> 200 Response

```json
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

## POST Runway视频生成

POST /proxy/video/runway

> Body 请求参数

```json
{
  "model": "gen3a_turbo",
  "image_url": "https://api.gamecreator.online/data/upload/assets/image/4396dc20-9852-4621-a83d-383dc4931382/0.jpg",
  "prompt_text": "Generate a video",
  "ratio": "1280:768",
  "duration": 10
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|Authorization|header|string| 否 |none|
|body|body|object| 否 |none|
|» model|body|string| 否 |none|
|» image_url|body|string| 是 |图像url或者base64|
|» prompt_text|body|string| 是 |提示词|
|» ratio|body|string| 否 |分辨率|
|» duration|body|number| 否 |时长|

#### 枚举值

|属性|值|
|---|---|
|» model|gen4_turbo|
|» model|gen3a_turbo|
|» ratio|1280:720|
|» ratio|720:1280|
|» ratio|1104:832|
|» ratio|832:1104|
|» ratio|960:960|
|» ratio|1584:672|
|» ratio|1280:768|
|» ratio|768:1280|
|» duration|5|
|» duration|10|

> 返回示例

> 200 Response

```json
{
  "status": "succeed",
  "code": 200,
  "msg": "image-to-video task finished, see result for status",
  "result": [
    "https://api.gamecreator.online/data/upload/assets/video/11670ff2-d2b8-4cac-8fda-ca2e977aaee8/0.mp4"
  ]
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» status|string|true|none||none|
|» code|integer|true|none||none|
|» msg|string|true|none||none|
|» result|[string]|true|none||none|

# 数据模型

<h2 id="tocS_Goal">Goal</h2>

<a id="schemagoal"></a>
<a id="schema_Goal"></a>
<a id="tocSgoal"></a>
<a id="tocsgoal"></a>

```json
{
  "modules": [
    {
      "module_id": 0,
      "start_page": 0,
      "end_page": 0,
      "game_goal": "string",
      "evidence": [
        {
          "page": 0,
          "text_excerpt": "string",
          "image_summary": "string"
        }
      ]
    }
  ]
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|modules|[object]|true|none||none|
|» module_id|integer|true|none||none|
|» start_page|integer|true|none||none|
|» end_page|integer|true|none||none|
|» game_goal|string|true|none||none|
|» evidence|[object]|true|none||none|
|»» page|integer|true|none||none|
|»» text_excerpt|string|true|none||none|
|»» image_summary|string|true|none||none|

<h2 id="tocS_Plan">Plan</h2>

<a id="schemaplan"></a>
<a id="schema_Plan"></a>
<a id="tocSplan"></a>
<a id="tocsplan"></a>

```json
[
  {
    "module_id": 0,
    "game_name": "string",
    "core_gameplay_summary": "string",
    "features": {
      "core_mechanics": [
        "string"
      ],
      "input_logic": [
        "string"
      ],
      "ui_elements": [
        "string"
      ],
      "animations_assets": [
        "string"
      ],
      "audio_feedback": [
        "string"
      ]
    },
    "prototype_flow": [
      {
        "state": "string",
        "description": "string",
        "user_input": "string",
        "next_state": "string"
      }
    ],
    "estimated_duration_seconds": 0,
    "asset": [
      {
        "asset_name": "string",
        "type": "string",
        "prompt": "string",
        "resolution": "string",
        "duration": null,
        "fps": null,
        "reference": "string"
      }
    ]
  }
]

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|module_id|integer|true|none||none|
|game_name|string|true|none||none|
|core_gameplay_summary|string|true|none||none|
|features|object|true|none||none|
|» core_mechanics|[string]|true|none||none|
|» input_logic|[string]|true|none||none|
|» ui_elements|[string]|true|none||none|
|» animations_assets|[string]|true|none||none|
|» audio_feedback|[string]|true|none||none|
|prototype_flow|[object]|true|none||none|
|» state|string|true|none||none|
|» description|string|true|none||none|
|» user_input|string|true|none||none|
|» next_state|string|true|none||none|
|estimated_duration_seconds|integer|true|none||none|
|asset|[object]|true|none||none|
|» asset_name|string|true|none||none|
|» type|string|true|none||none|
|» prompt|string|true|none||none|
|» resolution|string|true|none||none|
|» duration|null|true|none||none|
|» fps|null|true|none||none|
|» reference|string|true|none||none|

<h2 id="tocS_Parse">Parse</h2>

<a id="schemaparse"></a>
<a id="schema_Parse"></a>
<a id="tocSparse"></a>
<a id="tocsparse"></a>

```json
[
  {
    "audios": [
      "string"
    ],
    "images": [
      {
        "desp": "string",
        "height": 0,
        "left": 0,
        "ori_height": 0,
        "ori_width": 0,
        "path": "string",
        "tag": "string",
        "top": 0,
        "width": 0
      }
    ],
    "notes": "string",
    "page": 0,
    "screenshot": "string",
    "text": [
      "string"
    ],
    "title": null,
    "videos": [
      "string"
    ]
  }
]

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|audios|[string]|true|none||none|
|images|[object]|true|none||none|
|» desp|string|true|none||none|
|» height|number|true|none||none|
|» left|number|true|none||none|
|» ori_height|integer|true|none||none|
|» ori_width|integer|true|none||none|
|» path|string|true|none||none|
|» tag|string|true|none||none|
|» top|number|true|none||none|
|» width|number|true|none||none|
|notes|string¦null|true|none||none|
|page|integer|true|none||none|
|screenshot|string|true|none||none|
|text|[string]|true|none||none|
|title|null|true|none||none|
|videos|[string]|true|none||none|

