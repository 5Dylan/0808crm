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
    row[0].serviceProcePeople = $('#session_username').val();
    // 状态改为已分配
    row[0].state = '已处理';
    $('#fm').form('load', row[0]);
    $('#dialog').dialog('open');
}