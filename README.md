# jooster
Vue + Drf forum engine

  Адрес развернутого проекта: http://joost.su

  Данное вэб-приложение разрабатывается мною в целях самообучения. Его использование реальными пользователями не запланировано. 
  Это мессенджер, по своей структуре схожий со Slack. Бэкенд написан на Django + Django Rest Framework, а фронтенд представляет собой SPA, написанное на Vue js с использованием Vuex, VueRouter, Vuetify.
  
  В качестве основной базы данных я использовал postgresql, а так же redis в качестве брокера сообщений для celery и для хранения онлайн-сессий пользователей. 
  
  Авторизация в API производится посредствам токенов, за основу взята библиотека joser.
  Авторизация через социальные сети реализована при помощи google firebase на фронтенде, на бэкенд отправляются uid пользователя (он уникален для любого пользователя firebase и выглядит примерно так: UWQhELQTgfhTejn2FKFtoh1PzO73) в качестве логина и он же в хешированом виде в качестве пароля (сериалайзер модели пользователя не выдаёт информацию о логине и пароле клиентской стороне), а так же передаётся прочяя информация, необходимая для создания полноценного пользователя(ссылка на аватар, отоброжаемое имя и.т.п).
  Фиксация онлайна пользователей реализована при помощи expire-записей в redis. Продолжительность сессии устанавливается в настройках django-проекта.
  
  Аватары пользователей после загрузки сжимаются пропорционально до заданных размеров и хранятся на AWS S3 Cloud, как и прочие медиа файлы проекта. Допустимые параметры изображений, разрешенных к загрузке, а так же параметры сжатия устанавливаются в настройках django проекта. Аватары пользователей делятся на 3 группы: по умолчанию, аватар из сторонних источников и загруженный пользователем аватар. Приоритет их отображения следующий: В первую очередь отображается автар, загруженный пользователем, если он отсутствует, показывается аватар из стороннего источника (полученный, например, при OAuth авторизации), если же отсутствует и он, отображается аватар по умолчанию.
  
  Структурно приложение представляет собой форумы, включающие в себя ветки, которые, в свою очередь, включают в себя темы, состоящие из сообщений.
  Реализована возможность создавать закрытые форумы и ветки, с функцией добавления в них участников создателем. В окне добавления участников создан реактивный поиск с фильтрацией списка по символам, с которых пользователь начинает ввод.
  Темы и сообщения выдаются пагинированно и добавляются в ленту при помощи бесконечного скролла.
  Валидация данных большей своей частью реализуется на серверной стороне. Настроены соответствующие пермишены для пользователей.
  Приложение я старался сделать максимально адаптивным. На маленьких экранах у основного компонента, отображающего список тем, появляется возможность показывать сообщения, а компонент, отвечавший за отображение сообщений, исчезает. Так же высота приложения адаптируется под высоту вьюпорта при скрытии адресной строки в мобильном браузере google chrome.
  
  Для тем и сообщений проработана система рейтинга. Пользователь имеет возможность их оценить негативно или положительно. Эти действия оказывают влияние на общую репутацию автора сообщения, которая отоброжается под его аватаром. Изменения происходят в реактивном режиме с выполнением соответствующих AJAX-запросов в фоне.
  Так же каждая тема и сообщение имеет фиксацию пользователей, запрашивающих её, на этом основывается система отоброжения количества непрочитанных пользователем тем в ветке и сообщений в теме.
  
  В формах отправки сообщений имеется поддержка эмоджи. Эмоджи хранятся в уникод символах и парсятся с последующей заменой на изображения при маунте компонента, содержащего их.
  
  У меня было большое желание использовать celery, но не было очевидных идей для его применения, потому я решил приспособить его для отслежования завершений пользовательских сессий. Был написан мидлвэр, логирующий запросы пользователя на сервер, хранящий логи в redis. И по завершении пользовательской сессии лог запросов пользователя с кодами ответов сервера отправляется мне на e-mail, а логи удаляются из базы. Эта информация теоретически будет полезна в выявлении некорректных ответов сервера, а так же производить общий анализ действий пользователей в приложении. Для мониторинга деятельности celery был подключен flower, который можно обнаружить на 5555 порту.
  
  Так же в бэкенд приложения интегрирован логгер Sentry.
  
  Сервер - nginx, запущен на vps от яндекс облака. Деплой приложеня осуществлялся при помощи Docker. За исключением базы данных, она развернута в файловой системе сервера. Так же я подключил к нему, имеющийся у меня домен.
  
  На этом я заканчиваю описание проделанной мною на данный момент работы, но не заканчиваю работу над этим приложением, есть еще много фич, которые я хотел бы реализовать и много багов, которые хочу пофиксить. Благодарю вас, за уделенное время и внимание к моему скромному проекту, надеюсь, оно потрачено не зря! :) 
  
  
  
  
  
  
