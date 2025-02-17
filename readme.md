Проект телеграм бота по поиску отелей.

Запуск бота:
Для запуска бота необходимо:
1. В корне проекта создать файл с названием ".env" и ввести ваши ключи для телеграмм бота и для API сайта.
2. Запустить исполнительный файл main.py

Работа с ТГ-ботом:
1. Бот в неактивном состоянии не реагирует ни на какие команды кроме /start. Для начала работы необходимо ввести 
   команду /start.
2. При вводе команды /start пользователь попадает в главное меню, где ему предлагается выбрать следующую команду из:
    /low_price
    /high_price
    /best_deal
    /user_settings
    /history 
    2.1 /low_price - Команда для поиска отеля с самыми дешевыми ценами. При вводе команды начинается опрос 
пользователя об интересующем городе, количестве отелей и количестве фотографий отеля для вывода результата. В 
   результате пользователь получает результат в виде информации об отеле и фотографий отеля.
    2.2 /high_price - Команда для поиска отеля с самыми дорогими ценами. Команда отличается от /low_price только 
   поиском самых дорогих отелей.
    2.3 /best_deal - Команда для поиска отелей с настройками по ценовому диапазону и удаленности от центра города. 
   Пользователю дополнительно предлагается ввести ценовой диапазон в $ и диапазон удаленности отеля от центра города 
   в км.
    2.4 /user_settings - Команда для настройки поиска отелей по количеству человек, дате заселения и количеству 
   ночей. По умолчанию при старте бота будут настройки для одного человека, с датой заселения следующим днем за 
   текущей датой и количестве ночей равном одному. При вызове команды пользователю предлагается опрос с вводом этой 
   информации. После окончания опроса пользователь попадает в главное меню.
    2.5 /history - Команда для просмотра истории поиска. При вызове команды пользователю будут показаны его последние 
   десять запросов, которые пронумерованы. Для просмотра результат пользователю предлагается ввести номер запроса. 
   При корректном вводе будет показаны результат запроса.
3. При вводе города в диалогах /low_price, /high_price, /best_deal имя города не должно содержать специальных 
   символов. Если имя корректное, то программа обращается к API для поиска имени города. В результате опроса API 
   формируется результат из пронумерованного списка городов, пользователю предложат ввести номер города, если список 
   содержит только один город то выберется этот город. В случае не удачи пользователю предложат ввести другой город.
4. После окончания опроса будет произведен поиск отелей. В случае если поиск закончился успехом пользователю выдаст 
   результат и в БД запишется время, ID пользователя от ТГ-бота, Запрос в виде расшифрованного текса и ответ в виде 
   JSON словаря. В случае неудачи опроса API сформируется запись в файле error.log пользователю придет сообщение о 
   неудачном опросе.
5. В конце пользователь попадает в состояние где ему предложат вернутся в главное меню или воспользоваться командой 
   /back
6. /back - Команда для возврата в предыдущее состояние опроса.
7. Для остановки бота необходимо ввести команду /stop. После остановки настройки /user_setting исчезают.
8. some_data.db - БД хранящаяся историю поиска от пользователей. Представляет собой одну таблицу с полями id, time, 
   user_id, request, response.


