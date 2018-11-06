// 初始化修改密码dialog
$('#system_index_update_password_dialog').dialog({
    title: '修改密码',
    iconCls: 'icon-edit',
    resizable: false,
    modal: true, // 模态
    draggable: false, // 不可移动
    closed: true, // 是否关闭
    width: 260,
    buttons: [{  // 按钮
        text: '保存',
        iconCls: 'icon-save',
        handler: function () {
            var flag = $('#system_index_update_password_form').form('validate');
            if (flag) {
                // 提交表单
                sub_system_index_updatepwd_form();

                // 清除form表单input
                $('#system_index_update_password_form input').val('');

                // 关闭修改密码dialog
                $('#system_index_update_password_dialog').dialog('close');
            }
        }
    }, {
        text: '关闭',
        iconCls: 'icon-cancel',
        handler: function () {
            $('#system_index_update_password_dialog').dialog('close');
        }
    }]
});

// 点击修改密码弹出对话框
function open_update_password_dialog(username) {
    // 返显用户名
    $('#username').val(username);
    $('#system_index_update_password_dialog').dialog('open');
}

// 提交修改密码表单
function sub_system_index_updatepwd_form() {
    // 给csrf_token隐藏域赋值
    $('#csrfmiddlewaretoken').val($.cookie('csrftoken'));

    $('#system_index_update_password_form').form('submit', {
        url: '/system/update_password/',
        success: function (result) {
            var obj = JSON.parse(result);

            // 显示提示信息
            $.messager.show({
                title: '提示',
                msg: obj.msg,
                timeout: 5000
            });

            // 退出系统，清除cookie，清除session
            if (200 == obj.code) {
                // 前台清除cookie
                $.removeCookie('login_password_cookie',
                    {'expires': 15, 'path': '/', 'domain': 'crm.com'});

                // 后台清除session

                // 为了保证用户可以看到提示信息，我们要延迟执行
                setTimeout(function () {
                    window.location.href = '/system/logout/'
                }, 2000);
            }
        }
    });
}

// 安全退出 后台清除session
function logout() {
    // 弹出提示框是否退出
    $.messager.confirm('是否退出', '您确认要退出系统吗？', function (r) {
        if (r) {
            // 清除cookie保留用户名
            $.removeCookie('login_password_cookie',
                {'expires': 15, 'path': '/', 'domain': 'crm.com'});

            // 请求后台
            window.location.href = '/system/logout/';
        }
    });
}

// 打开一个新的tab页面
function openTab(title, url, iconCls) {
    // 选项面板是否存在，存在选中，不存在添加
    var flag = $('#tabs').tabs('exists', title);

    if (flag) {
        $('#tabs').tabs('select', title);
    } else {
        $('#tabs').tabs('add', {
            title: title,
            iconCls: iconCls,
            closable: true,  // 是否可以关闭
            // href: '/sales/sale_chance_index/',  // 跳转请求打开对应的页面，样式会出问题
            // 新增一个iframe窗口
            content: "<iframe frameborder=0 scrolling='auto' style='width:99%;height:99%' src='" + url + "'></iframe>",
        });
    }
}