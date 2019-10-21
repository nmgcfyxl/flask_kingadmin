#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from flask import render_template
from flask.views import MethodView

from wtforms.form import FormMeta

from king_admin.fields import Field


class Base(MethodView):

    def get_search_fields(self):
        search_fields = []
        for item in self.search_fields:
            if not isinstance(item, Field):
                raise ValueError(f"{self.__class__.__name__}中search_fields属性元素必须是Field的派生实例")
            search_fields.append(item)
        return search_fields

    def get_add_btn(self):
        if isinstance(self.add_btn, FormMeta):
            if type(self.add_url) == str and self.add_url:
                return self.add_btn(csrf_enabled=False)
            raise TypeError(f"{self.__class__.__name__}中add_btn属性存在时，add_url不得为空，必须要添加数据接口")

        if self.add_btn is False:
            return self.add_btn
        raise ValueError(f"{self.__class__.__name__}中add_btn属性只能是False或者FlaskForm的实例")

    def get_data_url(self):
        if not self.data_url:
            raise ValueError(f"类{self.__class__.__name__}的data_url不得为空")
        return self.data_url

    def get_options(self):
        if self.options:
            if isinstance(self.options, dict):
                if all(["js" in self.options, "extra" in self.options]):
                    return self.options
                else:
                    raise ValueError(f"类{self.__class__.__name__}中options字典必须包含js,extra两个键")

            raise TypeError(f"{self.__class__.__name__}中options属性必须是dict类型")

        return self.options


class BaseView(Base):
    title = ""  # 页面标题
    list_display = []  # 表格展示的字段 元素必须是元组，第1位：表格标题，第二位：数据字段
    checkbox = False  # 是否有checkbox
    search_fields = []  # 搜索的字段
    data_url = ""  # 表格数据请求地址
    options = {}  # 每行可操作按钮
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
    add_btn = False  # 显示添加按钮
    add_url = False  # 增加数据ajax接口

    def get(self):
        render = {
            "title": self.title,
            "data_url": self.get_data_url(),
            "list_display": self.list_display,
            "checkbox": self.checkbox,
            "options": self.get_options(),
            "search_fields": self.get_search_fields(),
            "add_btn": self.get_add_btn(),
            "add_url": self.add_url,
        }

        return render_template("chang_list.html", **render)
