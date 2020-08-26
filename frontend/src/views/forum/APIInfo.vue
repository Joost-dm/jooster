<template>
  <div class="api-info__body" >
    <div class="api-info__content">
      <div class="api-info__title">
        <h1>API Key</h1>
      </div>
      <div v-if="apiKey" class="api-info__code">
        Ваш уникальный ключ доступа к API:
        <pre>
 {{apiKey}}
        </pre>
      </div>
      <div class="api-info__title">
        <h1>Форумы</h1>
      </div>
      <div class="api-info__text">
        <p>Получение списка всех форумов:</p><br>
      </div>
      <div class="api-info__code">

 Запрос:
<pre>
 /forum/all/ method: GET
 Allowed methods: GET
</pre>
 Пример ответа:
<pre>
 Http 200 OK
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
      <div class="api-info__text">
        <p>Создание нового форума:</p>
      </div>
      <div class="api-info__code">

Запрос:
<pre>
/forum/add/ method: POST
Allowed methods: POST
Content-Type: application/json
</pre>
Пример запроса:
<pre>
POST
{
    "title": "Forum Title",
    "is_private": false
}
</pre>
Пример ответа:
<pre>
201 Created
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
      <div class="api-info__text">
        <p>Получение/редактирование/удаление форума:</p>
      </div>
      <div class="api-info__code">
Запрос:
<pre>
/forum/{forum ID}/ Method: GET
Allowed methods: GET, PUT, DELETE
</pre>

Пример ответа:
<pre>
 200 OK
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
      <div class="api-info__text">
        <p>Получение веток форума:</p>
      </div>
      <div class="api-info__code">
Запрос:
<pre>
/forum/{forum ID}/children/ Method: GET
  Allowed methods: GET
</pre>
Пример ответа:
<pre>
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
        "is_unread": 2,
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
        "is_unread": 0,
        "title": "Еще ветка",
        "pub_date": "2020-08-26T03:31:34.649334+03:00",
        "is_private": false,
        "parent_forum": 11,
        "members": []
    }
 ]
        </pre>
      </div>
      <div class="api-info__text">
        <p>Добавление/удаление участника в закрытый форум:</p>
      </div>
      <div class="api-info__code">
Запрос:
        <pre>
/forum/{Forum ID}/membership/{User ID}/ Method: POST, Body: empty
Allowed methods: POST, DELETE
Content-Type: application/json
</pre>
Привер ответа:
<pre>
HTTP 201 Created
{
    "user": 1,
    "forum": 1
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

.api-info__text {
  display: flex;
  width: 100%;
  margin-bottom: 1em;
}
.api-info__text p {
  font-size: 14px;
  text-align: justify;
  text-indent: 1em;
}

.api-info__code {
  width: 100%;
  font-size: 12px;
}

.api-info__code pre {
  overflow: scroll;
  background-color: $hover;
  padding-top: 1em;
  min-width: 300px;
  max-width: 700px;
  font-size: 10px;
  margin-bottom: 1em;
}
</style>
