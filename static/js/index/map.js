$(document).ready(function () {
    /***********************************  地图实例  *****************************************************/
    window._AMapSecurityConfig = {
        serviceHost: 'http://http://127.0.0.1:8000/_AMapService',
        // 例如 ：serviceHost:'http://1.1.1.1:80/_AMapService',
    }

    const world = new AMap.DistrictLayer.World({
        zIndex: 10,
        depth: 2,
        opacity: 1,
        styles: {
            'nation-stroke': '#3d3c3c',
            'city-stroke': '#f80b0b',
        }

    })

    const map = new AMap.Map('mapInfo', {
        zooms: [3, 10],
        showIndoorMap: false,
        zoom: 3,
        isHotspot: false,
        defaultCursor: 'pointer',
        touchZoomCenter: 1,
        pitch: 0,
        layers: [
            world,
        ],
        viewMode: '3D',
        resizeEnable: true,
    });

    const nationFill = 'rgba(20, 120, 230, 0.3)';
    map.on('click', function (ev) {
        const px = ev.pixel;
        // 拾取所在位置的行政区
        const props = world.getDistrictByContainerPos(px);
        if (props) {
            const SOC = props.SOC;
            if (SOC) {
                // 重置行政区样式
                world.setStyles({
                    'fill': function (props) {
                        return props.SOC === SOC ? nationFill : 'white';
                    }
                });
            }
        }
    })

    // 获取经纬度

    function getXYbyIP() {
        const url = "https://api.map.baidu.com/location/ip?ak=HQi0eHpVOLlRuIFlsTZNGlYvqLO56un3&coor=bd09ll";
        $.ajax({
            url: url,
            type: 'POST',
            dataType: 'JSONP',
            async: false,
            cache: true,
            success: function (data) {
                // console.log(data)
                let location = data.content.address
                let latitude = Number(data.content.point.x);
                let longitude = Number(data.content.point.y);
                //添加地图标记
                // 并添加信息窗口
                const marker = new AMap.Marker({
                    position: new AMap.LngLat(latitude, longitude),
                });

                const infoWindow = new AMap.InfoWindow({ //创建信息窗体
                    isCustom: true,  //使用自定义窗体
                    content: '<div>登录地点：[' + latitude + ',' + longitude + ']</div>' + '<div class="text-center">' + location + '</div>', //信息窗体的内容可以是任意html片段
                    offset: new AMap.Pixel(16, -45)
                });
                const onMarkerClick = function (e) {
                    const px = e.pixel;
                    // 拾取所在位置的行政区
                    const props = world.getDistrictByContainerPos(px);
                    if (props) {
                        const SOC = props.SOC;
                        if (SOC) {
                            // 重置行政区样式
                            world.setStyles({
                                'fill': function (props) {
                                    return props.SOC === SOC ? nationFill : 'white';
                                }
                            });
                        }
                    }

                    infoWindow.open(map, e.target.getPosition());//打开信息窗体
                    //e.target就是被点击的Marker
                };
                map.add(marker);
                marker.on('click', onMarkerClick);//绑定click事件
            },
            error: function (data) {
            }
        });
    }

    getXYbyIP();


})