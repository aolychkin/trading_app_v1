# Инструкция по гиту
git add *
git commit -m "project base"
git branch -M main
git remote add origin https://github.com/aolychkin/trading_app_v1.git
git push -u origin main

# Экспортировать Path для импорта библиотек
export PYTHONPATH="${PYTHONPATH}:/Desktop/trading_app_v1/"