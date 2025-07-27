1. Go the the 'SQL for DB' file and execute two sql files in 'MySQL Sever'
2. in the 'Backend/.env' file update MySQL server user_name and password
3. pip install all the dependencies for Backend using cmd: `pip install -r requirements.txt` in ('Backend/')
4. run cmd: `python -m uvicorn Backend.main:app --reload --reload-dir Backend`  (outside '/Backend')
5. app is running in browser
6. got to running_usl/docs (navigate to '/docs')
7. use auth/login endpoint to login
8. password for all the users is same: `Paves@123`
9. Added comments to check pull request
