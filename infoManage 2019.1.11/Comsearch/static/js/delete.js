function deleteUser(id) {
    if (window.confirm("您确认删除该条记录吗？")) {
        var post_data = {
            "userid": id
        };
        $.ajax({
            url: 'user_delete',
            type: 'POST',
            data: post_data,
            dataType: 'json',
            success: function (data) {
                alert(data["status"]);
                window.location.reload(true);//数据删除后，进行页面刷新
            }
        });
    } else {
        alert("删除失败");
    }
}
//批量选择checkbox
function seltAll() {
    var chckBoxSign = document.getElementById("selectAll");       //ckb 全选/反选的选择框id
    var chckBox = document.getElementsByName("chckBox");    //所有的选择框其那么都是chckBox
    var num = chckBox.length;
    if (chckBoxSign.checked) {
        for (var index = 0; index < num; index++) {
            chckBox[index].checked = true;
        }
    } else {
        for (var index = 0; index < num; index++) {
            chckBox[index].checked = false;
        }
    }
}
//批量删除数据
function deleteSelect() {
    var chckBox = document.getElementsByName("chckBox");
    var num = chckBox.length
    var ids = "";
    for (var index = 0; index < num; index++) {
        if (chckBox[index].checked) {
            ids += chckBox[index].value + ",";
        }
    }
    if (ids != "") {
        ids = ids.substring(0, ids.length - 1); //S 删除字符串最后一个字符的几种方法
        ids = {
            'ids': ids
        }
        if (window.confirm("确定删除所选记录？")) {
            $.ajax({
                type: "post",
                url: 'deledeSelect', //要自行删除的action
                data: ids,
                dataType: 'json',
                success: function (data) {
                    if (data["success"]) {
                        alert("删除成功");
                        window.location.reload(true);
                    }
                },
                error: function (data) {
                    alert("系统错误，删除失败");
                }
            });
        }
    } else {
        alert("请选择要删除的记录");
    }
}