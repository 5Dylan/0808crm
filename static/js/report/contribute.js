// 格式化总金额
function formatter_sum(value) {
    if (undefined == value || null == value) {
        return 0;
    } else {
        return value;
    }
}

// 查询
function select_contribute() {
    var name = $('#s_name').val();

    $('#dg').datagrid('reload', {
        name: name
    });
}