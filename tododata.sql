CREATE DATABASE taskdata;

DROP TABLE IF EXISTS タスク;
CREATE TABLE タスク (
    タスクID INTEGER PRIMARY KEY,
    タスク内容 TEXT NOT NULL,
    日時 DATE NOT NULL,
    ステータス TEXT NOT NULL
);

DROP TABLE IF EXISTS ユーザー;
CREATE TABLE ユーザー (
    ユーザーID TEXT PRIMARY KEY,
    名前 TEXT NOT NULL,
    パスワード TEXT NOT NULL
);

DROP TABLE IF EXISTS タスクデータ;
CREATE TABLE タスクデータ (
    タスクID INTEGER REFERENCES タスク(タスクID),
    ユーザーID TEXT REFERENCES ユーザー(ユーザーID)
);

INSERT INTO ユーザー (ユーザーID,名前,パスワード)
VALUES
    ('bunri01', '文理太郎', '20240120');