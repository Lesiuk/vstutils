# flake8: noqa: E501
TRANSLATION = {
    'create': 'создать',
    'add': 'добавить',
    'edit': 'редактировать',
    'save': 'сохранить',
    'remove': 'удалить',
    'reload': 'перезагрузить',
    'send': 'отправить',
    'select': 'выбрать',
    'filters': 'фильтры',
    'apply': 'применить',
    'cancel': 'отменить',
    'field': 'поле',
    'actions': 'действия',
    'sublinks': 'вложенные ссылки',
    'name': 'имя',
    'type': 'тип',
    'owner': 'владелец',
    'notes': 'заметки',
    'copy': 'копировать',
    'error': 'ошибка',
    'home': 'главная',
    'login': 'войти',
    'logout': 'выйти',
    'profile': 'профиль',
    'settings': 'настройки',
    'version': 'версий | версия | версии',
    'cache': 'кэш',
    'documentation': 'документация',
    'request': 'запрос',
    'repository': 'репозиторий',
    'app info': 'инфо',
    'status': 'статус',
    'list is empty': 'список пуст',
    'child instances': 'вложенные объекты',
    'enter value': 'введите значение',
    'more info': 'подробнее',
    'search by': 'поиск по полю',

    # field's validation
    # empty
    'Field "<b>{0}</b>" is empty.': 'Поле "<b>{0}</b>" пустое.',
    # required
    'Field "<b>{0}</b>" is required.': 'Поле "<b>{0}</b>" обязательно для заполнения.',
    # minLength
    'Field "<b>{0}</b>" is too short.<br> Field length should not be shorter, than {1}.': 'Длина поля "<b>{0}</b>" слишком мала.<br>Длина поля должна быть не меньше, чем {1}.',
    # maxLength
    'Field "<b>{0}</b>" is too long. <br> Field length should not be longer, than {1}.': 'Длина поля "<b>{0}</b>" слишком велика.<br>Длина поля должна быть не больше, чем {1}.',
    # min
    'Field "<b>{0}</b>" is too small.<br> Field should not be smaller, than {1}.': 'Значение поля "<b>{0}</b>" слишком мало.<br> Значение поля должно быть не меньше, чем {1}.',
    # max
    'Field "<b>{0}</b>" is too big.<br> Field should not be bigger, than {1}.': 'Значение поля "<b>{0}</b>" слишком велико.<br> Значение поля должно быть не больше, чем {1}.',
    # invalid
    '<b>{0} </b> value is not valid for <b>{1}</b> field.': 'Значение <b>{0}</b> не допустимо для поля <b>{1}</b>.',
    # email
    '<b>"{0}"</b> field should be written in <b>"example@mail.com"</b> format.': 'Поле <b>"{0}"</b> должно быть заполнено в формате <b>"example@mail.com"</b>.',


    # instance operation success
    # add
    'Child "<b>{0}</b>" instance was successfully added to parent list.': 'Дочерний объект "<b>{0}</b>" был успешно добавлен в родительский список.',
    # create
    'New "<b>{0}</b>" instance was successfully created.': 'Новый объект "<b>{0}</b>" был успешно создан.',
    # remove
    '"<b>{0}</b>" {1} was successfully removed.': '"<b>{0}</b>" {1} был(а) успешно удален.',
    # save
    'Changes in "<b>{0}</b>" {1} were successfully saved.': 'Изменения в объекте {1} "<b>{0}</b>" были успешно сохранены.',
    # execute
    'Action "<b>{0}</b>" was successfully executed on "<b>{1}</b>" instance.': 'Действие "<b>{0}</b>" было успешно запущено на объекте "<b>{1}</b>".',

    # instance operation error
    # add:
    'Some error occurred during adding of child "<b>{0}</b>" instance to parent list.<br> Error details: {1}': 'Во время добавления дочернего объекта "<b>{0}</b>" к родительскому списку произошла ошибка.<br> Подробнее: {1}',
    # create:
    'Some error occurred during new "<b>{0}</b>" instance creation.<br> Error details: {1}': 'Во время создания нового объекта "<b>{0}</b>" произошла ошибка.<br> Подробнее: {1}',
    # remove:
    'Some error occurred during remove process of "<b>{0}</b>" {1}.<br> Error details: {2}': 'Во время удаления {1} "<b>{0}</b>" произошла ошибка.<br> Подробнее: {2}',
    # save:
    'Some error occurred during saving process of "<b>{0}</b>" {1}.<br> Error details: {2}': 'Во время сохранения {1} "<b>{0}</b>" произошла ошибка.<br> Подробнее: {2}',
    # execute:
    'Some error occurred during "<b>{0}</b>" action execution on {1}.<br> Error details: {2}': 'Во время запуска действия "<b>{0}</b>" на {1} произошла ошибка.<br> Подробнее: {2}',

    # guiCustomizer translations
    'customize application styles': 'настройка цветовых стилей приложения',
    'skin': 'тема',
    'skin settings': 'настройки темы',
    'active menu background': 'фон активного элемента меню',
    'active menu color': 'активный элемент меню',
    'body background': 'фон страницы',
    'top navigation background': 'фон верхнего блока навигации',
    'top navigation border': 'окантовка верхнего блока навигации',
    'left sidebar background': 'фон сайдбара слева',
    'left sidebar border': 'окантовка сайдбара слева',
    'customizer sidebar background': 'фон данного сайдбара',
    'breadcrumbs background': 'фон хлебный крошек',
    'buttons default background': 'фон стандартной кнопки',
    'buttons default text': 'текст стандартной кнопки',
    'buttons default border': 'окантовка стандартной кнопки',
    'buttons primary background': 'фон основной кнопки',
    'buttons primary text': 'текст основной кнопки',
    'buttons primary border': 'окантовка основной кнопки',
    'buttons danger background': 'фон danger кнопки',
    'buttons danger text': 'текст danger кнопки',
    'buttons danger border': 'окантовка danger кнопки',
    'buttons warning background': 'фон warning кнопки',
    'buttons warning text': 'текст warning кнопки',
    'buttons warning border': 'окантовка warning кнопки',
    'links': 'ссылка',
    'links hover': 'ссылка при наведении',
    'links revers': 'ссылка на темном фоне',
    'links hover revers': 'ссылка на темном фоне при наведении',
    'text color': 'текст',
    'ico default color': 'стандартаный цвет иконки',
    'text header color': 'заголовок',
    'background default color': 'стандартный цвет фона',
    'card header background': 'фон верхней части "card" блока',
    'card body background': 'фон основной части "card" блока',
    'card footer background': 'фон нижней части "card" блока',
    'card color': 'текст "card" в блоке',
    'labels': 'лейбл',
    'help content': 'вспомогательный контент',
    'help text color': 'вспомогательный текст',
    'table line hover bg color': 'фон табличного ряда при наведении',
    'table border color': 'окантовка таблицы',
    'table line selected bg color': 'фон выделенного табличного ряда',
    'background active color': 'фон активного элемента',
    'background passive color': 'фон неактивного элемента',
    'text hover color': 'цвет текста при наведении',
    'boolean true color': 'цвет для булевых переменных со значением "true"',
    'boolean false color': 'цвет для булевых переменных со значением "false"',
    'modal background color': 'фон модального окна',
    'api sections background color': 'фон секций в Api',
    'api sections border color': 'окантовка секций в Api',
    'code highlighting color 1': 'подсветка кода - цвет 1',
    'code highlighting color 2': 'подсветка кода - цвет 2',
    'code highlighting color 3': 'подсветка кода - цвет 3',
    'code highlighting color 4': 'подсветка кода - цвет 4',
    'code highlighting color 5': 'подсветка кода - цвет 5',
    'code highlighting color 6': 'подсветка кода - цвет 6',
    'code highlighting color 7': 'подсветка кода - цвет 7',

    'custom css': 'пользовательский css',
    'reset skin settings to default': 'к настройкам по умолчанию',
    'save skin': 'сохранить тему',
    'Skin settings were successfully reset to default.': 'Настройки темы были успешно возвращены к стандратным.',
    'Skin settings were successfully saved': 'Настройки темы были успешно сохранены.',

    # multiactions button
    'actions on': 'действия над',
    'on item': 'элементов | элементом | элементами | элементами',

    'key': 'ключ',
    'value': 'значение',
    'new owner': 'новый владелец',
    'detail': 'детали',
    'description': 'описание',
    'username': 'имя пользователя',
    'is active': 'активен',
    'user': 'пользователь',
    'yes': 'да',
    'no': 'нет',
    'is staff': 'админ',
    'first name': 'имя',
    'last name': 'фамилия',
    'password': 'пароль',
    'change_password': 'сменить пароль',
    'generate password': 'сформировать пароль',
    'repeat password': 'повторить пароль',
    'old password': 'старый пароль',
    'new password': 'новый пароль',
    'confirm new password': 'подтвердить новый пароль',
    'kind': 'вид',
    'mode': 'режим',
    'options': 'опции',
    'information': 'информация',
    'date': 'дата',

    'file n selected': 'файл не выбран | 1 файл выбран | {n} файла выбрано | {n} файлов выбрано',
    'image n selected': 'изображение не выбрано | 1 изображение выбрано | {n} изображения выбрано | {n} изображений выбрано',

    # filters
    'ordering': 'порядок сортировки',
    'id__not': 'id не равный',
    'name__not': 'имя не равное',
    'is_active': 'активен',
    'first_name': 'имя',
    'last_name': 'фамилия',
    # 'email': '',
    'username__not': 'имя пользователя не равное',
    'status__not': 'статус не равный',

    # filters description
    'boolean value meaning status of user.': 'булево значение обозначающее статус пользователя.',
    'users first name.': 'имя пользователя',
    'users last name.': 'фамилия пользователя',
    'users e-mail value.': 'email пользователя',
    'which field to use when ordering the results.': 'поле по которому производить сортировку результатов.',
    'a unique integer value (or comma separated list) identifying this instance.': 'уникальное числовое значение (или их последовательность разделенная запятой) идентифицирующая данный объект.',
    'a name string value (or comma separated list) of instance.': 'имя объекта - строковое значение (или их последовательность разделенная запятой).',

    'page matching current url was not found': 'страница, соответствующая данному url, не была найдена',
}
