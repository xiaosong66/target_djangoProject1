$(document).ready(function () {
    // 全选/全取消
    $("thead input[type=checkbox]").click(function () {
        $("tbody input[type=checkbox]").prop("checked", $(this).prop("checked"));
    })
    // 其他按钮 click只能静态绑定
    $(document).on('click', 'tbody input[type=checkbox]', function () {
        if ($("#showShareItems input[type=checkbox]:checked").length === $("#showShareItems input[type=checkbox]").length) {
            $("thead input[type=checkbox]").prop("checked", true);
        } else {
            $("thead input[type=checkbox]").prop("checked", false);
        }
    })
    $(document).on('click', 'tbody input[type=checkbox]', function () {
        if ($("#showIpItems input[type=checkbox]:checked").length === $("#showIpItems input[type=checkbox]").length) {
            $("thead input[type=checkbox]").prop("checked", true);
        } else {
            $("thead input[type=checkbox]").prop("checked", false);
        }
    })

    //取得现在时间
    function get_now_time() {
        const myDate = new Date();
        const year = myDate.getFullYear();
        const month = myDate.getMonth() + 1;
        const day = myDate.getDate();
        const h = myDate.getHours();              //获取当前小时数(0-23)
        let m = myDate.getMinutes();          //获取当前分钟数(0-59)
        if (m < 10) {
            m = '0' + m
        }
        return year + '年' + month + "月" + day + "日 " + h + ':' + m;
    }

    /******************************资产授权信息 ************************/

    /*
        刷新数据库的内容，并显示到主页
     */
    function showPropertiesItems(data) {
        //将ajax的缓存数据取出显示
        const parser = new DOMParser();
        const htmlData = parser.parseFromString(data, 'text/html');
        const obj = htmlData.getElementById('showShareItems').innerHTML;
        $("#showShareItems").html(obj)
        //修改高度
        // const num = htmlData.getElementById('num').innerHTML;
        // //const pri_height = $("#propertyAuthInfo").css('height').match(/\d+/);
        // const final_height = num * 48 + 100
        // $("#propertyAuthInfo").css('height', final_height + 'px')
    }

    //请求资产信息
    $.ajax({
        url: '/AM/get_propertyAuth_info/',
        type: 'POST',
        data: {'tag': 1},
        headers: {"X-CSRFtoken": $.cookie("csrftoken")},
        success: function (data) {
            showPropertiesItems(data);
            console.log("资产授权信息查询成功");
        },
    });

    //修改资产授权
    $(document).on('click', '.modifyPropertyBtn', function () {
        const siblings = $(this).parents('tr').children(); // 获取所有兄弟结点
        $("#modify_auth_file_id").val($(this).parents('tr').attr('id'))
        $("#shared_username").val(siblings[3].innerHTML);
        $("#M_share_start_time").val(stringToDate(siblings[4].innerHTML));
        $("#M_share_end_time").val(stringToDate(siblings[5].innerHTML));
        $("#sharedFile_describe").val(siblings[6].children[0].innerHTML);

        $("#affirm_modify_share").on('click', function () {
            const form = $("#modifyPropertyForm")
            $.ajax({
                url: '/AM/modify_auth_property/',
                data: form.serialize(),
                type: 'POST',
                dataType: "text",
                headers: {"X-CSRFtoken": $.cookie("csrftoken")},
                success: function (data){
                    if(data==="修改失败"){
                        alert("修改失败")
                    } else {
                        showPropertiesItems(data)
                        new bootstrap.Toast(document.querySelector("#editOK")).show();
                    }
                }
            });
        });
    });

    // 删除一条资产授权
    $(document).on('click', '.deletePropertyBtn', function () {
        const delete_property_id = $(this).parents('tr').attr('id');

        $('#affirm_delete_Property').on('click', function () {
            $.ajax({
                url: '/AM/delete_auth_property/',
                data: {delete_property_id: delete_property_id},
                type: 'POST',
                dataType: "text",
                headers: {"X-CSRFtoken": $.cookie("csrftoken")},
                success: function (data){
                    if(data==="删除失败"){
                        alert("删除失败")
                    } else {
                        showPropertiesItems(data)
                        new bootstrap.Toast(document.querySelector("#deleteOK")).show();
                    }

                },
            })
        });
    });

    //删除选中的授权资产
    $("#deleteAllSelectedPropertiesBtn").on('click', function () {
        const chk_value_properties = [];
        const myModal = new bootstrap.Modal(document.getElementById('deleteSelectedAuthPropertyModal'))

        $('#showShareItems input[type=checkbox]:checked').each(function () {
            chk_value_properties.push($(this).parents('tr').attr('id'))
        });
        // console.log(chk_value_properties.length === 0 ? '未选中任何' : chk_value_properties)
        if (chk_value_properties.length === 0) {
            alert("未选中任何")
        } else {
            myModal.show()
        }
        //删除所有选中的item
        $("#affirm_deleteAllSelected_Property").click(function () {
            $.ajax({
                url: "/AM/delete_selectAll_properties/",
                type: "POST",
                data: {
                    'chk_id': JSON.stringify(chk_value_properties)
                },
                dataType: "text",
                headers: {"X-CSRFtoken": $.cookie("csrftoken")},
                success: function (data) {
                    //将ajax的缓存数据取出显示
                    if(data==='数据删除失败') {
                        alert("数据删除失败")
                    } else {
                        showPropertiesItems(data)
                        new bootstrap.Toast(document.querySelector("#deleteOK")).show();
                    }
                },
                error: function () {
                    alert("删除所选失败");
                }
            })
        });
    });


    /******************************资产授权信息 ************************/

    /******************************ip授权信息 ************************/
    //显示ip信息
    function showIpAuth(data) {
        //将ajax的缓存数据取出显示
        const parser = new DOMParser();
        const htmlData = parser.parseFromString(data, 'text/html');
        const obj = htmlData.getElementById('showIpItems').innerHTML;
        $("#showIpItems").html(obj)
    }

    //获取ip授权信息
    $.ajax({
        url: '/AM/get_auth_ip/',
        type: 'POST',
        dataType: "text",
        contentType: 'text/html',
        headers: {"X-CSRFtoken": $.cookie("csrftoken")},
        success: function (data) {
            showIpAuth(data);
            // console.log("所有数据查询成功");
        },
    })

    //新增ip授权信息
    // off先解除绑定，防止重复绑定
    $("#addNewLoginIpBtn").off('click').on('click', function () {
        $("#M_create_time").val(get_now_time())
        const form = $("#addNewIpForm")
        $("#affirm_addNewIp").off('click').on('click', function () {
            $.ajax({
                url: '/AM/add_new_authIP/',
                data: form.serialize(),
                type: 'POST',
                dataType: "text",
                headers: {"X-CSRFtoken": $.cookie("csrftoken")},
                success: function (data) {
                    if(data==="0"){
                        alert("添加失败")
                    }else{
                        showIpAuth(data)
                        new bootstrap.Toast(document.querySelector("#addOK")).show();
                    }

                }
            })
        })
    });

    //删除选中的IP授权信息
    //删除选中的授权资产
    $("#deleteSelectAuthIPBtn").off("click").on('click', function () {
        const chk_value_ip = [];
        const myModal = new bootstrap.Modal(document.getElementById('deleteSelectAuthIP'))

        $('#showIpItems input[type=checkbox]:checked').each(function () {
            chk_value_ip.push($(this).parents('tr').attr('id'))
        });
        // console.log(chk_value_properties.length === 0 ? '未选中任何' : chk_value_properties)
        if (chk_value_ip.length === 0) {
            alert("未选中任何")
        } else {
            myModal.show()
        }
        //删除所有选中的item
        $("#affirm_deleteSelectAuthIP").click(function () {
            $.ajax({
                url: "/AM/delete_selectAll_IP/",
                type: "POST",
                data: {
                    'chk_id': JSON.stringify(chk_value_ip)
                },
                dataType: "text",
                headers: {"X-CSRFtoken": $.cookie("csrftoken")},
                success: function (data) {
                    //将ajax的缓存数据取出显示
                    if(data==="数据删除失败"){
                        alert("数据删除失败")
                    }else{
                        showIpAuth(data)
                        new bootstrap.Toast(document.querySelector("#deleteOK")).show();
                    }
                },
                error: function () {
                    alert("删除所选失败");
                }
            })
        });

    })


    //修改ip授权信息
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

    //监听IP修改按钮活动
    //修改ip授权
    $(document).on('click', '.modifyAuthIPBTN', function () {
        const siblings = $(this).parents('tr').children(); // 获取所有兄弟结点
        $("#IPid").val($(this).parents('tr').attr('id'))
        $("#M_modify_auth_ip").val(siblings[3].innerHTML)
        $("#M_modify_create_time").val(siblings[4].innerHTML)
        $("#M_modify_auth_start_time").val(stringToDate(siblings[5].innerHTML))
        $("#M_modify_auth_end_time").val(stringToDate(siblings[6].innerHTML))
        if (siblings[7].innerHTML === 'True') {
            $("#m_authLogin_yes").prop('checked', true);
        } else {
            $("#m_authLogin_no").prop('checked', true);
        }

        $("#affirm_modifyIp").off('click').on('click', function () {
            const form = $("#modifyIpForm")
            $.ajax({
                url: '/AM/modify_auth_IP/',
                data: form.serialize(),
                type: 'POST',
                // dataType: "json",
                headers: {"X-CSRFtoken": $.cookie("csrftoken")},
                success: function (data){
                    if(data==="授权ip修改失败"){
                        alert("授权ip修改失败")
                    }else{
                        showIpAuth(data)
                        new bootstrap.Toast(document.querySelector("#editOK")).show();
                    }

                }
            })
        });
    });


    // 删除一条ip
    $(document).on('click', '.deleteAuthIPBTN', function () {
        const will_IP_id = $(this).parents('tr').attr('id');
        $('#affirm_deleteIp').off('click').on('click', function () {
            $.ajax({
                url: '/AM/delete_auth_ip/',
                data: {will_IP_id: will_IP_id},
                type: 'POST',
                dataType: "text",
                headers: {"X-CSRFtoken": $.cookie("csrftoken")},
                success: function (data){
                    if(data==='删除失败'){
                        console.log("删除失败")
                    }else {
                        showIpAuth(data)
                        new bootstrap.Toast(document.querySelector("#deleteOK")).show();
                    }
                }
            })
        });
    });
    /******************************ip授权信息 ************************/

    //切换显示的信息
    $('#exchange_auth_type').on('click', function () {
        $("#propertyAuthInfo").attr('class', 'visually-hidden')
        $("#loginAuthInfo").attr('class', 'visible')
    })

    $("#exchange").on('click', function () {
        const notionObj = $(".exchange_notions");

        if (notionObj.text() === '切换至资产授权管理') {
            $("#loginAuthInfo").prop('hidden', 'hidden')
            $("#propertyAuthInfo").removeAttr('hidden')
            notionObj.text("切换至登录授权管理")
        } else {
            $("#loginAuthInfo").removeAttr('hidden')
            $("#propertyAuthInfo").prop('hidden', 'hidden')
            notionObj.text("切换至资产授权管理")
        }

    });


})
