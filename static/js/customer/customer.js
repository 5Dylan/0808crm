// ------------------------------客户信息管理----------------start--------------------
// 格式化开发状态
function formatter_state(value) {
    if ('0' == value)
        return '正常';

    if ('1' == value)
        return '暂时流失';

    if ('2' == value)
        return '确认流失';

    return value;
}

// 格式化时间
function formatter_datetime(value) {
    if (undefined == value || null == value)
        return '';

    return value.replace('T', ' ');
}

// 按条件查询
function select_params_customer() {
    // 获取参数
    var name = $('#customer_name').val().trim();
    var khno = $('#customer_khno').val().trim();
    var state = $('#customer_state').combobox('getValue');

    $('#dg').datagrid('reload', {
        name: name,
        khno: khno,
        state: state
    });
}

// 切换分配状态立即查询
$("#state").combobox({
    onChange: function () {
        select_params_customer();
    }
});

// 初始化创建客户信息对话框
$('#customer_dialog').dialog({
    title: '添加客户信息',
    width: 660,
    height: 430,
    iconCls: 'icon-add',
    resizable: false,
    modal: true, // 模态
    draggable: false, // 不可移动
    closed: true, // 是否关闭
    buttons: [{
        text: '保存',
        iconCls: 'icon-save',
        handler: function () {
            // 提交form表单，1是添加，2修改
            if (1 == $('#flag').val()) {
                sub_create_customer_form();
            } else if (2 == $('#flag').val()) {
                sub_update_customer_form();
            }
        }
    }, {
        text: '关闭',
        iconCls: 'icon-cancel',
        handler: function () {
            $('#customer_dialog').dialog('close');
            // 清空对话框
            $('#sales_sale_chance_form input').val('');
            $('#sales_sale_chance_form textarea').val('');
            $('#sales_sale_chance_form select').empty();
        }
    }]
});

// 打开添加客户信息对话框
function open_customer_create_dialog() {
    // 打开对话框后给标识符隐藏域赋值
    $('#flag').val(1);

    $('#customer_dialog').dialog('open');
}

// 提交新增form表单
function sub_create_customer_form() {
    $('#customer_form').form('submit', {
        url: '/customer/create_customer/',
        success: function (result) {
            var obj = JSON.parse(result);

            if (200 == obj.code) {
                $.messager.show({
                    title: '提示',
                    msg: obj.msg,
                    timeout: 5000
                });

                // 关闭对话框
                $('#customer_dialog').dialog('close');
                // 清空对话框
                $('#customer_form input').val('');
                $('#customer_form select').combobox('setValue', '请选择');
                // 重新加载数据
                select_params_customer();
            }
        }
    });
}

// 打开修改客户信息对话框
function open_customer_update_dialog() {
    // 打开对话框后给标识符隐藏域赋值
    $('#flag').val(2);

    // 判断必须选择且只可以选择一条才能弹出对话框
    var ids = $('#dg').datagrid('getChecked');

    if (0 == ids.length) {
        $.messager.alert('系统提示', '必须选择一条信息', 'warning');
        return;
    }

    if (ids.length > 1) {
        $.messager.alert('系统提示', '只可以选择一条信息', 'warning');
        return;
    }

    // 根据主键查询客户信息
    var id = ids[0].id;
    $.get('/customer/select_customer_by_id/?id=' + id, function (result) {
        // 数据返显
        if (200 == result.code) {
            var obj = result.obj;
            $('#id').val(id);
            $('#khno').val(obj.khno);
            $('#name').val(obj.name);
            $('#area').combobox('select', obj.area);
            $('#cusManager').val(obj.cusManager);
            $('#level').combobox('select', obj.level);
            $('#myd').combobox('select', obj.myd);
            $('#xyd').combobox('select', obj.xyd);
            $('#postCode').val(obj.postCode);
            $('#phone').val(obj.phone);
            $('#fax').val(obj.fax);
            $('#website').val(obj.website);
            $('#address').val(obj.address);
            $('#yyzzzch').val(obj.yyzzzch);
            $('#fr').val(obj.fr);
            $('#zczj').val(obj.zczj);
            $('#nyye').val(obj.nyye);
            $('#khyh').val(obj.khyh);
            $('#khzh').val(obj.khzh);
            $('#dsdjh').val(obj.dsdjh);
            $('#gsdjh').val(obj.gsdjh);

            $('#customer_dialog').dialog('open');
        }
    });
}

