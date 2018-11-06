// ----------------------------------注册------------start----------------------
// 点击注册显示注册div，隐藏登录div
$('#reg_a').on('click', function () {
    $('#log-in').hide();
    $('#register').show();
});

// 点击登录显示登录div
$('#login_a').on('click', function () {
    $('#register').hide();
    $('#log-in').show();
});

// 验证用户名 必须字母加数字
function reg_check_username() {
    var flag = false;

    // 获取用户名
    var username = $('#reg_username').val().trim();

    // 验证用户名 字母或者字母加数字必须字母开头 最少4位 最多16位
    var reg = /^[a-zA-Z][a-zA-Z0-9]{4,16}$/;

    if (!reg.test(username)) {
        $('#reg_span').html('用户名必须是字母开头，4~16位');
        return flag;
    }

    // 合法后清空提示
    $('#reg_span').html('');

    // 发送ajax请求验证用户名唯一
    $.ajax({
        'type': 'POST',
        'url': '/system/unique_username/',
        'async': false,
        'data': {
            'csrfmiddlewaretoken': $.cookie('csrftoken'),
            'username': username
        },
        'dataType': 'json',
        'success': function (result) {
            // 如果是400 设置为false返回
            if (400 == result.code) {
                flag = false;
                $('#reg_span').html(result.msg);
            }

            // 如果是200 正常显示
            if (200 == result.code) {
                flag = true;
                $('#reg_span').html(result.msg);
            }
        },
        'error': function (result) {
            console.log(result);
        }
    });
    return flag;
}

$('#reg_username').on('blur', reg_check_username);

// 验证邮箱格式 丢失焦点事件
function reg_check_email() {
    var flag = false;

    // 获取邮箱
    var email = $('#reg_email').val().trim();

    // 非空判断
    if (undefined == email || '' == email) {
        $('#reg_span').html('邮箱不能为空');
        return flag;
    }

    // 验证邮箱
    var reg = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/;
    if (!reg.test(email)) {
        $('#reg_span').html('请输入正确的邮箱格式');
        return flag;
    }

    // 合法后清空提示
    $('#reg_span').html('');

    // 发送ajax请求验证用户名唯一
    $.ajax({
        'type': 'POST',
        'url': '/system/unique_username/',
        'async': false,
        'data': {
            'csrfmiddlewaretoken': $.cookie('csrftoken'),
            'email': email
        },
        'dataType': 'json',
        'success': function (result) {
            // 如果是400 设置为false返回
            if (400 == result.code) {
                flag = false;
                $('#reg_span').html(result.msg);
            }

            // 如果是200 正常显示
            if (200 == result.code) {
                flag = true;
                $('#reg_span').html(result.msg);
            }
        },
        'error': function (result) {
            console.log(result);
        }
    });
    return flag;
}

$('#reg_email').on('blur', reg_check_email);

