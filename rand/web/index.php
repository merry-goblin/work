<?php 

require_once(__DIR__."/../vendor/autoload.php");

//	Routing configuration
$routing = include("./../config/routing.php");
$routerlith = new \Monolith\Routerlith\Routerlith($routing);

//	Libraries to inject in Controller's constructor method
$dependancies = [];

//	Find route and reach controller
$route      = $routerlith->getCurrentRoute();
$response   = $routerlith->dispatch($route, $dependancies);

echo $response;

exit();
