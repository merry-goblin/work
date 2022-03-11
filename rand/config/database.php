<?php

$database = array(
	'keno' => [
		'driver'  => 'pdo_sqlite',
		'path'    => __DIR__."/keno.db",
		'memory'  => false,
	],
);

return $database;
