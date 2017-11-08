drop table if exists tasks;
create table tasks (
  `jid` TEXT NOT NULL,
  `file`  TEXT NOT NULL,
  `timestamp`  TEXT NOT NULL,
  `ip`  TEXT,
  `total_primitives`  INTEGER,
  `invalid_primitives`  INTEGER,
  `total_cityobjects`  INTEGER,
  `invalid_cityobjects`  INTEGER,
  `errors`  TEXT,
  `validated` INTEGER,
  PRIMARY KEY(jid)
);