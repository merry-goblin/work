<?php 

namespace MerryGoblin\Keno\Controllers;

class AppController extends AbstractController
{
	public function getAction()
	{
		ob_start();
		readfile(__DIR__ ."/../Ressources/views/app.html"); // no PHP so readfile is enough
		$html = ob_get_contents();
		ob_end_clean();

		return $html;
	}
}
