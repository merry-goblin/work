<?php

namespace MerryGoblin\Keno\Models\Composers;

use MerryGoblin\Keno\Models\Entities\Game as GameEntity;

use Monolith\Casterlith\Composer\ComposerInterface;
use Monolith\Casterlith\Composer\AbstractComposer;

class Game extends AbstractComposer implements ComposerInterface
{
	protected static $mapperName  = 'MerryGoblin\\Keno\\Models\\Mappers\\Game';
}
