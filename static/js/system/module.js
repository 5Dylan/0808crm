// 格式化层级
function formatter_grade(value) {
    if (0 == value)
        return '根级'

    if (1 == value)
        return '一级'

    if (2 == value)
        return '二级'
}

// 根据层级选择展示不同的父级菜单
$('#grade').combobox({
    onSelect: function () {
        var grade = $('#grade').combobox('getValue')
        if (0 == grade) {
            $('#parent_tr').hide();
        } else {
            $('#parent_tr').show();
            select_module_by_grade(grade);
        }
    }
});


// 打开添加模块对话框
function open_module_create_dialgo() {
    $('#parent_tr').hide();
    $('#dialog').dialog('open').dialog('setTitle', '添加模块');
    reset_form();
}

// 打开修改模块对话框
function open_module_update_dialgo() {
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
    // 如果不是根级菜单，显示父级菜单
    if (0 != row.grade) {
        $('#parent_tr').show();
        select_module_by_grade(row.grade, row.parent);
    } else {
        $('#parent_tr').hide();
    }

    $('#fm').form('load', row);
    $('#dialog').dialog('open').dialog('setTitle', '修改模块');
}

// 根据等级查询父级菜单
function select_module_by_grade(grade, parent) {
    $('#parent').combobox({
        url: '/system/select_module_by_grade/?grade=' + (grade - 1),
        valueField: 'id',
        textField: 'moduleName',
        method: 'get',
        editable: false,
        value: parent
    });
}

// 关闭模块对话框
function close_module_dialgo() {
    $('#dialog').dialog('close');
    reset_form();
}

// 重置对话框
function reset_form() {
    $('#fm').form('clear');
}

// 保存模块信息
function save_module() {
    var id = $('#id').val().trim();
    // 判断非空
    var url = null;
    if (undefined != id && null != id && id.length > 0) {
        url = '/system/update_module/'
    }else {
        url = '/system/create_module/'
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
function delete_module() {
    // 判断必须选择且可以多选择
    var ids = $('#dg').datagrid('getChecked');

    if (0 == ids.length) {
        $.messager.alert('系统提示', '必须选择一条信息', 'warning');
        return;
    }

    $.messager.confirm('系统提示', '您确认想要删除这 <span style="color: red">' + ids.length + '</span> 条记录吗？', function (r) {
        if (r) {
            // 拼接主键
            var module_ids = '';
            for (var i = 0; i < ids.length; i++) {
                if (i != ids.length - 1) {
                    module_ids += ids[i].id + ',';
                } else {
                    module_ids += ids[i].id;
                }
            }

            // 发送ajax删除数据
            $.ajax({
                'type': 'GET',
                'url': '/system/delete_module/',
                'data': {
                    'ids': module_ids
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
