<html>
<script>
         function loadMap() {
      
            var mapOptions = {
               center:new google.maps.LatLng(11.8745, 75.3704), 
               zoom:12, 
               mapTypeId:google.maps.MapTypeId.ROADMAP
            };
        
            var map = new google.maps.Map(document.getElementById("sample"),mapOptions);
         }
      
         google.maps.event.addDomListener(window, 'load', loadMap);
      </script></html>