// 初始化ueditor
var editor;
$(function () {
    // 具体参数配置在  editor_config.js中
    var options = {
        // 表示层级
        zIndex: 999,
        // 初化宽度
        initialFrameWidth: "90%",
        // 初化高度
        initialFrameHeight: 200,
        // 初始化时，是否让编辑器获得焦点true或false
        focus: false,
        // 允许的最大字符数 'fullscreen'
        maximumWords: 99999,
        removeFormatAttributes: 'class,style,lang,width,height,align,hspace,valign',
        // 是否默认为纯文本粘贴。false为不使用纯文本粘贴，true为使用纯文本粘贴
        pasteplain: false,
        autoHeightEnabled: true,
        // 自动排版设置
        /* autotypeset: {
            mergeEmptyline: true,        //合并空行
            removeClass: true,           //去掉冗余的class
            removeEmptyline: false,      //去掉空行
            textAlign: "left",           //段落的排版方式，可以是 left,right,center,justify 去掉这个属性表示不执行排版
            imageBlockLine: 'center',    //图片的浮动方式，独占一行剧中,左右浮动，默认: center,left,right,none 去掉这个属性表示不执行排版
            pasteFilter: false,          //根据规则过滤没事粘贴进来的内容
            clearFontSize: false,        //去掉所有的内嵌字号，使用编辑器默认的字号
            clearFontFamily: false,      //去掉所有的内嵌字体，使用编辑器默认的字体
            removeEmptyNode: false,      //去掉空节点
                                         //可以去掉的标签
            removeTagNames: {"font": 1},
            indent: false,               // 行首缩进
            indentValue: '0em'           //行首缩进的大小
        }*/
        toolbars: [
            ['fullscreen', 'source', '|', 'undo', 'redo', '|', 'bold', 'italic', 'underline', 'fontborder', 'strikethrough', 'superscript', 'subscript', 'removeformat', 'formatmatch', 'autotypeset', 'blockquote', 'pasteplain', '|', 'forecolor', 'backcolor', 'insertorderedlist', 'insertunorderedlist', 'selectall', 'cleardoc', '|', 'rowspacingtop', 'rowspacingbottom', 'lineheight', '|', 'customstyle', 'paragraph', 'fontfamily', 'fontsize', '|', 'directionalityltr', 'directionalityrtl', 'indent', '|', 'justifyleft', 'justifycenter', 'justifyright', 'justifyjustify', '|', 'touppercase', 'tolowercase', '|', 'link', 'unlink', 'anchor', '|', 'imagenone', 'imageleft', 'imageright', 'imagecenter', '|', 'insertimage', 'emotion', 'insertvideo', 'attachment', 'map', 'gmap', 'insertframe', 'insertcode', 'webapp', 'pagebreak', 'template', 'background', '|', 'horizontal', 'date', 'time', 'spechars', 'wordimage', '|', 'inserttable', 'deletetable', 'insertparagraphbeforetable', 'insertrow', 'deleterow', 'insertcol', 'deletecol', 'mergecells', 'mergeright', 'mergedown', 'splittocells', 'splittorows', 'splittocols', '|', 'print', 'preview', 'searchreplace']
        ]
    };
    editor = new UE.ui.Editor(options);
    editor.render("serviceRequest"); //  指定textarea的id

    // 面板默认和父容器窗口大小一致
    $('#p').panel('maximize', 'true');
});

// 重置以后唤醒保存按钮
function reset() {
    $('#serveType').combobox('setValue', '请选择服务类型');
    $('#customer').combobox('setValue', '请选择客户名称');
    $('#fm input').val('');
    $('#fm textarea').val('');
    $('#save_btn').linkbutton('enable');
}

// 保存以后置灰按钮
function save_serve() {
    $('#fm').form('submit', {
        url: '/serve/create_serve/',
        success: function (result) {
            var obj = JSON.parse(result);

            $.messager.show({
                title: '系统提示',
                msg: obj.msg,
                timeout: 5000
            });

            if (200 == obj.code) {
                $('#save_btn').linkbutton('disable');
            }
        }
    });
}