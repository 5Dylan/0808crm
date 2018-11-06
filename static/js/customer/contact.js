// 初始化编辑器
$('#tt').edatagrid({
    url: '/customer/select_contact_by_customer_id/' + $('#id').val() + '/',
    saveUrl: '/customer/create_contact/' + $('#id').val() + '/',  // 保存时提交url
    updateUrl: '/customer/update_contact/',  // 修改时提交url
    destroyUrl: '/customer/delete_contact/',  // 删除时提交url
    pagination: true,  // 显示分页工具栏
    rownumbers: true,  // 显示行号
    width: 600,
    height: 333
});

// 添加行
function add() {
    $('#tt').edatagrid('addRow');
}

// 取消行
function cancel() {
    $('#tt').edatagrid('cancelRow');
}

// 删除行
function destroy() {
    $('#tt').edatagrid('destroyRow');
}

// 保存行
function save() {
    $('#tt').edatagrid('saveRow');
    setTimeout(function () {
        $('#tt').edatagrid('reload');
    }, 200);
}

// 格式化分配时间
function formatter_datetime(value) {
    if (undefined == value || null == value)
        return '';

    return value.replace('T', ' ');
}