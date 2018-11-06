// 格式化分配时间
function formatter_datetime(value) {
    if (undefined == value || null == value)
        return '';

    return value.replace('T', ' ');
}

// 格式化状态
function formatter_state(value) {
    if ('0' == value)
        return '未分配';

    if ('1' == value)
        return '已分配';

    return value;
}

// 格式化开发状态
function formatter_devResult(value) {
    if ('0' == value)
        return '未开发';

    if ('1' == value)
        return '开发中';

    if ('2' == value)
        return '开完完成';

    if ('3' == value)
        return '开发失败';

    return value;
}

// 按条件查询营销机会
function select_params_sela_chance() {
    // 获取参数
    var customerName = $('#customerName').val().trim();
    var overview = $('#overview').val().trim();
    var createMan = $('#createMan').val().trim();
    var state = $('#state').combobox('getValue');

    $('#dg').datagrid('reload', {
        customerName: customerName,
        overview: overview,
        createMan: createMan,
        state: state
    });
}

// 切换分配状态立即查询
$("#state").combobox({
    onChange: function () {
        select_params_sela_chance();
    }
});

// ----------------------------------创建营销机会-----------------start---------------
// 初始化创建营销机会对话框
$('#sales_sale_chance_create_dialog').dialog({
    title: '添加营销机会',
    width: 700,
    height: 450,
    iconCls: 'icon-add',
    resizable: false,
    modal: true, // 模态
    draggable: false, // 不可移动
    closed: true, // 是否关闭
    buttons: [{
        text: '保存',
        iconCls: 'icon-save',
        handler: function () {
            // 先给csrf隐藏域赋值
            $('#csrfmiddlewaretoken').val($.cookie('csrftoken'));

            // 提交form表单
            sub_create_sale_chance_form();
        }
    }, {
        text: '关闭',
        iconCls: 'icon-cancel',
        handler: function () {
            $('#sales_sale_chance_create_dialog').dialog('close');
            // 清空对话框
            $('#sales_sale_chance_form input').val('');
            $('#sales_sale_chance_form textarea').val('');
            $('#sales_sale_chance_form select').empty();
        }
    }]
});

// 打开营销机会对话框
function open_sale_chance_dialog() {
    // 发送ajax请求查询客户名称和联系人名称
    $.ajax({
        'type': 'GET',
        'url': '/customer/select_cname_and_lname_and_uname/',
        'data': {
            'csrfmiddlewaretoken': $.cookie('csrftoken')
        },
        'dataType': 'json',
        'success': function (result) {
            // 如果是400 显示错误信息
            if (400 == result.code) {
                $.messager.show({
                    title: '系统提示',
                    msg: result.msg,
                    timeout: 5000
                });
            }

            // 如果是200 正常显示
            if (200 == result.code) {
                // 如果数据存在则循环展示
                if (result.cs.length > 0) {
                    var cs = result.cs;
                    $('#customer_select').append('<option value="0">-----请选择-----</option>');
                    for (var i = 0; i < cs.length; i++) {
                        $('#customer_select').append('<option value="' + cs[i].id + '">' + cs[i].name + '</option>');
                    }
                }

                // 如果数据存在则循环展示
                if (result.ls.length > 0) {
                    var ls = result.ls;
                    $('#linkman_select').append('<option value="0">-----请选择-----</option>');
                    for (var i = 0; i < ls.length; i++) {
                        $('#linkman_select').append('<option value="' + ls[i].id + '">' + ls[i].linkName + '</option>');
                    }
                }

                // 如果数据存在则循环展示
                if (result.us.length > 0) {
                    var us = result.us;
                    $('#username_select').append('<option value="0">-----请选择-----</option>');
                    for (var i = 0; i < us.length; i++) {
                        $('#username_select').append('<option value="' + us[i].id + '">' + us[i].username + '</option>');
                    }
                }

                $('#sales_sale_chance_create_dialog').dialog('open');
            }
        },
        'error': function (result) {
            console.log(result);
        }
    });
}

// 获取客户名称赋值给隐藏域
function get_customerName() {
    $('#customerName_hidden').val($('#customer_select').find("option:selected").text());
}

