<html>

<head>
    <title>IoT Traffic Data Monitoring Dashboard</title>
    <link rel="styleshe/**



 var totalDonationData={
            labels : ["Vehicle"],
            datasets : [{
                label : "Route",
                data : [1]
            }
           ]
        };



jQuery(document).ready(function() {
    //Charts
    var ctx1 = document.getElementById("totalDonationChart").getContext("2d");
    window.tChart = new Chart(ctx1, {
                type: 'bar',
                data: totalDonationData
            });


    //tables
    var totalDonationList = jQuery("#total_donation");

    //use sockjs
    var socket = new SockJS('/stomp');
    var stompClient = Stomp.over(socket);

    stompClient.connect({ }, function(frame) {
        //subscribe "/topic/trafficData" message
        stompClient.subscribe("/topic/realTimeAnalyticsData", function(data) {
            var dataList = data.body;
            var resp=jQuery.parseJSON(dataList);

            //Total traffic
            var totalOutput='';
            jQuery.each(resp.totalTraffic, function(i,vh) {
                 totalOutput +="<tbody><tr><td>"+ vh.routeId+"</td><td>"+vh.vehicleType+"</td><td>"+vh.totalCount+"</td><td>"+vh.timeStamp+"</td></tr></tbody>";
            });
            var t_tabl_start = "<table class='table table-bordered table-condensed table-hover innerTable'><thead><tr><th>Route</th><th>Vehicle</th><th>Count</th><th>Time</th></tr></thead>";
            var t_tabl_end = "</table>";
            totalTrafficList.html(t_tabl_start+totalOutput+t_tabl_end);

            //draw total donation chart
            drawBarChart(resp.donation,totalDonationData);

        });
    });
});

function drawBarChart(trafficDetail,trafficChartData){
    //Prepare data for total traffic chart
    var chartLabel = [ "Bus","Large Truck",  "Private Car","Small Truck", "Taxi"];
    var routeName = ["Route-37", "Route-82", "Route-43"];
    var chartData0 =[0,0,0,0,0], chartData1 =[0,0,0,0,0], chartData2 =[0,0,0,0,0];

    jQuery.each(trafficDetail, function(i,vh) {

        if(vh.routeId == routeName[0]){
            chartData0.splice(chartLabel.indexOf(vh.vehicleType),1,vh.totalCount);
        }
        if(vh.routeId == routeName[1]){
            chartData1.splice(chartLabel.indexOf(vh.vehicleType),1,vh.totalCount);
        }
        if(vh.routeId == routeName[2]){
            chartData2.splice(chartLabel.indexOf(vh.vehicleType),1,vh.totalCount);
        }
    });

    var trafficData = {
        labels : chartLabel,
        datasets : [{
            label				  : routeName[0],
            borderColor           : "#878BB6",
            backgroundColor       : "#878BB6",
            data                  : chartData0
        },
        {
            label				  : routeName[1],
            borderColor           : "#4ACAB4",
            backgroundColor       : "#4ACAB4",
            data                  : chartData1
        },
        {
            label				  : routeName[2],
            borderColor           : "#FFEA88",
            backgroundColor       : "#FFEA88",
            data                  : chartData2
        }

        ]
    };
      //update chart
      trafficChartData.datasets=trafficData.datasets;
      trafficChartData.labels=trafficData.labels;
 }


 function getRandomColor() {
    return  'rgba(' + Math.round(Math.random() * 255) + ',' + Math.round(Math.random() * 255) + ',' + Math.round(Math.random() * 255) + ',' + ('1') + ')';
};