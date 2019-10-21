# flask-kingadmin后台管理模板

## 1. 将king_admin和static文件夹复制到自己目录

## 2. 在项目中创建任意一个py文件

```python
#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import sys

import wtforms
from flask import jsonify, request
from flask_wtf import FlaskForm
from wtforms import validators

from king_admin import admin
from king_admin import fields
from king_admin.utils import json_response
from king_admin.service.core import BaseView


class StaffForm(FlaskForm):
    # 用于增加数据时，form表单的生成和校验
    # 用法参见 flask-wtf  https://flask-wtf.readthedocs.io/en/stable/
    username = wtforms.StringField('Username', [validators.Length(min=4, max=25)], render_kw={"class": "form-control"})
    email = wtforms.StringField('Email Address', [validators.Length(min=6, max=35)],
                                render_kw={"class": "form-control"})
    password = wtforms.PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='两次密码必须一致')
    ], render_kw={"class": "form-control"})
    confirm = wtforms.PasswordField('Repeat Password', render_kw={"class": "form-control"})
    accept_tos = wtforms.BooleanField('I accept the TOS', [validators.DataRequired()])


class Index(BaseView):
    title = "这是标题" # html页面显示的标题
    data_url = "/index/data" 
    # bootstrap-table请求数据api
    # 该api返回值必须是列表套字典形式 
    list_display = [("Id", "id"), ("名字", "name"), ("价格", "price")]
    # bootstrap-table展示字段
    # 元组第一项：表格显示标题，第二项：数据api对应字典的key
    checkbox = True
    # bootstrap-table是否可选，默认False
    search_fields = [
        fields.TextField("Id", "id", "用户id"),
        fields.DateField("开始日期", "startdate"),
        fields.TimeField("开始时间", "starttime"),
        fields.DateTimeField("开始日期时间", "startdatetime"),
        fields.SelectField("编辑人", "editor", source=[(0, "普通人"), (1, "人人")]),
        fields.MulSelectField("编辑人", "editors", source=[(0, "普通人"), (1, "人人"), (2, "普通人11"), (3, "人人11")])
    ]
    # 搜索条件展示
    # 可选值参见源码 king_admin>fields.py
    
    options = {}
    # bootstrap-table操作列
    """
    options key示意：
    1.js
        类型：js代码文件路径 通过static导入
        描述：用于展示表格列显示的内容
        注意：js文件
            1. function operateFormatter(value, row, index) {
                    return '<button type="submit" class="btn btn-warning btn-sm" id="btn_change">修改</button>'
                }
            2. let operateEvents = {
                  'click #btn_change': function (e, value, row, index) {
                    ...
                  }
                };
    2.extra
        类型：html代码文件路径 通过include导入
        描述：用于触发事件时，所需的html，比如模态对话框

    options示例：
    options = {
        "js": "js/option.js",
        "extra": "demo.html"
    }
    """
    
    add_btn = StaffForm
    # 是否显示添加按钮 默认False 如赋值应是FlaskForm的派生类
    add_url = data_url + "/add"
    # 显示添加按钮时ajax请求api


admin.add_url_rule("/", view_func=Index.as_view(name="index"))


@admin.route("/index/data")
def index_data():
    args = request.args.to_dict()

    data_rows = [
        {
            "id": 0,
            "name": "Item 0",
            "price": "$0"
        },
        {
            "id": 1,
            "name": "Item 1",
            "price": "$1"
        }
    ]

    args.update({"editors": request.args.getlist("editors")})

    args["id"] = int(args["id"]) if args.get("id") else 0

    rows1 = list(filter(lambda item: True if item["id"] >= args["id"] else False, data_rows))

    rows = rows1[int(args.get("offset", 0)): int(args.get("offset", 0)) + int(args.get("limit", 10))]

    data = {
        "total": len(rows1),
        "totalNotFiltered": 800,
        "rows": rows
    }

    return jsonify(data)


@admin.route("/index/data/add")
def index_add():
    args = request.args.to_dict()
    mod = sys.modules[__name__]

    form_class = args.pop("form_class", "")

    form = getattr(mod, form_class)(**args, csrf_enabled=False)
    if form.validate():
        # 数据库添加数据操作
        return json_response(200, "添加数据成功")

    return json_response(404, "添加数据失败", form.errors)

```

## 3. 在flask实例中导入admin蓝图并注册

```python
from flask import Flask
from flask_babel import Babel # 用于提示信息的本地化

# 注意需要从admin.py导入admin，而不能从king_admin中导入
from admin import admin 

app = Flask(__name__)

babel = Babel(app)
app.config["DEBUG"] = True
app.config["BABEL_DEFAULT_LOCALE"] = "zh"

app.register_blueprint(admin)

if __name__ == '__main__':
    app.run()
```