// 获取联系人名称赋值给隐藏域
function get_linkName() {
    // 判断如果不是请选择就查询电话号码
    if ('0' == $('#linkman_select').val()) {
        $('#linkPhone').val('');
        return;
    }

    // 联系人名称赋值给隐藏域
    $('#linkManName_hidden').val($('#linkman_select').find("option:selected").text());

    // 根据联系人id去查询电话返显至电话输入框
    $.ajax({
        'type': 'GET',
        'url': '/customer/select_link_phone_by_id/',
        'data': {
            'id': $('#linkman_select').val()
        },
        'dataType': 'json',
        'success': function (result) {
            // 如果是200 赋值
            if (200 == result.code) {
                $('#linkPhone').val(result.phone);
            }
        },
        'error': function (result) {
            console.log(result);
        }
    });
}

// 提交form表单
function sub_create_sale_chance_form() {
    $('#sales_sale_chance_form').form('submit', {
        url: '/sales/create_sale_chance/',
        success: function (result) {
            var obj = JSON.parse(result);

            // 显示提示信息
            $.messager.show({
                title: '提示',
                msg: obj.msg,
                timeout: 5000
            });

            // 如果code是200 清除对话框
            if (200 == obj.code) {
                // 关闭对话框
                $('#sales_sale_chance_create_dialog').dialog('close');

                $('#sales_sale_chance_form input').val('');
                $('#sales_sale_chance_form textarea').val('');
                $('#sales_sale_chance_form select').empty();

                select_params_sela_chance();
            }
        }
    });
}

// ----------------------------------创建营销机会------------------end----------------

// ----------------------------------修改营销机会-----------------start---------------
// 初始化修改营销机会对话框
$('#sales_sale_chance_update_dialog').dialog({
    title: '修改营销机会',
    width: 700,
    height: 450,
    iconCls: 'icon-edit',
    resizable: false,
    modal: true, // 模态
    draggable: false, // 不可移动
    closed: true, // 是否关闭
    buttons: [{
        text: '保存',
        iconCls: 'icon-save',
        handler: function () {
            // 提交form表单
            sub_update_sale_chance_form();
        }
    }, {
        text: '关闭',
        iconCls: 'icon-cancel',
        handler: function () {
            $('#sales_sale_chance_update_dialog').dialog('close');
            // 清空对话框
            $('#sales_sale_chance_form input').val('');
            $('#sales_sale_chance_form textarea').val('');
            $('#sales_sale_chance_form select').empty();
        }
    }]
});

// 打开修改营销机会对话框
function open_sale_chance_update_dialog() {
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

    var customer_id = null;
    var linkman_id = null;
    var user_id = null;

    // 根据主键查询营销机会
    var id = ids[0].id
    $.ajax({
        'type': 'GET',
        'url': '/sales/select_sale_chance_by_id/?id=' + id,
        'async': false,
        'dataType': 'json',
        'success': function (result) {
            if (200 == result.code) {
                // 返显数据
                $('#id').val(result.sc.id);
                $('#update_customerName_hidden').val(result.sc.customerName);
                $('#update_chanceSource').val(result.sc.chanceSource);
                $('#update_linkManName_hidden').val(result.sc.linkManName);
                $('#update_linkPhone').val(result.sc.linkPhone);
                $('#update_cgjl').val(result.sc.cgjl);
                $('#update_overview').val(result.sc.overview);
                $('#update_description').val(result.sc.description);

                customer_id = result.sc.customerId
                linkman_id = result.sc.linkManId
                user_id = result.sc.userId
            }
        }
    });

    // 发送ajax请求查询客户名称和联系人名称和分配人
    $.ajax({
        'type': 'GET',
        'url': '/customer/select_cname_and_lname_and_uname/',
        'dataType': 'json',
        'success': function (result) {
            // 如果是400 显示错误信息
            if (400 == result.code) {
                console.log(result.msg);
            }

            // 如果是200 正常显示
            if (200 == result.code) {
                // 如果数据存在则循环展示
                if (result.cs.length > 0) {
                    var cs = result.cs;
                    $('#update_customer_select').append('<option value="0">-----请选择-----</option>');
                    for (var i = 0; i < cs.length; i++) {
                        // 如果客户主键和机会表的客户外键一致时，选中
                        if (customer_id != cs[i].id) {
                            $('#update_customer_select').append('<option value="' + cs[i].id + '">' + cs[i].name + '</option>');
                        } else {
                            $('#update_customer_select').append('<option selected value="' + cs[i].id + '">' + cs[i].name + '</option>');
                        }
                    }
                }

                // 如果数据存在则循环展示
                if (result.ls.length > 0) {
                    var ls = result.ls;
                    $('#update_linkman_select').append('<option value="0">-----请选择-----</option>');
                    for (var i = 0; i < ls.length; i++) {
                        if (linkman_id != ls[i].id) {
                            $('#update_linkman_select').append('<option value="' + ls[i].id + '">' + ls[i].linkName + '</option>');
                        } else {
                            $('#update_linkman_select').append('<option selected value="' + ls[i].id + '">' + ls[i].linkName + '</option>');
                        }
                    }
                }

                // 如果数据存在则循环展示
                if (result.us.length > 0) {
                    var us = result.us;
                    $('#update_username_select').append('<option value="0">-----请选择-----</option>');
                    for (var i = 0; i < us.length; i++) {
                        if (user_id != us[i].id) {
                            $('#update_username_select').append('<option value="' + us[i].id + '">' + us[i].username + '</option>');
                        } else {
                            $('#update_username_select').append('<option selected value="' + us[i].id + '">' + us[i].username + '</option>');
                        }
                    }
                }
            }
        },
        'error': function (result) {
            console.log(result);
        }
    });

    $('#sales_sale_chance_update_dialog').dialog('open');
}

