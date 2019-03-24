function selcity1() {
    var arr = [["--选择类型--"], ["财务类", "证券类", "经营类", "其他"]];
    var index = document.getElementById("selID").selectedIndex;

    if (index == 1) {
        $(document).ready(function () {
            $("#subID").show();
            $("#thirdID").show();
            // $("#emotion_importance_sel_1").show();
            // $("#emotion_importance_sel_2").show();
            // $("#emotion_importance_sel_3").show();
            for (var i=1; $("#emotion_importance_sel_"+i).length>0; i++) { //判断标签是否存在
                $("#emotion_importance_sel_"+i).show();
            }
        });

        var subNode = document.getElementById("subID");
        var news_type = arr[index];

        subNode.options.length = 0;   //清空之前选项
        for (var x = 0; x < news_type.length; x++) {
            var optNode = document.createElement("option");
            optNode.innerText = news_type[x];
            subNode.appendChild(optNode);  //选择添加到子选项中
        }
        selcity2();
    }
    else {
        $(document).ready(function () {
            $("#subID").hide();
            $("#subID").empty(); //清空select
            $("#subID").append("<option value=''></option>");  //添加一项option
            $("#thirdID").hide();
            $("#thirdID").empty();
            $("#thirdID").append("<option value=''></option>");  //添加一项option
            // $("#emotion_importance_sel_1").hide();
            // $("#emotion_importance_sel_1").val("");  //设置选中项
            // $("#emotion_importance_sel_2").hide();
            // $("#emotion_importance_sel_2").val("");  //设置选中项
            // $("#emotion_importance_sel_3").hide();
            // $("#emotion_importance_sel_3").val("");  //设置选中项
            for (var i=1; $("#emotion_importance_sel_"+i).length>0; i++) {
                $("#emotion_importance_sel_"+i).hide();
                $("#emotion_importance_sel_"+i).val("");  //设置选中项
            }

        });
    }

}

function selcity2() {
    var arr = [["财报", "业绩预期", "股权和资产交易", "借款、担保和质押"], ["发行证券", "价格变化", "偿还债券利息或分红", "增持、减持、回购或兑付", "临时或永久停止交易", "监管部门举措", "其他"],
        ["司法事件", "重大结构调整", "新增或终止业务", "人事调整", "主营业务重大调整", "突发事件", "其他"],[""]];
    if (document.getElementById("subID").value == "其他") {
        $(document).ready(function () {
            $("#thirdID").hide();
        });
    } else {
        $(document).ready(function () {
            $("#thirdID").show();
        });
    }
    var index = document.getElementById("subID").selectedIndex;
    var subNode = document.getElementById("thirdID");
    var news_type = arr[index];

    subNode.options.length = 0;   //清空之前选项
    for (var x = 0; x < news_type.length; x++) {
        var optNode = document.createElement("option");
        optNode.innerText = news_type[x];
        subNode.appendChild(optNode);  //选择添加到子选项中
    }
}





