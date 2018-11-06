// 初始化服务对话框
$('#dialog').dialog({
    title: '服务处理',
    width: 700,
    height: 450,
    resizable: false,
    modal: true, // 模态
    draggable: false, // 不可移动
    closed: true, // 是否关闭
    buttons: [{
        text: '保存',
        iconCls: 'icon-save',
        handler: function () {
            // 提交form表单
            update_serve();
        }
    }, {
        text: '关闭',
        iconCls: 'icon-cancel',
        handler: function () {
            $('#dialog').dialog('close');
            // 清空对话框
            $('#fm input').val('');
            $('#fm textarea').val('');
        }
    }]
});

// 格式化时间
function formatter_datetime(value) {
    if (undefined == value || null == value)
        return '';

    return value.replace('T', ' ');
}

// 修改服务
function update_serve() {
    $('#csrfmiddlewaretoken').val($.cookie('csrftoken'));

    $('#fm').form('submit', {
        url: '/serve/update_serve/',
        success: function (result) {
            var obj = JSON.parse(result);

            $.messager.show({
                title: '系统提示',
                msg: obj.msg,
                timeout: 5000
            });

            if (200 == obj.code) {
                $('#dialog').dialog('close');
                // 清空对话框
                $('#fm input').val('');
                $('#fm textarea').val('');
            }
        }
    });

    setTimeout(function () {
        // 重新加载
        $('#dg').datagrid('reload');
    }, 500);
}