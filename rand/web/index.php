<?php 

require_once(__DIR__."/../vendor/autoload.php");

//	Database access
$config = include("./../config/database.php");
$casterlithService = new \MerryGoblin\Keno\Services\CasterlithService($config);

//	Routing configuration
$routing = include("./../config/routing.php");
$routerlith = new \Monolith\Routerlith\Routerlith($routing);

//	Libraries to inject in Controller's constructor method
$dependancies = [
	$casterlithService,
];

//	Find route and reach controller
$route      = $routerlith->getCurrentRoute();
$response   = $routerlith->dispatch($route, $dependancies);

echo $response;

exit();
