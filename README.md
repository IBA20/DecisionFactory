# Тестовое задание: API для системы опросов пользователей
## 1. Интерфейс для администраторов опросов
1.1. api-auth/login - авторизация администратора опросов  

1.2. surveys/ - GET просмотр списка опросов текущего администратора, POST создание новых. Формат:  
{
    "title": "<text: Survey name>",
    "description": "<text: Description of survey>",
    "start_date": "<date: 2021-12-24>",
    "end_date": "<date: 2022-01-29>",
    "questions": [
        {
            "number": <int: Question number>,
            "text": "<text: Question text>",
            "type": <int: Question type>,
            "options": []
        },
        {
            "number": <int: Question number>,
            "text": "<text: Question text>",
            "type": <int: Question type>,
            "options": [
                {
                    "number": <int: Option number>,
                    "text": "<text: Answer option>"
                },
                {
                    "number": <int: Option number>,
                    "text": "<text: Answer option>"
                },
                {
                    "number": <int: Option number>,
                    "text": "<text: Answer option>"
                }
            ]
        }
    ]
}  

Question type: 
1 - textbox - ответ текстом
2 - single choice - выбор одного варианта ответа
3 - multiple choice - выбор нескольких варианта ответа

Options - варианты ответов для вопросов с типом 2 и 3.  

Question number, Option number - для сортировки вопросов и вариантов ответа.

1.3. surveys/<int:survey_id>/ - GET, PATH, DELETE просмотр, изменение, удаление опроса по id  
## 2. Интерфейс для участника опросов  
2.1. getactivesurveys/ - GET список активных опросов  

2.2. getpid/ - GET получение UUID участника опроса  

2.3. answers/UUID/ - GET получение списка пройденных опросов с ответами для участника с UUID, 
POST - сохранение ответов на вопросы (только новые ответы, редактирование ответов запрещено); формат:
[{"questionId":<int:question_id>, "text":<text: answer_text>}  

Рекомендуемый формат ответов: 

Вопрос тип 1 - обычный текст

Вопрос тип 2 - номер выбранной опции

Вопрос тип 3 - строка из 0 и 1, единицы соответствуют выбранным опциям.

Конкретная реализация формата - на усмотрение администратра опросов.

## 3. Примечания

Для тестирования используются счетные записи администраторов опросов: SurveyAdmin1/1234567*, SurveyAdmin2/1234567*. Учетная запись суперадминистратора Admin/12345.
