$(document).ready(function () {
    /*
    获取用户ip和与位置信息
     */
    const ip = returnCitySN["cip"]
    let location;
    // 获取具体的地理位置信息
    $('#login').click(function () {
        const username = $("#floatingInput").val()
        const password = $("#floatingPassword").val()
        // 获取位置信息
        $.ajax({
            url: 'http://api.map.baidu.com/location/ip?ak=ia6HfFL660Bvh43exmH9LrI6',
            type: 'POST',
            dataType: 'jsonp',
            success: function (data) {
                location = data.content.address_detail.province + "," + data.content.address_detail.city
                $('#city').html(location)
                $('.location').html(location)

                login(username, password, ip, location)
            }
        })
        //登录提交认证功能
        function login(username, pwd, ip, location) {
            $.ajax({
                url: '/lg/loginAUTH/',
                type: 'POST',
                data: {
                    username: username,
                    pwd: pwd,
                    ip: ip,
                    location: location,
                },
                dataType: 'text',
                // headers: {"X-CSRFtoken": $.cookie("csrftoken")},
                success: function (data) {
                    if (data === 'false') {
                        window.location.href = '/lg/login/'
                        alert(data)
                    } else if (data === 'ok') {
                        // judge_email()
                        window.location.href = '/index'
                    } else if (data === '未被授权的登录IP地址' || data === "授权登录时间已过,继续登录请验证邮箱") {
                        alert('未被授权登录的ip地址, 请验证验证码')
                        verify_email()
                    } else if (data === "登录失败次数大于5次") {
                        alert('登录失败次数大于5次, 禁止登陆, 请明天登录或者重置密码。')
                    } else {
                        alert(data)
                    }
                }
            })
        }
    });


    /*$("#login").click(function () {
        const username = $("#floatingInput").val();
        const pwd = $("#floatingPassword").val();

    })*/

    //检测到未被授权的ip和已经过期的ip授权信息
    function verify_email() {
        const myModal = new bootstrap.Modal(document.getElementById('verify_self'));
        myModal.show()
    }


    //验证验证码
    $("#verifyEmailCode").click(function () {
        const username = $("#floatingInput").val();
        const authCode = $("#authCode").val();
        const email = $("#myEmail").val();
        $.ajax({
            url: '/lg/verifyAuthCode/',
            type: 'POST',
            data: {
                username: username,
                authCode: authCode,
                ip: ip,
                location: location,
                email: email,
            },
            dataType: 'text',
            headers: {"X-CSRFtoken": $.cookie("csrftoken")},
            success: function (data) {
                console.log(data)
                if (data === '验证码验证成功') {
                    // 邮箱完整
                    // judge_email()
                    window.location.href = '/index'
                } else if (data === '验证码验证失败') {
                    alert('验证码验证失败')
                }
            }

        })
    });

    //获取邮件验证码
    $("#getAuthCodeBtn").off('click').on("click", function () {
        const username = $("#floatingInput").val();
        const email = $("#myEmail").val();
        $.ajax({
            url: "/lg/sendMessage/loginVerify/",
            type: "POST",
            data: {
                username: username,
                email: email,
            },
            dataType: "text",
            headers: {"X-CSRFtoken": $.cookie("csrftoken")},
            success: function (data) {
                if (data === '验证码发送成功') {
                    alert('验证码获取成功')
                } else {
                    alert("验证码发送失败")
                }

            },
        });
    });

    //判断用户是否完善邮箱信息
    /*function judge_email(){
        $.ajax({
            url:'/lg/judge_userInfo_integrity/',
            type: "POST",
            headers: {"X-CSRFtoken": $.cookie("csrftoken")},
        })
    }*/
})