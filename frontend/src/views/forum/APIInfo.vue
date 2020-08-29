<template>
  <div class="api-info__body" >
    <div class="api-info__content">
      <div class="api-info__title"  id="api-navigation">
        <h1>Навигация</h1>
      </div>
      <div class="api-info__navigation">
        <ul class="api-info__links">
          <li><a href="#auth-token"></a>Токен авторизации</li>
          <li><a href="#authorization">Авторизация</a></li>
          <li><a href="#forum">Форумы</a></li>
          <li><a href="#forum-list">Получение списка всех форумов</a></li>
          <li><a href="#forum-new">Создание нового форума</a></li>
          <li><a href="#forum-details">Получение/редактирование/удаление форума</a></li>
          <li><a href="#forum-children">Получение веток форума</a></li>
          <li><a href="#forum-members">Добавление/удаление участника в закрытый форум</a></li>
          <li><a href="#branch">Ветки</a></li>
          <li><a href="#branch-new">Создание новой ветки</a></li>
          <li><a href="#branch-details">Получение/редактирование/удаление ветки</a></li>
          <li><a href="#branch-children">Получение тем ветки</a></li>
          <li><a href="#branch-members">Добавление участника в закрытую ветку</a></li>
          <li><a href="#thread">Темы</a></li>
          <li><a href="#thread-new">Создание новой темы</a></li>
          <li><a href="#thread-details">Получение/удаление/редактирование темы</a></li>
          <li><a href="#thread-children">Получение списка сообщений в теме</a></li>
          <li><a href="#thread-reaction">Установка реакции на тему</a></li>
          <li><a href="#post">Сообщения</a></li>
          <li><a href="#post-new">Создать новое сообщение</a></li>
          <li><a href="#post-details">Получение/удаление/редактирование сообщения</a></li>
          <li><a href="#post-reaction">Установка реакции на сообщение</a></li>
        </ul>
      </div>
      <div class="api-info__title" id="auth-token">
        <h1>Токен авторизации</h1>
      </div>
      <div class="api-info__subtitle">
        <p>API приложения использует токен-авторизацию, для его использования вашим запросам понадобится
          заголовок "Authorization" со значением формата "Token XXXXXXXXXXXXXXXXXXX", где вместо символов X
          будет находиться ваш токен авторизации.</p>
      </div>
      <div v-if="apiKey" class="api-info__code">
        {{user.displayed}}, ваш уникальный токен для доступа к API:
        <pre>
{{apiKey}}
        </pre>
      </div>
      <div class="api-info__subtitle">
        <p>Получить токен авторизации используя логин и пароль:</p>
      </div>
      <div class="api-info__code">
Путь:
<pre>
/api/v1/auth/token/login/
Allowed methods: POST
Content-Type: application/json
</pre>
Привер запроса:
<pre>
request: /api/v1/auth/token/login/
method: POST

{
    "password": "password",
    "username": "username"
}
</pre>
Пример ответа:
<pre>
response: Http 200 OK

{
    "auth_token": "##################################"
}
</pre>
      </div>
      <div class="api-info__title" id="authorization">
      <h1>Авторизация</h1>
      </div>
      <div class="api-info__title"  id="forum">
        <h1>Форумы</h1>
      </div>
      <div class="api-info__subtitle" id="forum-list">
        <p>Получение списка всех форумов:</p><br>
      </div>
      <div class="api-info__code">

Путь:
<pre>
api/v1/forum/all/
Allowed methods: GET
</pre>
Пример:
<pre>
request: api/v1/forum/all/
method: GET

response: Http 200 OK
[
  {
    "id": 1,
    "author": {
        "id": 1,
        "email": "vasiliishirokov@gmail.com",
        "is_staff": true,
        "displayed": "Василий Широков",
        "avatar_url": "https://jooster.s3.amazonaws.com/media/images/avatars/1/avatar.jpeg",
        "messages_count": 2,
        "carma": 0
    },
    "children_count": 2,
    "title": "Первый форум",
    "description": "",
    "pub_date": "2020-08-12T08:24:40.102245+03:00",
    "is_private": false,
    "members": []
  },
  {
    "id": 13,
    "author": {
        "id": 9,
        "email": "ksenof@greece.gc",
        "is_staff": false,
        "displayed": "Ксенофонт",
        "avatar_url": "https://jooster.s3.amazonaws.com/media/images/avatars/9/avatar.jpeg",
        "messages_count": 8,
        "carma": 3
    },
    "children_count": 0,
    "title": "Закрытый форум",
    "description": "",
    "pub_date": "2020-08-26T01:21:14.047858+03:00",
    "is_private": true,
    "members": [
        9
    ]
  },
]
        </pre>
      </div>
      <div class="api-info__subtitle" id="forum-new">
        <p>Создание нового форума:</p>
      </div>
      <div class="api-info__code">
