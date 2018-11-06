/**
 * 扩展validatebox
 *      value代表当前输入框自己的值
 *      param代表验证接收到的值
 */
$.extend($.fn.validatebox.defaults.rules, {
    // 验证密码长度 8~16位
    check_pwd_length: {
        validator: function (value) {

            return (value.length >= 8 && value.length <= 16);
        },
        message: '密码长度必须为8~16位'
    },

    // 正则验证密码规范 大小写数字特殊字符
    regex_check_pwd: {
        validator: function (value) {
            var reg = /^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)(?=.*?[#@*&.])[a-zA-Z\d#@*&.]{8,16}$/;

            return reg.test(value);
        },
        message: '密码必须是大小写字母/数字/特殊符号'
    },

    // 两次密码一致
    eq_pwd: {
        validator: function (value, param) {
            return value == $(param[0]).val();
        },
        message: '两次密码不一致'
    }
});