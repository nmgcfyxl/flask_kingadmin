function operateFormatter(value, row, index) {
  return [
    '<button type="submit" class="btn btn-warning btn-sm" style="margin-right: 10px" id="btn_change">修改</button>',
    '<button class="remove btn btn-sm btn-danger" href="javascript:void(0)" title="Remove">删除</button>'
  ].join('')
}

let operateEvents = {
  'click #btn_change': function (e, value, row, index) {
    // 发送ajax请求 获取修改行数据 或者使用 row 参数来进行修改
    console.log(row);
    $("#change_btn").modal('show');
  },
  'click .remove': function (e, value, row, index) {
    $table.bootstrapTable('remove', {
      field: 'id',
      values: [row.id]
    })
  }
};