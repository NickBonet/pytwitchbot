CREATE TABLE `py_users` (
    `nick` TEXT NOT NULL UNIQUE,
    `ident` TEXT NOT NULL,
    `host` TEXT NOT NULL,
    `passphrase` TEXT NOT NULL,
    `level` INTEGER NOT NULL
)