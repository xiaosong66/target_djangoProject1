$(document).ready(function () {
    /*********************************** 用户登录信息图  *****************************************************/
        // 指定图表的配置项和数据
        // 分析用户home使用情况
    const myChart = echarts.init(document.getElementById('logInfo'));
    const option = {
        title: {
            text: '用户登录总览',
        },
        legend: {
            data: ['总次数', '成功次数', '失败次数']
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        toolbox: {
            show: true,
            orient: 'vertical',
            left: 'right',
            top: 'center',
            feature: {
                mark: {show: true},
                magicType: {show: true, type: ['bar', 'stack']},
                saveAsImage: {show: true}
            }
        },
        xAxis: {
            data: []
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                name: '总次数',
                type: 'bar',
                data: []
            },
            {
                name: '成功次数',
                type: 'bar',
                data: []
            },
            {
                name: '失败次数',
                type: 'bar',
                data: []
            }
        ]
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
    //获取用户登录信息
    $.ajax({
        url: '/LM/log_success_failure/',
        type: 'POST',
        dataType: 'json',
        headers: {"X-CSRFtoken": $.cookie("csrftoken")},
        success: function (data) {
            myChart.setOption({
                title: {
                    text: data[4],
                },
                xAxis: {
                    axisLabel: {
                        interval: 0
                    },
                    data: data[0]
                },
                series: [
                    {
                        // 根据名字对应到相应的系列
                        name: '总次数',
                        barGap: 0,
                        data: data[1]

                    },
                    {
                        name: '成功次数',
                        barGap: 0,
                        data: data[2]
                    },
                    {
                        name: '失败次数',
                        barGap: 0,
                        data: data[3]
                    }
                ]
            })
        }
    })
    /********  echarts 绘制地图  */

    //地图点击
    /*
        刷新数据库的内容，并显示到主页
     */
    function showItems(data) {
        //将ajax的缓存数据取出显示
        const parser = new DOMParser();
        const htmlData = parser.parseFromString(data, 'text/html');
        const obj = htmlData.getElementById('showItems').innerHTML;
        $("#showItems").html(obj);
    }

    //图表的点击事件
    myChart.on('click', function (paras) {
        // 请求失败的信息
        $.ajax({
            url: '/LM/solve_log_failure/',
            type: 'POST',
            data: {
                'ip': paras.name,
                'type': paras.seriesName,
            },
            dataType: 'text',
            headers: {"X-CSRFtoken": $.cookie("csrftoken")},
            success: function (data) {
                showItems(data)
                $('#showLogInfoTitle').text(paras.name + '登录' + paras.seriesName + '详情：')
            }
        });
    })

    //加载页面时显示的信息
    $.ajax({
        url: '/LM/get_now_info/',
        type: 'POST',
        dataType: 'text',
        headers: {"X-CSRFtoken": $.cookie("csrftoken")},
        success: function (data) {
            showItems(data)
        }
    });
    /************************************ 管理登录信息 *******************/
        //信任此次登录
    let id;
    $(document).on("click", ".trustBTN", function () {
        id = $(this).parents('tr').attr('id')
    })
    $("#rightTrust").on('click', function () {
        const trustVal = $("input[name='if_trust']:checked").val();
        const formData = new FormData;
        formData.append('trustVal', trustVal)
        formData.append('id', id)
        $.ajax({
            url: '/LM/verify_logLocation/',
            data: formData,
            type: 'POST',
            dataType: 'text',
            contentType: false,
            processData: false,
            headers: {"X-CSRFtoken": $.cookie("csrftoken")},
            success: function () {
                console.log('1')
            }
        })
    })

    let form = $("#pdManageForm");
    //获取邮件验证码
    $("#getAuthCodeBtn").on("click", function () {
        $.ajax({
            url: "/LM/sendMessage/",
            type: "POST",
            data: form.serialize(),
            dataType: "text",
            // headers: {"X-CSRFtoken": $.cookie("csrftoken")},
            success: function (data) {
                console.log(data)
                if (data === '验证码发送成功') {
                    alert("验证码发送成功")
                } else if (data === '邮箱空') {
                    alert("邮箱不能为空")
                }
                //消息弹窗
            },
        });
    });
    //修改密码
    $('#modifyPD_right').on('click', function () {
        $.ajax({
            url: "/LM/modifyPD/",
            type: "POST",
            data: form.serialize(),
            dataType: "text",
            // headers: {"X-CSRFtoken": $.cookie("csrftoken")},
            success: function (data) {
                alert(data)
                if (data === '密码修改成功') {
                    form[0].reset()
                    //用于修改登录信息状态
                    $.ajax({
                        url: "/LM/verify_loc_modifyPD/",
                        type: "POST",
                        dataType: "text",
                        headers: {"X-CSRFtoken": $.cookie("csrftoken")},
                        success: function () {
                        }
                    })
                }
            },
        });
    })

    //查询功能
    $("#searchBtn").click(function () {
        let searchContent = $("#inquireContent").val()
        $("#showLogInfoTitle").html("检索信息")
        $.post('/LM/searchLoginInfo/', {'searchContent': searchContent}, function (data) {
            showItems(data)
        })
    })

    // 授权功能
    $(document).on('click', '.authBtn', function (data){
        const id = $(this).parents('tr').attr('id')
        $.post('/LM/get_authIp_info/', {'id': id}, function (data){
            const parser = new DOMParser();
            const htmlData = parser.parseFromString(data, 'text/html');
            const obj = htmlData.getElementById("authModal").innerHTML;
            $("#authModal").html(obj);

            const myModal = new bootstrap.Modal(document.getElementById('authModal'))
            myModal.show()
        })
    })

    //字符串日期转换为Date型
    function stringToDate(strDate) {
        const arr = strDate.match(/\d+/g);
        if (strDate !== 'None') {
            if (Number(arr[1]) < 10) {
                arr[1] = '0' + arr[1]
            }
            if (Number(arr[2]) < 10) {
                arr[2] = '0' + arr[2]
            }

            return arr[0] + '-' + arr[1] + '-' + arr[2] + 'T' + arr[3] + ':' + arr[4]
        } else {
            return ''
        }
    }


})
