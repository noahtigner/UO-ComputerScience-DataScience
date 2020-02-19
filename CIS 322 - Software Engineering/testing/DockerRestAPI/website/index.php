<html>
    <head>
        <title>CIS 322 REST-api demo: Laptop list</title>
    </head>

    <body>
        <h1>List of laptops</h1>
        <ul>
            <?php
            $json = file_get_contents('http://laptop-service:5000/');
            $obj = json_decode($json);
	          $laptops = $obj->Laptops;
            foreach ($laptops as $l) {
                echo "<li>$l</li>";
            }
            ?>
        </ul>
    </body>
</html>
