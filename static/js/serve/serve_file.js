// 初始化服务对话框
$('#dialog').dialog({
    title: '服务处理',
    width: 700,
    height: 450,
    resizable: false,
    modal: true, // 模态
    draggable: false, // 不可移动
    closed: true, // 是否关闭
    buttons: [{
        text: '关闭',
        iconCls: 'icon-cancel',
        handler: function () {
            $('#dialog').dialog('close');
            // 清空对话框
            $('#fm input').val('');
            $('#fm textarea').val('');
        }
    }]
});

// 格式化时间
function formatter_datetime(value) {
    if (undefined == value || null == value)
        return '';

    return value.replace('T', ' ');
}

// 打开服务分配对话框
function open_serve_dialog() {
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

    // 格式化时间
    row[0].createDate = row[0].createDate.replace('T', ' ');
    row[0].assignTime = row[0].assignTime.replace('T', ' ');
    row[0].serviceProcePeople = row[0].serviceProcePeople.replace('T', ' ');
    $('#fm').form('load', row[0]);
    $('#dialog').dialog('open');
}


// 按条件查询
function select_params_serve() {
    // 获取参数
    var customer = $('#s_customer').val().trim();
    var overview = $('#s_overview').val().trim();
    var serveType = $('#s_serveType').combobox('getValue');

    var createTimefrom = $("#s_createDatefrom").datebox("getValue");
    if (createTimefrom != null && $.trim(createTimefrom).length > 0) {
        createTimefrom += " 00:00:00";
    }

    var createDateto = $("#s_createDateto").datebox("getValue");
    if (createDateto != null && $.trim(createDateto).length > 0) {
        createDateto += " 23:59:59";
    }

    $('#dg').datagrid('reload', {
        customer: customer,
        overview: overview,
        serveType: serveType,
        createTimefrom: createTimefrom,
        createDateto: createDateto
    });
}

// 切换分配状态立即查询
$("#s_state").combobox({
    onChange: function () {
        select_params_serve();
    }
});