// 获取客户名称赋值给隐藏域
function get_update_customerName() {
    $('#update_customerName_hidden').val($('#update_customer_select').find("option:selected").text());
}

// 获取联系人名称赋值给隐藏域
function get_update_linkName() {
    // 判断如果不是请选择就查询电话号码
    if ('0' == $('#update_linkman_select').val()) {
        $('#update_linkPhone').val('');
        return;
    }

    // 联系人名称赋值给隐藏域
    $('#update_linkManName_hidden').val($('#update_linkman_select').find("option:selected").text());

    // 根据联系人id去查询电话返显至电话输入框
    $.ajax({
        'type': 'GET',
        'url': '/customer/select_link_phone_by_id/',
        'data': {
            'id': $('#update_linkman_select').val()
        },
        'dataType': 'json',
        'success': function (result) {
            // 如果是200 赋值
            if (200 == result.code) {
                $('#update_linkPhone').val(result.phone);
            }
        },
        'error': function (result) {
            console.log(result);
        }
    });
}

// 提交form表单
function sub_update_sale_chance_form() {
    $('#sales_sale_chance_update_form').form('submit', {
        url: '/sales/update_sale_chance/',
        success: function (result) {
            var obj = JSON.parse(result);

            // 显示提示信息
            $.messager.show({
                title: '提示',
                msg: obj.msg,
                timeout: 5000
            });

            // 如果code是200 清除对话框
            if (200 == obj.code) {
                // 关闭对话框
                $('#sales_sale_chance_update_dialog').dialog('close');

                $('#sales_sale_chance_update_form input').val('');
                $('#sales_sale_chance_update_form textarea').val('');
                $('#sales_sale_chance_update_form select').empty();

                // 重新加载数据
                select_params_sela_chance();
            }
        }
    });
}

// ----------------------------------修改营销机会------------------end----------------

// ----------------------------------删除营销机会-----------------start---------------
function delete_sale_chance() {
    // 判断必须选择且可以多选择
    var ids = $('#dg').datagrid('getChecked');

    if (0 == ids.length) {
        $.messager.alert('系统提示', '必须选择一条信息', 'warning');
        return;
    }

    $.messager.confirm('系统提示', '您确认想要删除这 ' + ids.length + ' 条记录吗？', function (r) {
        if (r) {
            // 拼接主键
            var sale_chance_ids = '';
            for (var i = 0; i < ids.length; i++) {
                if (i != ids.length - 1) {
                    sale_chance_ids += ids[i].id + ',';
                } else {
                    sale_chance_ids += ids[i].id;
                }
            }

            // 发送ajax删除数据
            $.ajax({
                'type': 'POST',
                'url': '/sales/delete_sale_chance/',
                'data': {
                    'ids': sale_chance_ids
                },
                'dataType': 'json',
                'success': function (result) {
                    // 显示提示信息
                    $.messager.show({
                        title: '提示',
                        msg: result.msg,
                        timeout: 5000
                    });

                    if (200 == result.code)
                        select_params_sela_chance();
                },
                'error': function (result) {
                    console.log(result);
                }
            });
        }
    });
}

// ----------------------------------删除营销机会------------------end----------------