<?php 

require_once(__DIR__."/../vendor/autoload.php");

//	Routing configuration
$routing = include("./../config/routing.php");
$routerlith = new \Monolith\Routerlith\Routerlith($routing);

//	Find route and reach controller
$route      = $routerlith->getCurrentRoute();
$response   = $routerlith->dispatch($route, array());

echo $response;

exit();
