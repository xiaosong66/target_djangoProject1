$(document).ready(function(){
    /*
        刷新数据库的内容，并显示到主页
     */
    function showItems(data, showId) {
        //将ajax的缓存数据取出显示
        const parser = new DOMParser();
        const htmlData = parser.parseFromString(data, 'text/html');
        const obj = htmlData.getElementById(showId).innerHTML;
        $("#"+ showId).html(obj);
    }

    // 请求登录锁定信息
    /*$.ajax({
        url: "/RW/get_loginFailure_info/",
        type: 'POST',
        dataType: 'text',
        contentType: 'text/html',
        headers: {"X-CSRFtoken": $.cookie("csrftoken")},
        success: function (data) {
            //将ajax的缓存数据取出显示
            // showItems(data);
            // console.log("登录信息获取完毕")
        },
    })*/

    // 获取密码强度信息
    $.ajax({
        url: "/RW/getPdStrengthSecurityInfo/",
        type: 'POST',
        dataType: 'text',
        contentType: 'text/html',
        headers: {"X-CSRFtoken": $.cookie("csrftoken")},
        success: function (data) {
            showItems(data, 'pdSecurity');
            showItems(data, 'allRisk_pd');
            console.log("密码信息获取完毕")
        },
    })

    // 获取资产安全信息
    $.ajax({
        url: "/RW/getPropertySecurityInfo/",
        type: 'POST',
        dataType: 'text',
        contentType: 'text/html',
        headers: {"X-CSRFtoken": $.cookie("csrftoken")},
        success: function (data) {
            showItems(data, 'propertySecurity');
            showItems(data, 'allRisk_property');
            console.log("资产安全信息获取完毕")
        },
    })

    // 获取账户安全信息
    $.ajax({
        url: "/RW/getAccountSecurityInfo/",
        type: 'POST',
        dataType: 'text',
        contentType: 'text/html',
        headers: {"X-CSRFtoken": $.cookie("csrftoken")},
        success: function (data) {
            showItems(data, 'accountSecurity');
            showItems(data, 'allRisk_account');
            console.log("账户安全信息获取完毕")
        },
    })

    // 获取行为安全信息
    $.ajax({
        url: "/RW/getActionSecurityInfo/",
        type: 'POST',
        dataType: 'text',
        contentType: 'text/html',
        headers: {"X-CSRFtoken": $.cookie("csrftoken")},
        success: function (data) {
            showItems(data, 'actionSecurity');
            showItems(data, 'allRisk_action');
            console.log("行为安全信息获取完毕")
        },
    })

    // 获取其他安全信息
    $.ajax({
        url: "/RW/getOtherSecurityInfo/",
        type: 'POST',
        dataType: 'text',
        contentType: 'text/html',
        headers: {"X-CSRFtoken": $.cookie("csrftoken")},
        success: function (data) {
            showItems(data, 'otherSecurity');
            showItems(data, 'allRisk_other');
            console.log("其他安全信息获取完毕")
        },
    })


})