Путь:
<pre>
api/v1/forum/add/
Allowed methods: POST
</pre>
Пример запроса:
<pre>
request: api/v1/forum/add/
method: POST
Content-Type: application/json

{
    "title": "Forum Title",
    "is_private": false
}
</pre>
Пример ответа:
<pre>
response: Http 201 Created
{
    "id": 1,
    "title": "Forum Title",
    "description": "",
    "pub_date": "2020-08-26T02:23:48.278039+03:00",
    "is_private": false,
    "members": []
}
        </pre>
      </div>
      <div class="api-info__subtitle" id="forum-details">
        <p>Получение/редактирование/удаление форума:</p>
      </div>
      <div class="api-info__code">
Путь:
<pre>
api/v1/forum/{forum ID}/
Allowed methods: GET, PUT, DELETE
Content-Type: application/json
</pre>

Пример:
<pre>
request: api/v1/forum/11/
method: GET

response: Http 200 OK
 {
    "id": 11,
    "author": {
        "id": 2,
        "is_staff": false,
        "displayed": "Василий Широков",
        "avatar_url": "https://jooster.s3.amazonaws.com/media/images/avatars/2/avatar.png",
        "messages_count": 13,
        "carma": 2
    },
    "children_count": 6,
    "title": "Закрытый форум",
    "description": "",
    "pub_date": "2020-08-19T02:12:48.653386+03:00",
    "is_private": true,
    "members": [
        2,
        4,
        3
    ]
 }
        </pre>
      </div>
      <div class="api-info__subtitle" id="forum-children">
        <p>Получение веток форума:</p>
      </div>
      <div class="api-info__code">
Путь:
<pre>
api/v1/forum/{forum ID}/children/
Allowed methods: GET
</pre>
Пример:
<pre>
request: api/v1/forum/11/children/
method: GET

response: Http 200 OK
 [
    {
        "id": 8,
        "author": {
            "id": 6,
            "email": "lao@china.ch",
            "is_staff": false,
            "displayed": "Лао-Цзы",
            "avatar_url": "https://jooster.s3.amazonaws.com/media/images/avatars/6/avatar.jpeg",
            "messages_count": 12,
            "carma": 11
        },
        "children_count": 2,
        "unread_count": 2,
        "title": "Ветка второго форума",
        "pub_date": "2020-08-26T00:32:43.389788+03:00",
        "is_private": false,
        "parent_forum": 11,
        "members": []
    },
    {
        "id": 10,
        "author": {
            "id": 6,
            "email": "lao@china.ch",
            "is_staff": false,
            "displayed": "Лао-Цзы",
            "avatar_url": "https://jooster.s3.amazonaws.com/media/images/avatars/6/avatar.jpeg",
            "messages_count": 12,
            "carma": 11
        },
        "children_count": 0,
        "unread_count": 0,
        "title": "Еще ветка",
        "pub_date": "2020-08-26T03:31:34.649334+03:00",
        "is_private": false,
        "parent_forum": 11,
        "members": []
    }
 ]
        </pre>
      </div>
      <div class="api-info__subtitle" id="forum-members">
        <p>Добавление/удаление участника в закрытый форум:</p>
      </div>
      <div class="api-info__code">
Путь:
<pre>
api/v1/forum/{Forum ID}/membership/{User ID}/
Allowed methods: POST, DELETE
Content-Type: application/json
Body: Empty
</pre>
Пример:
<pre>
request: api/v1/forum/1/membership/1/
Method: POST
Body: Empty

response: Http 201 Created
{
    "user": 1,
    "forum": 1
}
</pre>
      </div>
      <div class="api-info__title" id="branch">
        <h1>Ветки</h1>
      </div>
      <div class="api-info__subtitle" id="branch-new">
        <p>Создание новой ветки:</p>
      </div>
      <div class="api-info__code">
Путь:
<pre>
api/v1/branch/add/
Allowed methods: POST
Content-Type: application/json
</pre>
Пример запроса:
<pre>
request: api/v1/branch/add/
method: POST

