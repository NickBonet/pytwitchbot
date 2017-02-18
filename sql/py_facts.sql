CREATE TABLE `py_facts` (
    `factname` TEXT NOT NULL UNIQUE,
    `factauthor` TEXT NOT NULL,
    `factlock` INTEGER NOT NULL,
    `date` TEXT NOT NULL,
    `channel` TEXT NOT NULL,
    `fact` TEXT NOT NULL
)