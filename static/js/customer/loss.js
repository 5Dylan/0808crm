// 格式化分配时间
function formatter_datetime(value) {
    if (undefined == value || null == value)
        return '';

    return value.replace('T', ' ');
}

// 格式化状态
function formatter_state(value) {
    if ('0' == value)
        return '暂缓流失';

    if ('1' == value)
        return '确认流失';

    return value;
}

// 操作
function handler(value, row, index) {
    if (0 == row.state) {
        // 如果是暂缓流失，返回可点击链接
        return '<a href="javascript:reprieve(' + row.id + ');">暂缓流失措施</a>';
    } else if (1 == row.state) {
        // 如果是确认流失，返回文本显示
        return '客户确认流失';
    }
}

// 暂缓流失措施
function reprieve(id) {
    // 打开一个新窗口
    window.parent.openTab('暂缓流失措施', '/customer/reprieve_index/?id=' + id, 'icon-khlsgl');
}

// 带条件查询
// c 代表customer r代表report
function select_params_loss(type) {
    // 获取参数
    var cusName = $('#cusName').val().trim();
    var cusManager = $('#cusManager').val().trim();


    if ('c' == type) {
        var state = $('#state').combobox('getValue');
        $('#dg').datagrid('reload', {
            cusName: cusName,
            cusManager: cusManager,
            state: state
        });
    } else if ('r' == type) {
        $('#dg').datagrid('reload', {
            cusName: cusName,
            cusManager: cusManager
        });
    }
}

// 切换状态立即查询
$("#state").combobox({
    onChange: function () {
        select_params_loss($('#type').val());
    }
});
