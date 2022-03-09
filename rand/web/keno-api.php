<?php 

class GridIsFullException extends \Exception {}
class NumberIsOutOfGridException extends \Exception {}
class NumberIsAlreadySelectedException extends \Exception {}

class KenoGrid
{
	protected static $availableCells = 70;
	protected static $playerSelectableCells = 10;
	protected static $gameSelectableCells = 20;

	protected $cells;

	public function __construct()
	{
		$this->cells = [];
	}

	public function addPlayerNumber(int $number):int
	{
		$this->addNumber($number);

		//	Does grid is full?
		$size = count($this->cells);
		if ($size >= self::$playerSelectableCells) {
			throw new GridIsFullException("Player's grid is already full");
		}

		$this->cells[] = $number;
		$size++;

		if ($size == self::$playerSelectableCells) {
			sort($this->cells);
		}

		return $size;
	}

	public function addGameNumber(int $number):int
	{
		$this->addNumber($number);

		//	Does grid is full?
		$size = count($this->cells);
		if ($size >= self::$gameSelectableCells) {
			throw new \GridIsFullException("Game's grid is already full");
		}

		$this->cells[] = $number;
		$size++;

		if ($size == self::$gameSelectableCells) {
			sort($this->cells);
		}

		return $size;
	}

	protected function addNumber(int $number):void
	{
		//	Out of range?
		if ($number < 1 || $number > self::$availableCells) {
			throw new NumberIsOutOfGridException("Grid doesn't have this number");
		}

		//	Already selected?
		if (in_array($number, $this->cells)) {
			throw new NumberIsAlreadySelectedException("Number is already in grid");
		}
	}

	public function getCells()
	{
		return $this->cells;
	}

	public function __toString()
	{
		$toDisplay = "";

		foreach ($this->cells as $key => $value) {
			$toDisplay .= "<tr><td>".$key."</td><td class='number'>".$value."</td></tr>";
		}

		$toDisplay = "<table><thead><tr><th>ID</th><th>Number</th></tr></thead><tbody>".$toDisplay."</tbody></table>";

		return $toDisplay;
	}
}

class KenoGame
{
	public static function randomInteger(int $min, int $max):int
	{
		for ($i=0; $i<10; $i++) {
			random_int($min, $max);
		}

		return random_int($min, $max);
	}

	public static function result(KenoGrid $playerGrid, KenoGrid $gameGrid)
	{
		$foundNumbers = 0;
		$numberUnion = [];

		$playerCells = $playerGrid->getCells();
		$gameCells = $gameGrid->getCells();

		foreach ($playerCells as $playerNumber) {
			if (in_array($playerNumber, $gameCells)) {
				$foundNumbers++;
				$numberUnion[] = $playerNumber;
			}
		}

		sort($numberUnion);

		return [$foundNumbers, $numberUnion];
	}

	public static function fillPlayerGrid()
	{
		$grid = new KenoGrid();

		$continueSelection = true;
		while ($continueSelection) {
			try {
				$rand = self::randomInteger(1, 70);
				$size = $grid->addPlayerNumber($rand);
				if ($size == 10) {
					break;
				}
			}
			catch (NumberIsAlreadySelectedException $e) {

			}
		}

		return $grid;
	}

	public static function fillGameGrid()
	{
		$grid = new KenoGrid();

		$continueSelection = true;
		while ($continueSelection) {
			try {
				$rand = self::randomInteger(1, 70);
				$size = $grid->addGameNumber($rand);
				if ($size == 20) {
					break;
				}
			}
			catch (NumberIsAlreadySelectedException $e) {

			}
		}

		return $grid;
	}
}

$count = 0;
$conditionToContinue = true;
while ($conditionToContinue) {
	$count++;
	$gameGrid = KenoGame::fillGameGrid();
	$playerGrid = KenoGame::fillPlayerGrid();

	list($foundNumbers, $numberUnion) = KenoGame::result($playerGrid, $gameGrid);
	if ($foundNumbers >= 10) {
		$conditionToContinue = false;

		$result  = "<p>Found: ".$foundNumbers."</p>";
		$result .= "<p>Attempts: ".$count."</p>";
		$result .= "<div id='playerGrid'>".$playerGrid."</div><br>";
		$result .= "<div id='gameGrid'>".$gameGrid."</div><br>";
		$result .= "<div id='union'>".implode(", ", $numberUnion)."</div>";
	}
}

?><!DOCTYPE html>
<html>
<head>

	<style>

table {
	width: 200px;
	border: 1px solid #333;
	border-collapse: collapse;
}

tr, td, th {
	border: 1px solid #333;
}

	</style>

</head>
<body>

	<?php echo $result; ?>

</body>
</html>