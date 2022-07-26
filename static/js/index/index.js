$(document).ready(function () {
    /********   资产授权信息 ****************** */
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

    //异步请求资产授权信息
    $.ajax({
        url: '/AM/get_propertyAuth_info/',
        type: 'POST',
        data: {'tag': '0'},
        headers: {"X-CSRFtoken": $.cookie("csrftoken")},
        success: function (data) {
            showItems(data);
        },
    })



})