{
    "title": "Branch Title",
    "is_private": false,
    "parent_forum": 14
}
</pre>
Пример ответа:
<pre>
response: Http 201 Created
{
    "id": 5,
    "title": "Branch Title",
    "pub_date": "2020-08-26T02:28:59.775412+03:00",
    "is_private": false,
    "parent_forum": 1,
    "members": []
}
</pre>
      </div>
      <div class="api-info__subtitle" id="branch-details">
        <p>Получение/редактирование/удаление ветки:</p>
      </div>
      <div class="api-info__code">
Путь:
<pre>
api/v1/branch/{Branch ID}/
Allowed methods: GET, PUT, DELETE
Content-Type: application/json
</pre>
Пример:
<pre>
request api/v1/branch/3/
method: GET

response: Http 200 OK
{
    "id": 3,
    "author": {
        "id": 2,
        "is_staff": false,
        "displayed": "Василий Широков",
        "avatar_url": "https://jooster.s3.amazonaws.com/media/images/avatars/2/avatar.png",
        "messages_count": 13,
        "carma": 2
    },
    "children_count": 2,
    "unread_count": 0,
    "title": "Закрытая ветка",
    "pub_date": "2020-08-18T23:47:01.333892+03:00",
    "is_private": true,
    "parent_forum": 1,
    "members": [
        1,
        2
    ]
}
</pre>
      </div>
      <div class="api-info__subtitle"  id="branch-children">
        <p>Получение тем ветки:</p>
      </div>
      <div class="api-info__code">
Путь:
<pre>
api/v1/branch/{Branch ID}/children/
Allowed methods: GET
</pre>
Пример:
<pre>
request: api/v1/branch/1/children/
method: GET

response: Http 200 OK
{
  "count": 32,
  "next": "http://joost.su/api/v1/branch/1/children/?page=2",
  "previous": null,
  "results": [
      {
          "id": 41,
          "author": {
              "id": 1,
              "is_staff": true,
              "displayed": "Joost",
              "avatar_url": "https://jooster.s3.amazonaws.com/media/images/avatars/1/avatar.jpeg",
              "messages_count": 39,
              "carma": 5
          },
          "children_count": 0,
          "unread_count": 0,
          "carma": 0,
          "users_liked_list": [],
          "users_disliked_list": [],
          "text": "Thread Text",
          "pub_date": "2020-08-26T02:41:58.536156+03:00",
          "parent_forum": 1,
          "parent_branch": 1,
          "viewers": [
              1,
              2
          ],
          "parent_branch_title": "Первая ветка"
      },
      {
          "id": 40,
          "author": {
              "id": 1,
              "is_staff": true,
              "displayed": "Joost",
              "avatar_url": "https://jooster.s3.amazonaws.com/media/images/avatars/1/avatar.jpeg",
              "messages_count": 39,
              "carma": 5
          },
          "children_count": 0,
          "unread_count": 0,
          "carma": 0,
          "users_liked_list": [],
          "users_disliked_list": [],
          "text": "123",
          "pub_date": "2020-08-25T01:15:03.525682+03:00",
          "parent_forum": 1,
          "parent_branch": 1,
          "viewers": [
              1,
              5,
              2
          ],
          "parent_branch_title": "Первая ветка"
      }
  ]
}
</pre>
      </div>
      <div class="api-info__subtitle"  id="branch-members">
        <p>Добавление участника в закрытую ветку:</p>
      </div>
      <div class="api-info__code">
Путь:
<pre>
api/v1/branch/{Branch ID}/membership/{User ID}/
Allowed methods: POST, DELETE
Body: Empty
</pre>
Пример:
<pre>
request: api/v1/branch/1/membership/1/
method: POST
body: Empty

response: HTTP 201 Created
{
    "user": 1,
    "branch": 1
}
</pre>
      </div>
      <div class="api-info__title" id="thread">
        <h1>Темы</h1>
      </div>
      <div class="api-info__subtitle"  id="thread-new">
        <p>Создание новой темы:</p>
      </div>
      <div class="api-info__code">
Путь:
<pre>
api/v1/thread/add/
Allowed methods: POST
Content-Type: application/json
</pre>
Пример запроса:
<pre>
request: api/v1/thread/add/
method: POST