// 提交修改form
function sub_update_customer_form() {
    $('#csrfmiddlewaretoken').val($.cookie('csrftoken'));

    $('#customer_form').form('submit', {
        url: '/customer/update_customer/',
        success: function (result) {
            var obj = JSON.parse(result);

            if (200 == obj.code) {
                $.messager.show({
                    title: '提示',
                    msg: obj.msg,
                    timeout: 5000
                });

                // 关闭对话框
                $('#customer_dialog').dialog('close');
                // 清空对话框
                $('#customer_form input').val('');
                $('#customer_form select').combobox('setValue', '请选择');
                // 重新加载数据
                select_params_customer();
            }
        }
    });
}

// 删除客户信息
function delete_customer() {
    // 判断必须选择且可以多选择
    var ids = $('#dg').datagrid('getChecked');

    if (0 == ids.length) {
        $.messager.alert('系统提示', '必须选择一条信息', 'warning');
        return;
    }

    $.messager.confirm('系统提示', '您确认想要删除这 ' + ids.length + ' 条记录吗？', function (r) {
        if (r) {
            // 拼接主键
            var customer_ids = '';
            for (var i = 0; i < ids.length; i++) {
                if (i != ids.length - 1) {
                    customer_ids += ids[i].id + ',';
                } else {
                    customer_ids += ids[i].id;
                }
            }

            // 发送ajax删除数据
            $.ajax({
                'type': 'GET',
                'url': '/customer/delete_customer/',
                'data': {
                    'ids': customer_ids
                },
                'dataType': 'json',
                'success': function (result) {
                    // 显示提示信息
                    $.messager.show({
                        title: '提示',
                        msg: result.msg,
                        timeout: 5000
                    });

                    select_params_customer();
                },
                'error': function (result) {
                    console.log(result);
                }
            });
        }
    });
}

// ------------------------------客户信息管理-----------------end---------------------

// ------------------------------客户联系人管理----------------start--------------------
// 打开客户联系人窗口
function open_linkman_window() {
    // 判断必须选择且只可以选择一条才能弹出对话框
    var ids = $('#dg').datagrid('getChecked');

    if (0 == ids.length) {
        $.messager.alert('系统提示', '必须选择一条信息', 'warning');
        return;
    }

    if (ids.length > 1) {
        $.messager.alert('系统提示', '只可以选择一条信息', 'warning');
        return;
    }

    // 打开一个新窗口
    window.parent.openTab('客户联系人', '/customer/linkman_index/?id=' + ids[0].id, 'icon-lxr');
}

// ------------------------------客户联系人管理-----------------end---------------------

// ------------------------------客户交往记录管理----------------start--------------------
// 打开客户联系人窗口
function open_contact_window() {
    // 判断必须选择且只可以选择一条才能弹出对话框
    var ids = $('#dg').datagrid('getChecked');

    if (0 == ids.length) {
        $.messager.alert('系统提示', '必须选择一条信息', 'warning');
        return;
    }

    if (ids.length > 1) {
        $.messager.alert('系统提示', '只可以选择一条信息', 'warning');
        return;
    }

    // 打开一个新窗口
    window.parent.openTab('客户交往记录', '/customer/contact_index/?id=' + ids[0].id, 'icon-jwjl');
}

// ------------------------------客户交往记录管理-----------------end---------------------

// ------------------------------客户历史订单管理----------------start--------------------
// 打开客户联系人窗口
function open_order_window() {
    // 判断必须选择且只可以选择一条才能弹出对话框
    var ids = $('#dg').datagrid('getChecked');

    if (0 == ids.length) {
        $.messager.alert('系统提示', '必须选择一条信息', 'warning');
        return;
    }

    if (ids.length > 1) {
        $.messager.alert('系统提示', '只可以选择一条信息', 'warning');
        return;
    }

    // 打开一个新窗口
    window.parent.openTab('客户历史订单', '/customer/order_index/?id=' + ids[0].id, 'icon-lsdd');
}

// ------------------------------客户历史订单管理-----------------end---------------------