@ECHO off
TITLE chrome debugging mode
PUSHD %~dp0
SET USER_DATA_DIR=%CD%\crawler_user_data
CD /d %1
chrome.exe --remote-debugging-port=%2 --user-data-dir=%USER_DATA_DIR%