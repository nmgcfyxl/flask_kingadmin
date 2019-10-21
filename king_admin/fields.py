#!/usr/local/bin/python
# -*- coding: utf-8 -*- 
from datetime import datetime

from flask import Markup


class Field(object):
    def __init__(self, label, field, help_text=None, source=None, style=None):
        """
        :param label: 表单label内容
        :param field:  表单id的名字
        :param help_text:  表单placeholder内容
        :param source:  下拉框的选项  示例 [(0, "普通人"), (1, "人人")]
        :param style: 表单额外的 样式类
        """
        self.source = source
        self.label = label
        self.style = "" if not style else style
        self.field = field
        self.help_text = '请输入' + label if not help_text else help_text

    def to_representation(self, value):
        """自定义方法接口
        """
        raise NotImplementedError(
            '{cls}.to_representation() must be implemented.'.format(cls=self.__class__.__name__, )
        )

    def __str__(self):
        return self.field


class TextField(Field):
    """
    搜索选项中 文本输入框
    """

    def to_representation(self, value=None):
        return Markup('''
            <div class="form-group {style}" style="margin:10px 50px;width:350px;">
                <label for="id_{field}" style="width:100px;text-align:right;">{label}</label>
                <input type="text" class="form-control" id="id_{field}" placeholder="{help_text}">
            </div>
        ''').format(style=self.style, field=self.field, label=self.label, help_text=self.help_text)


class DateField(Field):
    """
    搜索选项中 日期输入框
    """

    def to_representation(self, value=None):
        return Markup('''
                    <div class="form-group {style}" style="margin:10px 50px;width:350px;">
                        <label for="id_{field}" style="width:100px;text-align:right;">{label}</label>
                        <input type="text" class="form-control" id="id_{field}" placeholder="{help_text}" autocomplete="off">
                    </div>
                    <script>
                        $("#id_{field}").datetime({{
                            type:"date",
                            value:[{year},{month},{day}]
                        }})
                    </script>
                ''').format(style=self.style, field=self.field, label=self.label, help_text=self.help_text,
                            year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)


class TimeField(Field):
    """
    搜索选项中 时间输入框
    """

    def to_representation(self, value=None):
        return Markup('''
                    <div class="form-group {style}" style="margin:10px 50px;width:350px;">
                        <label for="id_{field}" style="width:100px;text-align:right;">{label}</label>
                        <input type="text" class="form-control" id="id_{field}" placeholder="{help_text}" autocomplete="off">
                    </div>
                    <script>
                        $("#id_{field}").datetime({{
                            type:"time",
                            value:[{hour},{minute}]
                        }})
                    </script>
                ''').format(style=self.style, field=self.field, label=self.label, help_text=self.help_text,
                            hour=datetime.now().hour, minute=datetime.now().minute)


class DateTimeField(Field):
    """
    搜索选项中 日期时间输入框
    """

    def to_representation(self, value=None):
        return Markup('''
                    <div class="form-group {style}" style="margin:10px 50px;width:350px;">
                        <label for="id_{field}" style="width:100px;text-align:right;">{label}</label>
                        <input type="text" class="form-control" id="id_{field}" placeholder="{help_text}" autocomplete="off">
                    </div>
                    <script>
                        $("#id_{field}").datetime({{
                            type:"datetime",
                            value:[{year},{month},{day},{hour},{minute}]
                        }})
                    </script>
                ''').format(style=self.style, field=self.field, label=self.label, help_text=self.help_text,
                            year=datetime.now().year, month=datetime.now().month, day=datetime.now().day,
                            hour=datetime.now().hour, minute=datetime.now().minute)


class SelectField(Field):
    """
    搜索选项中 下拉框
    """

    def to_representation(self, value=None):
        select_list = []
        for item in self.source:
            option = f'<option value="{item[0]}">{item[1]}</option>'
            select_list.append(option)

        return Markup('''
                    <div class="form-group {style}" style="margin:10px 50px;width:350px;">
                        <label for="id_{field}" style="width:100px;text-align:right;">{label}</label>
                        <select class="form-control" id="id_{field}">
                            <option value="">{help_text}</option>
                            {option}
                        </select>
                    </div>
               ''').format(style=self.style, field=self.field, label=self.label, help_text=self.help_text,
                           option=Markup("".join(select_list)))


class MulSelectField(Field):
    """
    搜索选项中 下拉多选框
    """

    def to_representation(self, value=None):
        select_list = []
        for item in self.source:
            option = f'<option value="{item[0]}">{item[1]}</option>'
            select_list.append(option)

        return Markup('''
                       <div class="form-group {style}" style="margin:10px 50px;width:350px;">
                           <label for="id_{field}" style="width:100px;text-align:right;">{label}</label>
                           <select id="id_{field}" multiple>
                               {option}
                           </select>
                       </div>
                       <script>
                         $('#id_{field}').multiselect({{
                            includeSelectAllOption: true,
                            selectAllText: '全选',
                            nonSelectedText: '{help_text}',
                            allSelectedText: '已全选',
                            buttonWidth: '180px',
                            buttonContainer: '<div id="id_{field}_container"></div>',
                            enableFiltering: true,
                            onChange: function($option) {{
                                // Check if the filter was used.
                                var query = $('#id_{field}_container li.multiselect-filter input').val();
                        
                                if (query) {{
                                    $('#id_{field}_container li.multiselect-filter input').val('').trigger('keydown');
                                }}
                            }}
                         }});
                       </script>
                  ''').format(style=self.style, field=self.field, label=self.label, help_text=self.help_text,
                              option=Markup("".join(select_list)))
