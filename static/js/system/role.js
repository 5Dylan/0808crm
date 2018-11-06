// 打开添加角色对话框
function open_role_create_dialgo() {
    $('#dialog').dialog('open').dialog('setTitle', '添加角色');
    reset_form();
}

// 打开修改模块对话框
function open_role_update_dialgo() {
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

    row = row[0];
    $('#fm').form('load', row);
    $('#dialog').dialog('open').dialog('setTitle', '修改角色');
}

// 关闭模块对话框
function close_role_dialgo() {
    $('#dialog').dialog('close');
    reset_form();
}

// 重置对话框
function reset_form() {
    $('#fm').form('clear');
}

// 保存模块信息
function save_role() {
    var id = $('#id').val().trim();
    // 判断非空
    var url = null;
    if (undefined != id && null != id && id.length > 0) {
        url = '/system/update_role/'
    } else {
        url = '/system/create_role/'
    }

    $('#fm').form('submit', {
        url: url,
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
function delete_role() {
    // 判断必须选择且可以多选择
    var ids = $('#dg').datagrid('getChecked');

    if (0 == ids.length) {
        $.messager.alert('系统提示', '必须选择一条信息', 'warning');
        return;
    }

    $.messager.confirm('系统提示', '您确认想要删除这 <span style="color: red">' + ids.length + '</span> 条记录吗？', function (r) {
        if (r) {
            // 拼接主键
            var role_ids = '';
            for (var i = 0; i < ids.length; i++) {
                if (i != ids.length - 1) {
                    role_ids += ids[i].id + ',';
                } else {
                    role_ids += ids[i].id;
                }
            }

            // 发送ajax删除数据
            $.ajax({
                'type': 'GET',
                'url': '/system/delete_role/',
                'data': {
                    'ids': role_ids
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

// 角色关联资源
function role_relate_module() {
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

    var id = row[0].id;

    window.parent.openTab('关联权限', '/system/role_module_index/?id=' + id, 'icon-user')
}