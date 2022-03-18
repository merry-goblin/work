
CREATE TABLE "game" (
	"id"     INTEGER,
	"cells"  VARCHAR(255),
	"active" INTEGER DEFAULT 1,
	"status" INTEGER DEFAULT 1,
	PRIMARY KEY("id")
);

CREATE TABLE "grid" (
	"id"      INTEGER PRIMARY KEY AUTOINCREMENT,
	"cells"   TEXT,
	"gameId"  INTEGER,
	"status"  INTEGER,
	"nbFound" INTEGER
);

CREATE TABLE "game_statistics" (
	"id"      INTEGER PRIMARY KEY AUTOINCREMENT,
	"gameId"  INTEGER,
	"nbGrids" INTEGER
);

CREATE TABLE "found_on_game_statistics" (
	"id"               INTEGER PRIMARY KEY AUTOINCREMENT,
	"gameStatisticsId" INTEGER,
	"number"           INTEGER,
	"count"            INTEGER
);
