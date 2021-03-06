<template>
 <div class="wrapper">
    <v-textarea
      outlined
      auto-grow
      rows="3"
      class="regular-input"
      label="Новое сообщение"
      v-model="newMessage.text"
      hide-details
    >
    </v-textarea>
    <emoji-picker @emoji="append" :search="search">
      <div
        @click="emojiParse"
        class="emoji-invoker"
        slot="emoji-invoker"
        slot-scope="{ events: { click: clickEvent } }"
        @click.stop="clickEvent"
      >
        <svg height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg">
          <path d="M0 0h24v24H0z" fill="none"/>
          <path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42
           0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm3.5-9c.83 0 1.5-.67 1.5-1.5S16.33 8 15.5 8 14 8.67 14 9.5s.67
           1.5 1.5 1.5zm-7 0c.83 0 1.5-.67 1.5-1.5S9.33 8 8.5 8 7 8.67 7 9.5 7.67 11 8.5 11zm3.5 6.5c2.33 0 4.31-1.46
            5.11-3.5H6.89c.8 2.04 2.78 3.5 5.11 3.5z"/>
        </svg>
      </div>
      <div slot="emoji-picker" slot-scope="{ emojis, insert, display }">
        <div class="emoji-picker" :style="{ top: display.y + 'px', left: display.x + 'px' }">
          <div class="emoji-picker__search">
            <input type="text" v-model="search" v-focus>
          </div>
          <div>
            <div v-for="(emojiGroup, category) in emojis" :key="category">
              <h5>{{ category }}</h5>
              <div class="emojis">
                <span
                  v-for="(emoji, emojiName) in emojiGroup"
                  :key="emojiName"
                  @click="insert(emoji)"
                  :title="emojiName"
                >{{ emoji }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </emoji-picker>
    <v-icon class="bottom-form__button" @click="createPost">mdi-send</v-icon>
  </div>
</template>

<script>
import EmojiPicker from 'vue-emoji-picker'
import twemoji from 'twemoji'
export default {
  name: 'TrainingVue',
  components: {
    'emoji-picker': EmojiPicker
  },
  data () {
    return {
      newMessage: {
        text: ''
      },
      search: ''
    }
  },
  methods: {
    async createPost () {
      if (this.type === 'post') {
        this.newMessage.parent_thread = this.currentThread.id
        await this.$store.dispatch('createPost', this.newMessage)
      } else if (this.type === 'thread') {
        this.newMessage.parent_branch = this.currentBranch.id
        await this.$store.dispatch('createThread', this.newMessage)
      }
      this.user.messages_count++
      this.newMessage.text = ''
    },
    append (emoji) {
      this.newMessage.text += emoji
    },
    async emojiParse () {
      function timeout (ms) {
        return new Promise(resolve => setTimeout(resolve, ms))
      }
      await timeout(1)
      document.getElementsByClassName('emojis').forEach(element => twemoji.parse(element))
      document.getElementsByClassName('emoji').forEach(emoji => {
        emoji.style.cssText = `
          height: 1em;
          width: 1em;
          margin: 0 .05em 0 .1em;
          vertical-align: -0.1em;
        `
      })
    }
  },
  directives: {
    focus: {
      inserted (el) {
        el.focus()
      }
    }
  },
  props: ['type'],
  computed: {
    currentThread () {
      return this.$store.getters.getCurrentThread
    },
    currentBranch () {
      return this.$store.getters.getCurrentBranch
    },
    user () {
      return this.$store.getters.getCurrentUser
    }
  }
}
</script>

<style scoped lang="scss">
@import "../../styles/variables";
.wrapper {
  position: relative;
  display: inline-block;
  padding-top: 10px;
  width: 100%;
  background-color: $secondary;
  z-index: 2;
}
.bottom-form__button {
  z-index: 3;
  color: $extra;
  position: absolute;
  bottom: 0.5rem;
  right: 5px;
  font-size: 25px;
  transition: all 0.2s;
}
.bottom-form__button:hover {
  transform: scale(1.2);
}
.emoji-invoker {
  z-index: 3;
  position: absolute;
  bottom: 1.5rem;
  right: 0.5rem;
  width: 1.5rem;
  height: 2.3rem;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s;
}
.regular-input {
  position: relative;
  width: 100%;
  font-family: Montserrat;
}
.emoji-invoker:hover {
  transform: scale(1.2);
}
.emoji-invoker > svg {
  fill: $third-party;
}
.emoji-picker {
  position: absolute;
  z-index: 4;
  font-family: Montserrat;
  left: auto !important;
  right: 0;
  top: auto !important;
  bottom: 0 !important;
  border: 1px solid $third-party;
  width: 360px;
  height: 15rem;
  overflow: scroll;
  padding: 1rem;
  box-sizing: border-box;
  border-radius: 0.5rem;
  background: $secondary;
  box-shadow: 1px 1px 8px $third-party;
}
.emoji-picker__search {
  display: flex;
}
.emoji-picker__search > input {
  flex: 1;
  border-radius: 10rem;
  border: 1px solid $third-party;
  padding: 0.5rem 1rem;
  outline: none;
}
.emoji-picker h5 {
  margin-bottom: 0;
  color: $third-party;
  text-transform: uppercase;
  font-size: 0.8rem;
  cursor: default;
}
.emoji-picker .emojis {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  font-size:  1.3rem;
}
.emoji-picker .emojis:after {
  content: "";
  flex: auto;
}
.emoji-picker .emojis span {
  padding: 0.2rem;
  cursor: pointer;
  border-radius: 5px;
}
.emoji-picker .emojis span:hover {
  background: $hover;
  cursor: pointer;
}
</style>
