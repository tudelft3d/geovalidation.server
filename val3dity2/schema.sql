drop table if exists tasks;
create table tasks (
  `jid` TEXT NOT NULL,
  `file`  TEXT NOT NULL,
  `primitives`  TEXT NOT NULL,
  `snaptol` REAL NOT NULL,
  `plantol` REAL NOT NULL,
  `timestamp`  TEXT NOT NULL,
  `noprimitives`  INTEGER,
  `noinvalid`  INTEGER,
  `errors`  TEXT,
  `ip`  TEXT,
  `usebuildings`  INTEGER,
  `nobuildings`  INTEGER,
  `invalidbuildings`  INTEGER,
  PRIMARY KEY(jid)
);