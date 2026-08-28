## ER-диаграмма
![Диаграмма сущностей](https://github.com/MMoreon/Billing/blob/main/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202026-08-28%20222159.png)

тут Payment.transaction_id Invoice.merchant_invoice_id были созданы для идемпотентности 
к примеру пришел коллбек но что то пошло не так и сервер вернул ошибку, при повторении колбека будет тот же Payment.transaction_id по нему будет понятно внешний платеж обработан
так же с Invoice.merchant_invoice_id ,если запрос повторится второй запрос должен вернуть существующий Invoice а не создать второй