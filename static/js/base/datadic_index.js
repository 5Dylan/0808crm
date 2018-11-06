// 初始化对话框
$('#dialog').dialog({
    title: '添加数据字典',
    width: 650,
    iconCls: 'icon-add',
    resizable: false,
    modal: true, // 模态
    draggable: false, // 不可移动
    closed: true, // 是否关闭
    buttons: [{
        text: '保存',
        iconCls: 'icon-save',
        handler: function () {
            // 提交form表单
            sub_datadic_form();
        }
    }, {
        text: '关闭',
        iconCls: 'icon-cancel',
        handler: function () {
            $('#dialog').dialog('close');
            // 清空对话框
            $('#fm input').val('');
            $('#dataDicName').combobox('setValue', '');
        }
    }]
});

// 打开对话框
function open_datadic_dialog(flag) {
    // 赋值1或者2
    $('#flag').val(flag);

    // 如果是2 还要拦截操作进行判断
    // 判断必须选择且只可以选择一条才能弹出对话框
    if (2 == flag) {
        var ids = $('#dg').datagrid('getChecked');

        if (0 == ids.length) {
            $.messager.alert('系统提示', '必须选择一条信息', 'warning');
            return;
        }

        if (ids.length > 1) {
            $.messager.alert('系统提示', '只可以选择一条信息', 'warning');
            return;
        }

        $('#fm').form('load', ids[0]);
    }

    $('#dialog').dialog('open');
}

// 提交form
function sub_datadic_form() {
    // 获取1或者2
    var flag = $('#flag').val();

    // 1添加 2修改
    var url = null;
    if (1 == flag) {
        url = '/base/create_datadic/';
    } else if (2 == flag) {
        url = '/base/update_datadic/';
    }

    $('#csrfmiddlewaretoken').val($.cookie('csrftoken'));

    // 执行
    $('#fm').form('submit', {
        url: url,
        'success': function (result) {
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
                $('#dataDicName').combobox('setValue', '');

                // 重新加载数据
                $('#dg').datagrid('reload');
            }
        }
    });
}

// 删除数据字典
function delete_datadic() {
    var ids = $('#dg').datagrid('getChecked');

    if (0 == ids.length) {
        $.messager.alert('系统提示', '必须选择一条信息', 'warning');
        return;
    }

    $.messager.confirm('系统提示', '您确认想要删除这 ' + ids.length + ' 条记录吗？', function (r) {
        if (r) {
            // 拼接主键
            var datadic_ids = '';
            for (var i = 0; i < ids.length; i++) {
                if (i != ids.length - 1) {
                    datadic_ids += ids[i].id + ',';
                } else {
                    datadic_ids += ids[i].id;
                }
            }

            // 发送ajax请求
            $.get('/base/delete_datadic/?id=' + datadic_ids, function (result) {
                if (200 == result.code) {
                    $.messager.show({
                        title: '系统提示',
                        msg: result.msg,
                        timeout: 5000
                    });

                    // 重新加载数据
                    $('#dg').datagrid('reload');
                }
            });
        }
    });
}