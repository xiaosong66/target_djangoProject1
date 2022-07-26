$(document).ready(function () {
    const dom = document.getElementById("userRiskValueChart");
    const myChart = echarts.init(dom);

    let option;


    option = {
        //提示框
        tooltip: {
            trigger: 'item',
            formatter: "{b}: {c} ({d}%)",

        },
        // 图例，图旁边的格子
        legend: {
            orient: 'vertical',
            top: '5%',
            left: '10%'
        },
        title: {
            show: true,
            text: "用户安全系数",  //主标题文本
            link: "#",        // 主标题连接
            target: 'self',        //指定窗口打开主标题超链接，支持 'self' | 'blank'，不指定等同为 'blank'（新窗口）
            subtext: '~/100',   //副标题文本
            sublink: '#',     //副标题连接
            subtarget: 'self', //指定窗口打开副标题超链接，支持 'self' | 'blank'，不指定等同为 'blank'（新窗口）
            textAlign: 'center', //水平对齐方式，默认根据x设置自动调整，可选为： left' | 'right' | 'center
            left: '59%',
            top: '44%',
            // x: 'center',
            // y: 'center',
            // backgroundColor: 'rgba(0,0,0,0)',//标题背景颜色，默认 'rgba(0,0,0,0)' 透明
            // borderColor: '#ccc',//标题边框颜色,默认'#ccc'
            // borderWidth: 0,//标题边框线宽，单位px，默认为0（无边框）
            // padding: 5,//标题内边距，单位px，默认各方向内边距为5，接受数组分别设定上右下左边距
            // itemGap: 10,//主副标题纵向间隔，单位px，默认为10
            textStyle: {
                fontSize: 20,
                color: '#454c5c',
                align: 'center'
            },
            subtextStyle: {
                fontFamily: "微软雅黑",
                fontSize: 18,
                color: '#6c7a89',
            }
        },
        series: [
            {
                name: '风险评分图',
                type: 'pie',
                id: '',
                radius: ['30%', '65%'],  // 由40%到70%的圆
                center: ['60%', '50%'],
                avoidLabelOverlap: false,
                selectedMode: "single",
                selectedOffset: 10,
                // 选中样式
                select: {   //开启selectedMode有效
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    },
                    label: {
                        show: true,
                        fontSize: '40',
                        fontWeight: 'bold',
                        formatter: "{b}\n{c}({d}%)",
                    },
                },
                // 块样式
                itemStyle: {
                    borderRadius: 10,
                    borderColor: '#fff',
                    borderWidth: 2,
                },
                //标签样式
                label: {
                    show: false,
                    position: 'center',
                },
                // 悬浮样式
                emphasis: {
                    focus: 'self',  // 聚焦当前淡出其他
                    blurScope: 'coordinateSystem',
                    // label: {
                    //     show: true,
                    //     fontSize: '40',
                    //     fontWeight: 'bold',
                    //     position: 'top',
                    //     formatter:"{a} {b} {c} {d}",
                    // },
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    },
                },
                // 指示线
                labelLine: {
                    show: false
                },
                // 数据集
                data: [
                    {value: 20, name: '密码安全评分'},
                    {value: 20, name: '资产安全评分'},
                    {value: 20, name: '账户安全评分'},
                    {value: 20, name: '行为安全评分'},
                    {value: 20, name: '其他安全评分'}
                ]
            }
        ],
    };
    // 获取总评分
    $.ajax({
        url: "/RW/getSecurityScore/",
        type: 'POST',
        dataType: 'json',
        success: function (result) {
            myChart.setOption({
                title: {
                    subtext: result[5][1] + '/100',
                },
                series: [{
                    data: [
                        {value: result[0][1], name: result[0][0]},
                        {value: result[1][1], name: result[1][0]},
                        {value: result[2][1], name: result[2][0]},
                        {value: result[3][1], name: result[3][0]},
                        {value: result[4][1], name: result[4][0]},
                    ]
                }]
            })
        }
    })

    if (option && typeof option === 'object') {
        myChart.setOption(option);
    }
    const hideTitle = {
        title: {
            show: false,
        }
    }
    const showTitle = {
        title: {
            show: true,
        }
    }
    let num = 0;
    let title;
    // 用来切换右边的标题
    let now_title;
    myChart.on("click", function (paras) {
        if (title !== paras.name) {
            title = paras.name
            num = 1
            $("#showTitle").html(title)
            now_title = $("#showTitle").html()
        } else {
            num += 1
            if ((num % 2) === 0) {
                $("#showTitle").html("风险评分总览")
                now_title = $("#showTitle").html()
            } else {
                $("#showTitle").html(title)
                now_title = $("#showTitle").html()
            }
        }
        // 显示需要展示的内容
        if (now_title === "密码安全评分") {
            $("#pdSecurity").removeAttr("hidden")
            hideOther(now_title)
        } else if (now_title === "资产安全评分") {
            $("#propertySecurity").removeAttr("hidden")
            hideOther(now_title)
        } else if (now_title === "其他安全评分") {
            $("#otherSecurity").removeAttr("hidden")
            hideOther(now_title)
        } else if (now_title === "账户安全评分") {
            $("#accountSecurity").removeAttr("hidden")
            hideOther(now_title)
        } else if (now_title === "行为安全评分") {
            $("#actionSecurity").removeAttr("hidden")
            hideOther(now_title)
        }
    })

    //隐藏其他类容
    const contents = [
        {"title": "风险评分总览", "id": "allRisk"},
        {"title": "密码安全评分", "id": "pdSecurity"},
        {"title": "资产安全评分", "id": "propertySecurity"},
        {"title": "其他安全评分", "id": "otherSecurity"},
        {"title": "账户安全评分", "id": "accountSecurity"},
        {"title": "行为安全评分", "id": "actionSecurity"},
    ]

    function hideOther(showObjTitle) {
        for (let i = 0; i < contents.length; i++) {
            if (contents[i].title === showObjTitle) {
                continue;
            }
            $('#' + contents[i].id).prop("hidden", "hidden")
        }
    }


    //显示和隐藏标题
    myChart.on('select', 'series', function () {
        myChart.setOption(hideTitle)
    })
    myChart.on('unselect', 'series', function () {
        hideOther("风险评分总览")
        $("#allRisk").removeAttr("hidden")
        myChart.setOption(showTitle)
    })


})