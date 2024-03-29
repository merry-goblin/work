<?php

namespace MerryGoblin\Keno\Models\Composers;

use MerryGoblin\Keno\Models\Entities\Grid as GridEntity;
use MerryGoblin\Keno\Models\Entities\Game as GameEntity;

use Monolith\Casterlith\Composer\ComposerInterface;
use Monolith\Casterlith\Composer\AbstractComposer;

class Grid extends AbstractComposer implements ComposerInterface
{
	protected static $mapperName  = 'MerryGoblin\\Keno\\Models\\Mappers\\Grid';

	CONST GRID_TO_PROCESS_STATUS  = 1;
	CONST GRID_PROCESSED_STATUS   = 2;

	public function insertGrid(GameEntity $game, $selectedCells)
	{
		$dbal = $this->getDBALConnection();

		$sql = "
			INSERT INTO grid
				(`id`, `cells`, `gameId`, `status`, `nbFound`)
			VALUES 
				(:id , :cells , :gameId,  :status , :nbFound )
		";
		$values = array(
			'id'      => null,
			'cells'   => $selectedCells,
			'gameId'  => $game->id,
			'status'  => self::GRID_TO_PROCESS_STATUS,
			'nbFound' => null,
		);
		$dbal->executeUpdate($sql, $values);
	}

	public function getGridsToProcess(GameEntity $game, $max)
	{
		$grids = $this
			->select('grid')
			->where($this->expr()->andX(
				$this->expr()->eq('grid.gameId', ':gameId'),
				$this->expr()->eq('grid.status', ':status')
			))
			->setParameter('gameId', $game->id)
			->setParameter('status', self::GRID_TO_PROCESS_STATUS)
			->limit(0, $max)
		;

		return $grids;
	}

	public function getNumberOfGridsToProcess(GameEntity $game)
	{
		$row = $this
			->selectAsRaw("grid", "count(grid.id) as nb")
			->where($this->expr()->andX(
				$this->expr()->eq('grid.gameId', ':gameId'),
				$this->expr()->eq('grid.status', ':status')
			))
			->setParameter('gameId', $game->id)
			->setParameter('status', self::GRID_TO_PROCESS_STATUS)
			->first()
		;

		return $row['nb'];
	}

	/**
	 * @param  MerryGoblin\Keno\Models\Entities\Grid $grid
	 * @return null
	 */
	public function updateAfterDrawProcess($grid)
	{
		$dbal = $this->getDBALConnection();

		$sql = "
			UPDATE grid
			SET   
				status = :status,
				nbFound = :nbFound
			WHERE id = :id
		";
		$values = array(
			'status'  => $grid->status,
			'nbFound' => $grid->nbFound,
			'id'      => $grid->id,
		);
		$dbal->executeUpdate($sql, $values);
	}
}
