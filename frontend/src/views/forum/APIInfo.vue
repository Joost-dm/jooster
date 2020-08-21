<template>
  <div class="api-info__body" >
    <div class="api-info__content">
      <div class="api-info__title">
        <h1>API Key</h1>
      </div>
      <div  class="api-info__text">
        Ваш уникальный ключ доступа к API:
      </div>
      <div v-if="apiKey" class="api-info__code">
        <pre>
          {{apiKey}}
        </pre>
      </div>
      <div class="api-info__title">
        <h1>Заголовок</h1>
      </div>
      <div class="api-info__text">
        <p>Короткие приветственные тексты

Короткие (до 1 000 знаков) приветственные тексты на главную страницу могут позволить себе далеко не все сайты. Например, почти все крупные интернет-магазины, сайты компаний, серьезные сервисы и прочие подобные ресурсы обходятся без громоздких «простыней» текста. Пара слов о компании, небольшое приветствие и все.

Короткие тексты размещают с одной целью – поприветствовать читателя и немного рассказать о себе. Собственно, именно так в идеале и должна выглядеть основная страница ресурса. Если бы не стремление поисковых систем высоко ранжировать запросы с главной страницы, думаю, 80% сайтов с радостью бы ограничивались скромным приветственным форматом.

Реалии же таковы, что короткие тексты обычно встречаются на трастовых и уважаемых сайтах, которые прекрасно чувствуют себя в выдаче. Наверное, в число «счастливчиков» можно добавить еще ресурсы, привлекающие трафик с рекламы – им тоже вполне комфортно без больших текстов на главных страницах.

Если же ресурс молодой и не слишком известный, редко кто упускает возможность дополнительно оптимизировать главную. Следовательно, материалы небольшого объема не подходят.</p>
      </div>
      <div class="api-info__code">
        <pre>
  {
      "id": 2,
      "email": "vasiliishirokov@gmail.com",
      "is_staff": true,
      "displayed": "Joost",
      "avatar_url": "https://jooster.s3.amazonaws.com/media/images/avatars/2/avatar.png",
      "messages_count": 23,
      "carma": 1
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
  overflow: scroll;
  background-color: $hover;
  padding-top: 1em;
  min-width: 300px;
  max-width: 700px;
  width: 100%;
  margin-bottom: 1em;
}

.api-info__code pre {
  font-size: 10px;
}
</style>
