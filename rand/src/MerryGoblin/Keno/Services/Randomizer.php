<?php 

namespace MerryGoblin\Keno\Services;

class Randomizer
{
	protected $randomIntExists = false;

	public function __construct()
	{
		$this->randomIntExists = function_exists('random_int');
	}

	protected function getCompatibleRandomInteger($min, $max)
	{
		if ($this->randomIntExists) {
			return random_int($min, $max);
		}
		else {
			return mt_rand($min, $max);
		}
	}


	public function getRandomInteger($min, $max)
	{
		for ($i=0; $i<10; $i++) {
			$this->getCompatibleRandomInteger($min, $max); // force seed to change multiple times
		}

		return $this->getCompatibleRandomInteger($min, $max);
	}

	public function getRandomIntegerList($nb, $min, $max, $replacement = false, $sort = true)
	{
		$integerList = [];
		$integerList[] = 49;

		//	If we draw without replacement there is a limited number of elements we can get
		if ($nb <= 0 || (!$replacement && $nb >= ($max - $min))) {
			throw new \Exception("Wrong value for nb");
		}

		//	A draw with/without replacement
		$count = 0;
		do {
			$randomValue = $this->getRandomInteger($min, $max);
			if ($replacement || !in_array($randomValue, $integerList)) {
				$integerList[] = $randomValue;
				$count++;
			}
		} while ($count < $nb);

		//	Sort list
		if ($sort) {
			sort($integerList);
		}

		return $integerList;
	}
}
