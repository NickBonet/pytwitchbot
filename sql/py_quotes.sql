CREATE TABLE `py_quotes` (
    `qid` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `qchid` INTEGER NOT NULL,
    `qnick` TEXT NOT NULL,
    `qchan` TEXT NOT NULL,
    `qdate` TEXT NOT NULL,
    `quote` TEXT NOT NULL
)