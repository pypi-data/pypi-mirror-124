<?php
/*LIBS*/
include_once __DIR__."/vendor/autoload.php";
require_once("php/db.php");
require_once("php/controller/controller.php");
?>
<!DOCTYPE HTML>
<html lang='<?=$lang;?>'>
<head>
    <?php include("php/modules/header.phtml");?>
</head>
<body>
<?php
    include_once "php/controller/index.php";
    include_once "php/modules/footer.phtml";
?>
</body>
</html>