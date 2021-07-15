
jQuery(document).ready(function() {
    //tables
    var totalDonationList = jQuery("#total_donation");
    var streamerDonation = jQuery("#streamer_donation");
    var streamerFollower = jQuery("#streamer_follower");
    var streamerViews = jQuery("#streamer_views");

    //use sockjs
    var socket = new SockJS('/stomp');
    var stompClient = Stomp.over(socket);

    stompClient.connect({ }, function(frame) {
        //subscribe "/topic/realTimeAnalyticsData" message
        stompClient.subscribe("/topic/realTimeAnalyticsData", function(data) {
            var resp = jQuery.parseJSON(data.body);

            //Total Donation
            var totalOutput='';
            jQuery.each(resp.donations, function(i,d) {
                 totalOutput +="<tbody><tr><td>"+ d.hourOfTheDay+"</td><td>"+d.dayOfTheWeek+"</td><td>"+d.country+"</td><td>"+d.totalDonations+"</td></tr></tbody>";
            });
            
            var t_tabl_start = "<table class='table table-bordered table-condensed table-hover innerTable'><thead><th>hourOfTheDay</th><th>dayOfTheWeek</th><th>country</th><th>totalDonations</th></thead>";
            var t_tabl_end = "</table>";
            
            totalDonationList.html(t_tabl_start+totalOutput+t_tabl_end);
            
            var totalOutput='';
            jQuery.each(resp.streamerDonations, function(i,d) {
                 totalOutput +="<tbody><tr><td>"+ d.streamerID+"</td><td>"+d.year+"</td><td>"+d.month+"</td><td>"+d.totalDonations+"</td></tr></tbody>";
            });
            
            var t_tabl_start = "<table class='table table-bordered table-condensed table-hover innerTable'><thead><th>streamerID</th><th>year</th><th>month</th><th>totalDonations</th></thead>";
            var t_tabl_end = "</table>";
            
            streamerDonation.html(t_tabl_start+totalOutput+t_tabl_end);
            
            var totalOutput='';
            jQuery.each(resp.streamerFollower, function(i,d) {
                 totalOutput +="<tbody><tr><td>"+ d.streamerID+"</td><td>"+d.dayOfTheWeek+"</td><td>"+d.avgFollowersAdded+"</td></tr></tbody>";
            });
            
            var t_tabl_start = "<table class='table table-bordered table-condensed table-hover innerTable'><thead><th>streamerID</th><th>dayOfTheWeek</th><th>avgFollowersAdded</th></thead>";
            var t_tabl_end = "</table>";
            
            streamerFollower.html(t_tabl_start+totalOutput+t_tabl_end);
            
            var totalOutput='';
            jQuery.each(resp.streamerView, function(i,d) {
                 totalOutput +="<tbody><tr><td>"+ d.streamerID+"</td><td>"+d.hourOfTheDay+"</td><td>"+d.avgViews+"</td></tr></tbody>";
            });
            
            var t_tabl_start = "<table class='table table-bordered table-condensed table-hover innerTable'><thead><th>streamerID</th><th>hourOfTheDay</th><th>avgViews</th></thead>";
            var t_tabl_end = "</table>";
            
            streamerViews.html(t_tabl_start+totalOutput+t_tabl_end);
        });
    });
});

