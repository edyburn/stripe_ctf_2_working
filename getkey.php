<?php
$path = $_GET['filename'];

if (is_file($path))
    echo file_get_contents($path);
else
    $contents = scandir($path);
    foreach ($contents as $item)
        echo $item . "\n";

?>