{
    "text": "Thread Text",
    "parent_branch": 1
}
</pre>
Пример ответа:
<pre>
response: Http 201 Created
{
    "id": 41,
    "text": "Thread Text",
    "pub_date": "2020-08-26T02:41:58.536156+03:00",
    "parent_forum": 1,
    "parent_branch": 1,
    "likes": [],
    "viewers": []
}
</pre>
      </div>
      <div class="api-info__subtitle"  id="thread-details">
        <p>Получение/удаление/редактирование темы:</p>
      </div>
      <div class="api-info__code">
Путь:
<pre>
api/v1/thread/{Thread ID}/
Allowed methods: GET, PUT, DELETE
Content-Type: application/json
</pre>
Пример:
<pre>
request: api/v1/thread/1/
method: GET

response: Http 200 OK
{
    "id": 1,
    "author": {
        "id": 1,
        "is_staff": true,
        "displayed": "Joost",
        "avatar_url": "https://jooster.s3.amazonaws.com/media/images/avatars/1/avatar.jpeg",
        "messages_count": 39,
        "carma": 5
    },
    "children_count": 1,
    "unread_count": 1,
    "carma": 1,
    "users_liked_list": [
        2
    ],
    "users_disliked_list": [],
    "text": "1",
    "pub_date": "2020-08-13T00:31:59.880739+03:00",
    "parent_forum": 1,
    "parent_branch": 1,
    "viewers": [
        4,
        2,
        1,
        9
    ],
    "parent_branch_title": "Первая ветка"
}
</pre>
      </div>
      <div class="api-info__subtitle" id="thread-children">
        <p>Получение списка сообщений в теме:</p>
      </div>
      <div class="api-info__code">
Путь:
<pre>
api/v1/thread/{Thread ID}/children/
Allowed methods: GET
</pre>
Пример:
<pre>
request: api/v1/thread/43/children/
method: GET

response: Http 200 OK
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 60,
            "author": {
                "id": 10,
                "email": "makiavelli@italy.ik",
                "is_staff": false,
                "displayed": "Никколо Макиавелли",
                "avatar_url": "https://jooster.s3.amazonaws.com/media/images/avatars/10/avatar.jpeg",
                "messages_count": 8,
                "carma": 2
            },
            "carma": 0,
            "users_liked_list": [],
            "users_disliked_list": [],
            "text": "Умы бывают трех родов: один все постигает сам; другой может понять то, что постиг первый; третий — сам ничего не постигает и постигнутого другим понять не может. Первый ум — выдающийся, второй — значительный, третий — негодный.",
            "pub_date": "2020-08-26T01:10:06.445314+03:00",
            "parent_forum": 1,
            "parent_branch": 1,
            "parent_thread": 43,
            "viewers": [
                1,
                6,
                10
            ]
        },
        {
            "id": 54,
            "author": {
                "id": 7,
                "email": "conf@china.ch",
                "is_staff": false,
                "displayed": "Конфуций",
                "avatar_url": "https://jooster.s3.amazonaws.com/media/images/avatars/7/avatar.jpeg",
                "messages_count": 11,
                "carma": 4
            },
            "carma": 0,
            "users_liked_list": [],
            "users_disliked_list": [],
            "text": "Если вы самый умный человек в комнате, то вы не в той комнате, где должны находиться.",
            "pub_date": "2020-08-26T01:03:41.067056+03:00",
            "parent_forum": 1,
            "parent_branch": 1,
            "parent_thread": 43,
            "viewers": [
                1,
                6,
                7,
                10
            ]
        }
    ]
}
</pre>
      </div>
      <div class="api-info__subtitle" id="thread-reaction">
      <p>Установка реакции на тему:</p>
      </div>
      <div class="api-info__code">
Путь:
<pre>
api/v1/thread/{Thread ID}/like/
Allowed methods: POST, DELETE
Content-Type: application/json
</pre>
Пример запроса:
<pre>
request: api/v1/thread/2/like/
method: POST

{
    "like": false
  // False - для дизлайка, True - для лайка.
  // При наличии дизлайка, первый лайк отменяет дизлайк, второй идёт в счёт лайка и наоборот.
}
</pre>
Пример ответа:
<pre>
response: Http 201 Created
{
    "thread": 2,
    "like": false
}
</pre>
  </div>
      <div class="api-info__title" id="post">
        <h1>Сообщения</h1>
      </div>
      <div class="api-info__subtitle" id="post-new">
        <p>Создать новое сообщение:</p>
      </div>
      <div class="api-info__code">
