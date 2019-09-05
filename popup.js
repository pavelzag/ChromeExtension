$(document).ready(function() {
   $("button").click(function() {
       var xhr = new XMLHttpRequest();
       var url = "http://localhost:8081/trigger_jenkins_job";
       var selectedCity = $('#city').val();
       xhr.open("POST", url, true);
       xhr.setRequestHeader("Content-Type", "application/json");
       xhr.onreadystatechange = function() {
           if (xhr.readyState === 4 && xhr.status === 200) {
               var json = JSON.parse(xhr.responseText);
           }
       };
       var data = JSON.stringify({
           "city_name": selectedCity
       });
       xhr.send(data);
   });
});
