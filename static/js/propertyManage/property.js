$(document).ready(function () {
    // 下拉菜单
    $(".dropdown-item").click(function () {
        $("#searchType").val($(this).text())
    })
    // 全选/全取消
    $("thead input[type=checkbox]").click(function () {
        $("tbody input[type=checkbox]").prop("checked", $(this).prop("checked"));
    })
    // 其他按钮 click只能静态绑定
    $(document).on('click', 'tbody input[type=checkbox]', function () {
        if ($("tbody input[type=checkbox]:checked").length === $("tbody input[type=checkbox]").length) {
            $("thead input[type=checkbox]").prop("checked", true);
        } else {
            $("thead input[type=checkbox]").prop("checked", false);
        }
    })

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


    // 选中的项目
    const chk_value = [];
    $("#deleteSelectBtn").on('click', function () {
        $('tbody input[type=checkbox]:checked').each(function () {
            chk_value.push($(this).parents('tr').attr('id'))
        });
        console.log(chk_value.length === 0 ? '未选中任何' : chk_value)
        //删除所有选中的item
        $("#deleteAll").click(function () {
            $.ajax({
                url: "/PM/deleteAll/",
                type: "POST",
                data: {
                    'chk_id': JSON.stringify(chk_value)
                },
                dataType: "text",
                headers: {"X-CSRFtoken": $.cookie("csrftoken")},
                success: function (data) {
                    //将ajax的缓存数据取出显示
                    showItems(data);
                    new bootstrap.Toast(document.querySelector("#deleteOK")).show();
                },
                error: function () {
                    console.log("删除所选失败");
                }
            });
        });
    });


    // 模态框 删除
    // 只删除单独一个
    $(document).off('click').on("click", '.delete', function () {
        const will_delete = $(this).parents('tr')
        const delete_id = will_delete.attr('id')
        $("#right").click(function () {
            // will_delete.remove();
            $.ajax({
                url: "/PM/deleteOne/",
                type: "POST",
                data: {'delete_id': delete_id},
                dataType: "text",
                // headers: {"X-CSRFtoken": $.cookie("csrftoken")},
                success: function (data) {
                    //将ajax的缓存数据取出显示
                    showItems(data);
                    new bootstrap.Toast(document.querySelector("#deleteOK")).show();
                    console.log("删除成功");
                },
                error: function () {
                    console.log("删除失败");
                }
            })
        })
    });

    //用Ajax传递参数
    //提交模态框中要添加的内容
    //let checkID = [];//定义一个空数组
    // $("select[name='if-encrypt']:selected").each(function (i) {//把所有被选中的复选框的值存入数组
    //   checkID[i] = $(this).val();
    //});
    // 添加时间


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

    $(".addTime").val(get_now_time());  // 显示修改时间和新添加时的时间
    // 检测是否设置了二次密码
    let secondPDState = Boolean(false);
    $("#addNew").click(function (){
        detect_secondPD();
        if(secondPDState){
            new bootstrap.Modal(document.getElementById('addData')).show()
        }
    })

    //添加新资产
    $('#right_add').off('click').on('click', function () {
        const formData = new FormData();
        const fileName = $("#fileName").val();
        const describe = $("#describe").val();
        const addTime = $("#addTime").val();
        const myFile = $("#formFile")[0].files[0];
        const if_backup = $('[name=if-backup]:checked').val();
        const if_encrypt = $('[name=if-encrypt]:checked').val();

        if ($("#formFile").val() === '' || $("#formFile").val() == null) {
            $("#add_file_notion").attr('class', 'visible')
        } else {
            const myModal = bootstrap.Modal.getInstance(document.getElementById('addData'));

            formData.append('addTime', addTime);
            formData.append('myFile', myFile);
            formData.append('if_backup', if_backup);
            formData.append('if_encrypt', if_encrypt);
            formData.append('describe', describe);
            formData.append('fileName', fileName);

            $.ajax({
                url: "/PM/add_data/",
                type: "POST",
                // data: {checkID: checkID},
                data: formData,
                dataType: 'text',  //服务器端返回数据类型，success函数执行会根据该类型判断返回的数据类型
                headers: {"X-CSRFtoken": $.cookie("csrftoken")},
                contentType: false,  // 告诉jQuery不要去设置Content-Type请求头
                processData: false,  // 告诉jQuery不要去处理发送的数据
                success: function (data) {
                    if (data === '文件已存在') {
                        alert("文件已存在,修改名之后重试!")
                    } else if(data=== '文件上传失败'){
                        alert("文件上传失败")
                    } else {
                        //将ajax的缓存数据取出显示
                        showItems(data);
                        new bootstrap.Toast(document.querySelector('#addOK')).show();  // 提醒添加成功
                        console.log('添加数据成功')
                        $("#add_file_notion").attr('class', 'visually-hidden')
                        myModal.hide();
                        //location.reload();
                    }
                },
            });
        }
    });

    //
    // 详情和编辑功能显示数据
    // 编辑按钮点击时，并显示  ajax提交数据
    $(document).on("click", ".edit, .detail", function () {
        const will_edit = $(this).parents('tr')
        const id = will_edit.attr('id')
        const obj = document.getElementById(id);  // tr标签所有内容
        const num = obj.children[1].innerHTML;  // 编号
        const type = obj.children[2].innerHTML;  // 文件类型
        const user = obj.children[3].innerHTML;  // 所属用户
        const create_time = obj.children[4].innerHTML;   //提取显示的内容
        const fileDescribe = obj.children[6].children[0].innerHTML;   //提取显示的内容
        const backup = obj.children[7].innerHTML;   //提取显示的内容
        const encrypt = obj.children[8].innerHTML;   //提取显示的内容
        $(".num").val(num)
        $(".type").val(type)
        $(".user").val(user)
        $(".editID").val(id)
        $(".createTime").val(create_time)
        $(".fileDescribe").val(fileDescribe)

        // 显示和隐藏共享按钮
        if (will_edit.is('.NoShare')) {
            $("#shareBtn").prop('hidden', 'true')
        }
        if (will_edit.is('.Share')) {
            $("#shareBtn").removeAttr('hidden')
        }
        /*
             这里用attr只是为元素添加了checked=“checked”的属性，但是并没有使checked的动作生效。
              ****利用prop是可以直接将属性生效的方法*****
         */
        if (backup === "True") {
            $("#backup_yes").prop("checked", true)
            $("#d_backup_yes").prop("checked", true)
        } else {
            $("#backup_no").prop("checked", true)
            $("#d_backup_no").prop("checked", true)
        }
        if (encrypt === "True") {
            $("#encrypt_yes").prop("checked", true)
            $("#d_encrypt_yes").prop("checked", true)
        } else {
            $("#encrypt_no").prop("checked", true)
            $("#d_encrypt_no").prop("checked", true)
        }
        /*后面修改提交的*/
        $("#rightEdit").off("click").on('click', function () {
            const editForm = $("#editForm");
            $.ajax({
                url: "/PM/editOne/",
                type: "POST",
                // data: {checkID: checkID},
                data: editForm.serialize(),
                dataType: 'text',  //服务器端返回数据类型，success函数执行会根据该类型判断返回的数据类型
                headers: {"X-CSRFtoken": $.cookie("csrftoken")},
                success: function (data) {
                    showItems(data);
                    new bootstrap.Toast(document.querySelector("#editOK")).show();
                    console.log('修改数据成功')
                },
            });
        });

        //添加共享资产按钮
        $("#affirm_addNewShare_Property").off('click').on('click', function () {
            const M_share_users = $("#M_share_users").val();
            const M_start_share_time = $("#M_start_share_time").val();
            const M_end_share_time = $("#M_end_share_time").val();

            $.ajax({
                url: "/AM/add_share_info/",
                type: "POST",
                data: {
                    id: id,
                    M_share_users: M_share_users,
                    M_start_share_time: M_start_share_time,
                    M_end_share_time: M_end_share_time,
                    fileDescribe: fileDescribe,
                },
                dataType: 'text',
                headers: {"X-CSRFtoken": $.cookie("csrftoken")},
                success: function (data) {
                    if (data === '共享文件成功') {
                        new bootstrap.Toast(document.querySelector("#shareOK")).show();
                    }
                }
            });
        });

        //下载文件
        $('#downloadFileBtn').off('click').on('click', function () {
            const form = $('<form action="/PM/downloadFile/" method="post"></form>')
            const input1 = $("<input type='hidden' name='id' />")
            input1.attr('value', id)
            form.append(input1)
            $('body').append(form);
            form.submit();
        })

    });

    // with对变量赋值
    //
    // 加载页面用户的所有数据
    //
    //jQuery.get("/static/other/items.html", function (item){
    //           console.log(item)  读取内容
    //               })
    /* 异步提交方式 获取所有数据 */
    $.ajax({
        cache: false,
        async: true,
        url: "/PM/get_all_data/",
        type: "POST",
        dataType: 'text',
        contentType: 'text/html',
        headers: {"X-CSRFtoken": $.cookie("csrftoken")},
        success: function (data) {
            //将ajax的缓存数据取出显示
            showItems(data);
            console.log("加载所有数据成功")
        },
        error: function () {
            console.log("请求用户所有数据失败")
        },
    });

    //搜索内容
    $("#searchBtn").on('click', function () {
        const form = $('#searchContentForm')
        $.ajax({
            url: "/PM/search_data/",
            data: form.serialize(),
            type: "POST",
            dataType: 'text',
            headers: {"X-CSRFtoken": $.cookie("csrftoken")},
            success: function (data) {
                //将ajax的缓存数据取出显示
                showItems(data);
            },
            error: function () {

            },
        })
    })

    function detect_secondPD() {
        $.post("/PM/judge_make_secondPD/", function (result) {
            if (result === "未设置二次密码") {
                // alert("未设置二次密码")
                const myModal = new bootstrap.Modal(document.getElementById('setSecondPD'))
                myModal.show()
                 secondPDState = false
            }else if(result === "已设置二次密码"){
                secondPDState = true
            }
        })
    }
    // 检测是否设置二次密码
    detect_secondPD();
    // 设置二次密码发送验证码
    $("#getCode").click(function () {
        const email = $("#email").val()
        console.log(email)
        $.post('/lg/sendMessage/secondPD/',{'myEmail': email}, function (data){
            if(data==='验证码发送成功'){
                alert("验证码发送成功")
            }
        })
    })
    $("#rightSetSecondPDBtn").click(function (){
        const myForm = $("#setSecondPDFrom")
        $.ajax({
            url: "/PM/setSecondPD/",
            data: myForm.serialize(),
            type: 'post',
            success: function (data){
                alert(data)
            }
        })
    })

    /*
    function download(url, fileName) {
        const xhr = new XMLHttpRequest();
        xhr.open('POST', url, true);     // 请求方式，看具体接口情况决定
        xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8'); // 内容类型，看具体接口情况决定
        xhr.withCredentials = true;
        xhr.responseType = "blob";  // 返回类型blob
        // 定义请求完成的处理函数，请求前也可以增加加载框/禁用下载按钮逻辑
        xhr.onload = function () {
            // 请求完成
            if (this.status === 200) {
                // 返回200
                const blob = this.response;
                const reader = new FileReader();
                reader.readAsDataURL(blob);  // 转换为base64，可以直接放入a>href
                reader.onload = function (e) {
                    // 转换完成，创建一个a标签用于下载
                    const a = document.createElement('a');
                    a.download = fileName;
                    a.href = e.target.result;
                    // $("body").append(a);  // 修复firefox中无法触发click
                    a.click();
                    // $(a).remove();
                }
            }
        };
        // 发送ajax请求
        // xhr.send(JSON.stringify(data)); // 数据格式，看具体接口情况决定
        xhr.send(); // 数据格式，看具体接口情况决定
    }
    */

})