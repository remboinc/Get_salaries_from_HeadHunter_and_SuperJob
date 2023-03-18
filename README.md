# Find out your future salary
****
### Description
The script get information on programmer vacancies from 
HeadHunter and SuperJob sites for 7 popular programming languages. And finds the average salary for the selected programming languages.

Code Run Example:

```
+SuperJob Moscow--------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| Python                | 79               | 8                   | 139425           |
| JavaScript            | 81               | 9                   | 137457           |
| Java                  | 77               | 8                   | 143280           |
| Ruby                  | 79               | 8                   | 141133           |
| PHP                   | 79               | 8                   | 141133           |
| C++                   | 79               | 8                   | 141825           |
| C#                    | 82               | 9                   | 138289           |
+-----------------------+------------------+---------------------+------------------+
+hh.ru Moscow-----------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| Python                | 5094             | 454                 | 198423           |
| JavaScript            | 3090             | 725                 | 173515           |
| Java                  | 2956             | 318                 | 217870           |
| Ruby                  | 178              | 30                  | 202208           |
| PHP                   | 1384             | 560                 | 167588           |
| C++                   | 1531             | 429                 | 185176           |
| C#                    | 1207             | 284                 | 178823           |
+-----------------------+------------------+---------------------+------------------+

Process finished with exit code 0
```
### How to use
Clone the repository.
```
git clone https://github.com/remboinc/Get_salaries_from_HeadHunter_and_SuperJob
```
### Installation and launch
- Create a virtual environment on directory project:
```
python3.10 -m venv env
```
Start virtual environment:
```
.env/bin/activate
```
- Install dependencies from requirements.txt file.
```
pip install -r requirements.txt
```

- generate SECRET_KEY for SuperJob(https://api.superjob.ru).
-  Add the ".env" file to the project folder and enter the following data:
```
SJ_SECRET_KEY='we get the secret key when registering'
```
-  script launch:
```
python main.py
```
