// 打开添加用户对话框
function open_user_create_dialgo() {
    // 添加密码必填样式
    $('#password').validatebox({
        required: true
    });
    // 显示密码span样式
    $('#pwd_span').css('display', 'false');

    $('#dialog').dialog('open').dialog('setTitle', '添加用户');
    reset_form();
}

// 打开修改用户对话框
// 要查询角色返显
function open_user_update_dialgo() {
    // 判断必须选择且只可以选择一条才能弹出对话框
    var row = $('#dg').datagrid('getChecked');

    if (0 == row.length) {
        $.messager.alert('系统提示', '必须选择一条信息', 'warning');
        return;
    }

    if (row.length > 1) {
        $.messager.alert('系统提示', '只可以选择一条信息', 'warning');
        return;
    }

    // 取消密码必填样式
    $('#password').validatebox({
        required: false
    });
    // 隐藏密码span样式
    $('#pwd_span').css('display', 'none');

    row = row[0];
    // 根据用户id查询角色
    $.get('/system/select_role_by_userid/?id=' + row.id, function (result) {
        // 将后台返回的列表直接赋值给表单的roles域名
        row.roles = result;
        $('#fm').form('load', row);
        $('#dialog').dialog('open').dialog('setTitle', '修改用户');
    });
}

// 关闭模块对话框
function close_user_dialgo() {
    $('#dialog').dialog('close');
    reset_form();
}

// 重置对话框
function reset_form() {
    $('#fm').form('clear');
}

// 保存模块信息
function save_user() {
    var id = $('#id').val().trim();
    // 判断非空
    var url = null;
    if (undefined != id && null != id && id.length > 0) {
        url = '/system/update_user/'
    } else {
        url = '/system/create_user/'
    }

    $('#fm').form('submit', {
        url: url,
        // 添加额外参数校验
        onSubmit: function () {
            if (undefined == $('#roles').combobox('getValue') || '' == $('#roles').combobox('getValue')) {
                $.messager.show({
                    title: '系统提示',
                    msg: '请选择角色',
                    timeout: 5000
                });
                return false;
            }

            // 获取roles的所有角色值
            /*var role_arr = $('#roles').combobox('getValues');
            // 循环拼接赋值给隐藏域发往后台
            var role_hidden = '';
            for (var i = 0; i < role_arr.length; i++) {
                if (i != role_arr.length - 1)
                    role_hidden += role_arr[i] + ',';
                else
                    role_hidden += role_arr[i];
            }
            $('#roles_hidden').val(role_hidden);*/

            // 验证所有form的必填项
            return $('#fm').form('validate');
        },
        success: function (result) {
            var obj = JSON.parse(result);

            $.messager.show({
                title: '系统提示',
                msg: obj.msg,
                timeout: 5000
            });

            if (200 == obj.code) {
                $('#dialog').dialog('close');
                reset_form();
                $('#dg').datagrid('reload');
            }
        }
    });
}

// 删除模型
function delete_user() {
    // 判断必须选择且可以多选择
    var ids = $('#dg').datagrid('getChecked');

    if (0 == ids.length) {
        $.messager.alert('系统提示', '必须选择一条信息', 'warning');
        return;
    }

    $.messager.confirm('系统提示', '您确认想要删除这 <span style="color: red">' + ids.length + '</span> 条记录吗？', function (r) {
        if (r) {
            // 拼接主键
            var user_ids = '';
            for (var i = 0; i < ids.length; i++) {
                if (i != ids.length - 1) {
                    user_ids += ids[i].id + ',';
                } else {
                    user_ids += ids[i].id;
                }
            }

            // 发送ajax删除数据
            $.ajax({
                'type': 'GET',
                'url': '/system/delete_user/',
                'data': {
                    'ids': user_ids
                },
                'dataType': 'json',
                'success': function (result) {
                    // 显示提示信息
                    $.messager.show({
                        title: '提示',
                        msg: result.msg,
                        timeout: 5000
                    });

                    if (200 == result.code) {
                        $('#dg').datagrid('reload');
                    }
                },
                'error': function (result) {
                    console.log(result);
                }
            });
        }
    });
}