// 验证密码 必须数字大小写字母特殊符号组成 最少8位 最多16位
function reg_check_password() {
    // 获取密码
    var pwd = $('#reg_password').val().trim();

    // 判断密码是否满足长度
    if (pwd.length < 8 || pwd.length > 16) {
        $('#reg_span').html('密码长度必须在8~16位之间');
        return false;
    }

    // 验证密码
    var reg = /^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)(?=.*?[#@*&.])[a-zA-Z\d#@*&.]{8,16}$/;

    if (!reg.test(pwd)) {
        $('#reg_span').html('请输入正确的密码');
        return false;
    }

    // 合法后清空提示
    $('#reg_span').html('');
    return true;
}

$('#reg_password').on('blur', reg_check_password);

// 重复密码 获取密码的值进行比较
function reg_check_password2() {
    // 获取密码
    var pwd = $('#reg_password').val().trim();
    // 获取重复密码
    var pwd2 = $('#reg_password2').val().trim();

    // 非空判断
    if (undefined == pwd2 || '' == pwd2) {
        $('#reg_span').html('重复密码不能为空');
        return false;
    }

    // 进行比较
    if (pwd2 != pwd) {
        $('#reg_span').html('两次密码不一致');
        return false;
    }

    // 合法后清空提示
    $('#reg_span').html('');
    return true;
}

$('#reg_password2').on('blur', reg_check_password2);

// 点击注册按钮再次验证数据合法性
$('#reg_btn').on('click', function () {
    // 点击注册以后置灰按钮
    $('#reg_btn').attr("disabled", "true");

    var flag = reg_check_username();
    if (!flag)
        return;
    flag = reg_check_email();
    if (!flag)
        return;
    flag = reg_check_password();
    if (!flag)
        return;
    flag = reg_check_password2();
    if (!flag)
        return;

    // 合法的话 发送邮件 激活账号
    // 获取用户名
    var username = $('#reg_username').val().trim();
    // 获取邮箱
    var email = $('#reg_email').val().trim();
    // 获取密码
    var password = $('#reg_password').val().trim();
    $.ajax({
        'type': 'POST',
        'url': '/system/send_email/',
        'async': false,
        'data': {
            'csrfmiddlewaretoken': $.cookie('csrftoken'),
            'email': email,
            'username': username,
            'password': password
        },
        'dataType': 'json',
        'success': function (result) {
            // 如果是400 显示错误信息
            if (400 == result.code) {
                $('#reg_span').html(result.msg);
            }

            // 如果是200 正常显示
            if (200 == result.code) {
                $('#reg_span').html(result.msg);
            }
        },
        'error': function (result) {
            console.log(result);
        }
    });
});
// ----------------------------------注册-------------end-----------------------

// ----------------------------------登录--------------start--------------------
// 用户名非空验证
function login_check_username() {
    username = $('#login_username').val().trim();

    if (undefined == username || '' == username) {
        $('#login_span').html('请输入用户名');
        return false;
    }

    $('#login_span').html('');
    return true;
}

$('#login_username').on('blur', login_check_username);

// 密码非空验证
function login_check_password() {
    password = $('#login_password').val().trim();

    if (undefined == password || '' == password) {
        $('#login_span').html('请输入密码');
        return false;
    }

    $('#login_span').html('');
    return true;
};
$('#login_password').on('blur', login_check_password);

// 登录
function login_user() {
    var flag = login_check_username();
    if (!flag)
        return;

    flag = login_check_password();
    if (!flag)
        return;

    // 判断是否选择了记住密码
    var remember = $('#remember').is(':checked');

    // 登录
    $.ajax({
        'type': 'POST',
        'url': '/system/login_user/',
        'async': false,
        'data': {
            'csrfmiddlewaretoken': $.cookie('csrftoken'),
            'username': username,
            'password': password,
            'remember': remember
        },
        'dataType': 'json',
        'success': function (result) {
            // 如果是400 显示错误信息
            if (400 == result.code) {
                $('#login_span').html(result.msg);
            }

            // 如果是200 正常显示
            if (200 == result.code) {
                // 如果用户选择了记住密码
                if (!(undefined == result.login_username_cookie || null == result.login_username_cookie)) {
                    // 设置cookuie，有效时间为15天
                    $.cookie('login_username_cookie', result.login_username_cookie,
                        {'expires': 15, 'path': '/', 'domain': 'crm.com'});

                    $.cookie('login_password_cookie', result.login_password_cookie,
                        {'expires': 15, 'path': '/', 'domain': 'crm.com'});
                }

                window.location.href = '/index/'
            }
        },
        'error': function (result) {
            console.log(result);
        }
    });
}
$('#login_btn').on('click', login_user);

// 进入页面就执行的方法
$(function () {
    // 获取login_cookie，赋值到登录框
    var username = $.cookie('login_username_cookie');
    var password = $.cookie('login_password_cookie');

    // 判断是否存在cookie
    if (!(undefined == username || null == username)) {
        // base64解密cookie
        username = $.base64.decode(username);
        // 赋值到登录框
        $('#login_username').val(username);
    }

    if (!(undefined == password || null == password)) {
        // base64解密cookie
        password = $.base64.decode(password);
        // 赋值到登录框
        $('#login_password').val(password);
    }

    // 实现免登陆，判断session
    // login_user()
});
// ----------------------------------登录---------------end---------------------