Путь:
<pre>
api/v1/post/add/
Allowed methods: POST
Content-Type: application/json
</pre>
Пример запроса:
<pre>
request: api/v1/post/add/
method: POST

{
    "text": "Post Text",
    "parent_thread": 1
}
</pre>
Пример ответа:
<pre>
response: Http 201 Created
{
    "id": 20,
    "text": "Post Text",
    "pub_date": "2020-08-26T02:43:56.605610+03:00",
    "parent_thread": 1,
    "parent_forum": 1,
    "parent_branch": 1,
    "likes": [],
    "viewers": []
}
</pre>
      </div>
      <div class="api-info__subtitle" id="post-details">
        <p>Получение/удаление/редактирование сообщения:</p>
      </div>
      <div class="api-info__code">
Путь:
<pre>
api/v1/post/{Post ID}/
Allowed methods: GET PUT DELETE
Content-Type: application/json
</pre>
Пример:
<pre>
request: api/v1/post/1/
method: GET

response: Http 200 OK
{
    "id": 1,
    "author": {
        "id": 1,
        "is_staff": true,
        "displayed": "Joost",
        "avatar_url": "https://jooster.s3.amazonaws.com/media/images/avatars/1/avatar.jpeg",
        "messages_count": 39,
        "carma": 5
    },
    "carma": 0,
    "users_liked_list": [],
    "users_disliked_list": [],
    "text": "1",
    "pub_date": "2020-08-13T00:33:03.186998+03:00",
    "parent_forum": 1,
    "parent_branch": 1,
    "parent_thread": 21,
    "viewers": [
        1,
        5,
        2
    ]
}
</pre>
      </div>
      <div class="api-info__subtitle" id="post-reaction">
      <p>Установка реакции на сообщение:</p>
    </div>
      <div class="api-info__code">
Путь:
<pre>
api/v1/post/{Post ID}/like/
Allowed methods: POST, DELETE
Content-Type: application/json
</pre>
Пример запроса:
<pre>
request: api/v1/post/1/like/
method: POST

{
    "like": false
  // False - для дизлайка, True - для лайка.
  // При наличии дизлайка, первый лайк отменяет дизлайк, второй идёт в счёт лайка и наоборот.
}
</pre>
Пример ответа:
<pre>
response: Http 201 Created
{
    "post": 1,
    "like": false
}
</pre>
  </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'APIInfo',
  computed: {
    apiKey () {
      return this.$store.getters.getAuthToken
    },
    user () {
      return this.$store.getters.getCurrentUser
    }
  }
}
</script>
<style scoped lang="scss">

@import 'src/styles/variables';

.api-info__body {
  display: flex;
  justify-content: center;
  align-content: center;
  min-height: 100%;
  width: 100%;
  padding: 1rem 0 1rem 0;
  background-color: $secondary;
  border-right: solid $third-party 1px;
}

.api-info__content {
  display: flex;
  flex-direction: column;
  align-content: stretch;
  align-items: center;
  height: 100%;
  min-width: 300px;
  max-width: 1000px;
  padding: 1rem;
  scroll-behavior: smooth;
}
.api-info__up-button {
  position: absolute;
  top: 70px;
  width: 100px;
  height: 100%;
  background-color: green;
}
.api-info__navigation {
  width: 100%;
  margin-bottom: 3rem;
}
.api-info__links li a{
  text-decoration: none;
}
.api-info__links li a:hover{
  color: $extra;
}
.api-info__title {
  display: flex;
  position: relative;
  margin-bottom: 1em;
  width: 100%;
}
.api-info__title h1 {
  font-size: 22px;
  font-weight: bold;
}

.api-info__title:before {
  background-color: $primary;
  width: 170px;
  height: 2px;
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
}

.api-info__title:after {
  background-color: $extra;
  width: 30px;
  height: 2px;
  content: '';
  position: absolute;
  bottom: 0;
  left: 170px;
  border-bottom-right-radius: 2px;
}

.api-info__subtitle {
  margin-top: 1rem;
  display: flex;
  width: 100%;
  font-weight: 600;
  padding-left: 0;
  max-width: 700px;
}
.api-info__subtitle p {
  font-size: 14px;
  text-align: justify;
}

.api-info__code {
  width: 100%;
  font-size: 12px;
}

.api-info__code pre {
  overflow: scroll;
  background-color: $hover;
  min-width: 300px;
  max-width: 700px;
  font-size: 10px;
  margin-bottom: 1rem;
  padding: 1rem;
}
</style>
