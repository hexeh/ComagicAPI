# ComagicAPI
#### Простой класс для работы с API сервиса Comagic на языке Python

---

<p align="center">
<b><a href = "https://www.comagic.ru/support/api/comagic_api/">Документация по API Comagic</a></b>
</p>

---

## Использование

### Авторизация

Авторизация запросов к API Comagic происходит при помощи ключа сессии, получаемого в обмен на логин/пароль пользователя системы. Для каждой инициализации класса создаётся новая сессия. После завершения работы с API необходимо вызывать метод `endSession`, который завершает сессию в соответствии с документацией

### Список методов

В текущей реализации представлены методы:

-   **getClients**. [Описание](https://www.comagic.ru/support/api/comagic_api/#poluchenie-spiska-klientov-agentstva)
-   **getSites**. [Описание](https://www.comagic.ru/support/api/comagic_api/#poluchenie-spiska-saytov)
-   **getTags**. [Описание](https://www.comagic.ru/support/api/comagic_api/#poluchenie-spiska-tegov)
-   **getSummaryStats**. [Описание](https://www.comagic.ru/support/api/comagic_api/#poluchenie-statistiki-po-saytu)

    Входные параметры:
    
    siteId - идентификатор сайта, 
    
    dateFrom - стартовая дата подсчёта статистики, 
    
    dateTo - последняя дата подсчёта статистики, 
    
    acId - идентификатор кампании (необязательный), 
    
    customerId - идентификатор пользователя (необязательный), 
    
    byDate - получить суммарную статистику за период или в разбивке по дням (необязательный, по умолчанию - получение суммарной статистики).
-   **getCommunicationStats**. [Описание](https://www.comagic.ru/support/api/comagic_api/#poluchenie-spiska-obrasheniy)

    Входные параметры:
    
    siteId - идентификатор сайта, 
    
    dateFrom - стартовая дата подсчёта статистики, 
    
    dateTo - последняя дата подсчёта статистики, 
    
    acId - идентификатор кампании (необязательный), 
    
    customerId - идентификатор пользователя (необязательный), 
    
    showNotGoal - возвращать все обращения или только не "нецелевые" (необязательный),
    
    onlyFirst - возвращать все обращения или только первичные.
-   **getGoalStats**. [Описание](https://www.comagic.ru/support/api/comagic_api/#poluchenie-informacii-o-dostignutih-celyah)

    Входные параметры:
    
    siteId - идентификатор сайта, 
    
    dateFrom - стартовая дата подсчёта статистики, 
    
    dateTo - последняя дата подсчёта статистики, 
    
    acId - идентификатор кампании (необязательный), 
    
    customerId - идентификатор пользователя (необязательный), 
    
    goalId - идентификатор цели (необязательный),
    
    visitorId - идентификатор посетителя (необязательный),
    
    tagId - идентификатор тега (необязательный).
-   **getCallStats**. [Описание](https://www.comagic.ru/support/api/comagic_api/#poluchenie-informacii-o-zvonkah)

    Входные параметры:
    
    siteId - идентификатор сайта, 
    
    dateFrom - стартовая дата подсчёта статистики, 
    
    dateTo - последняя дата подсчёта статистики, 
    
    acId - идентификатор кампании (необязательный), 
    
    customerId - идентификатор пользователя (необязательный), 
    
    callId - идентификатор звонка (необязательный),
    
    visitorId - идентификатор посетителя (необязательный),
    
    tagId - идентификатор тега (необязательный),
    
    callId - идентификатор звонка (необязательный),
    
    direction - направление звонка (необязательный),
    
    numa - номер звонившего (необязательный),
    
    numb - номер принимавшего (необязательный),
    
    returnRecordUrls - возвращать ли дополнительный справочник с Id звонка и ссылкой на его запись (необязательный).
-   **endSession**. [Описание](https://www.comagic.ru/support/api/comagic_api/#zavershenie-sessii)

## Зависимости
   
  - Python3+
  - Модули:
    - urllib
    - json
    - requests
