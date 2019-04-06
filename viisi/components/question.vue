<template lang="pug">
  div.question(v-if="isLoaded")
    div.skip-container(v-if="!isAtWelcomeScreen")
      a.skip-step.fa.fa-share
    div(v-if="isAtWelcomeScreen")
      div.welcome-text 
        b {{ __i("welcome-text-title") }}
        p(v-html="__i('welcome-text')")
      div.languages
        div(v-for="(locale, locale_key) in $store.state.locales", :key="locale_key", class="locale-container")
          span(:class="'flag-icon-' + locale").flag-icon
          span.locale-text 
            a(href="#") {{ __i("locale-link-"+locale) }}
      div.actions
        button.next-step(@click="startTest") {{ __i("start-test") }}
    div(v-else)
      div.question-text {{ __i(question.msgid) }}
      div.answer-remark(v-if="question.isMultipleChoice")
        span {{ __i("question-is-multiplechoice") }}
      div.answers
        div.answer(v-for="(answer, a_key) in answers", :key="a_key",:class="{'answer-selected animated pulse fast': isAnswerSelected(answer)}",@click='answerQuestion(answer)')
          span.answer-text {{ __i(answer.msgid) }}
          a.mark-important(v-if="isAnswerSelected(answer)",:class="{'is-important': answer.isImportant}", @click="markImportant(answer)") important for me!
      div.actions
        button.next-step(@click="nextQuestion") {{  __i(isAtLastQuestion() ? "get-result" : "next-question") }}
</template>
<script>
import i18n from '~/mixins/i18n'
export default {
  mixins: [i18n],
  props: {
    language: {
      type: String,
      required: true,
      default: 'en'
    }
  },
  computed: {
    isLoaded() {
      return this.$store.state !== null
    },
    question() {
      return this.$store.state.question
    },
    answers() {
      return this.$store.state.answers
    },
    isAtWelcomeScreen() {
      return !this.$store.state.isStarted
    }
  },
  methods: {
    answerQuestion(answer) {
      if (this.isAnswerSelected(answer)) {
        this.$store.commit('removeAnswerQuestion', answer)
      } else {
        this.$store.dispatch('answerQuestion', {
          selectedAnswer: answer
        })
      }
    },
    startTest() {
      var _t = this
      this.$store.dispatch('nextQuestion', {
        params: {
          language: _t.language
        }
      })
    },
    nextQuestion() {
      var _t = this
      if (!this.isAtLastQuestion()) {
        this.$store.dispatch('nextQuestion', {
          params: {
            language: _t.language
          }
        })
      } else {
        this.$store.dispatch('submitAnswers', {
          params: {
            token: this.$store.state.token,
            language: _t.language
          },
          data: {
            answers: this.$store.state.givenAnswers
          }
        })
      }
    },
    isAtLastQuestion() {
      var currentIndex = this.$store.state.currentCategory.index
      var maximumIndex = Math.max.apply(
        Math,
        this.$store.state.categories.map(function(c) {
          return c.index
        })
      )
      return currentIndex === maximumIndex
    },
    isAnswerSelected(answer) {
      return (
        this.$store.state.givenAnswers.filter(a => a.msgid === answer.msgid)
          .length === 1
      )
    },
    markImportant(answer) {
      this.$store.commit('toggleImportanceState', answer)
    }
  }
}
</script>
<style lang="scss" scoped>
@import '~/scss/variables.scss';
@import '~/node_modules/animate.css/animate.min.css';
@import '~/node_modules/flag-icon-css/css/flag-icon.min.css';
.question {
  margin-top: 3em;
  width: 70%;
  margin-right: 15%;
  margin-left: 15%;
  background: $questionBackground;
  height: 25em;
}
@media only screen and (max-width: $mobileWidth) {
  .question {
    width: 90%;
    margin-left: 5%;
    margin-right: 5%;
  }
  .answer-remark {
    left: 53% !important;
  }
  .next-step {
    left: 80% !important;
  }
}

@media only screen and (max-width: $desktopMinWidth) {
  .question {
    width: 90%;
    margin-left: 5%;
    margin-right: 5%;
  }
}
.question-text,
.welcome-text {
  font-family: 'Heebo', sans-serif;
  padding: 2em;
  font-size: 13pt;
  font-weight: 300;
  height: 40%;
}
.welcome-text {
  padding-bottom: 0.5em;
}
.welcome-text b {
  margin-bottom: 1em;
  display: block;
  padding-bottom: 0.5em;
  display: block;
  color: #4484ce;
}
ul {
  padding-top: 0.5em;
}
.answer {
  background: $unselectedAnswerBackground !important;
  color: $unselectedAnswerForeground !important;
  height: 40px;
  padding: 10px;
  font-family: Karla, sans-serif;
  margin-bottom: 1em;
  cursor: pointer;
}
.answer-selected {
  background: $selectedAnswerBackground !important;
  color: $selectedAnswerForeground !important;
  margin-right: -0.5em;
  margin-left: -0.5em;
}
.next-step {
  background: $nextButtonBackground;
  color: $nextButtonForeground;
  position: fixed;
  height: 40px;
  width: 80px;
  border: 0px;
  cursor: pointer;
  left: 62%;
  border-radius: 4px;
}
.skip-step {
  position: relative;
  left: 95%;
  top: 0.5em;
  display: inline;
  color: $skipButtonColor;
}
.answer-remark {
  font-family: karla;
  font-style: italic;
  font-size: 9pt;
  position: relative;
  left: 5%;
  bottom: 1em;
}
.mark-important {
  display: none; // it's disabled until I find a proper solution
}
.is-important {
  color: $markImportantSelectedColor;
}
// Flag addition
.flag-icon-en {
  background-image: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIGlkPSJmbGFnLWljb24tY3NzLWdiIiB2aWV3Qm94PSIwIDAgNjQwIDQ4MCI+CiAgPGRlZnM+CiAgICA8Y2xpcFBhdGggaWQ9ImEiPgogICAgICA8cGF0aCBmaWxsLW9wYWNpdHk9Ii43IiBkPSJNLTg1LjMgMGg2ODIuNnY1MTJILTg1LjN6Ii8+CiAgICA8L2NsaXBQYXRoPgogIDwvZGVmcz4KICA8ZyBjbGlwLXBhdGg9InVybCgjYSkiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDgwKSBzY2FsZSguOTQpIj4KICAgIDxnIHN0cm9rZS13aWR0aD0iMXB0Ij4KICAgICAgPHBhdGggZmlsbD0iIzAxMjE2OSIgZD0iTS0yNTYgMEg3Njh2NTEySC0yNTZ6Ii8+CiAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0tMjU2IDB2NTcuMkw2NTMuNSA1MTJINzY4di01Ny4yTC0xNDEuNSAwSC0yNTZ6TTc2OCAwdjU3LjJMLTE0MS41IDUxMkgtMjU2di01Ny4yTDY1My41IDBINzY4eiIvPgogICAgICA8cGF0aCBmaWxsPSIjZmZmIiBkPSJNMTcwLjcgMHY1MTJoMTcwLjZWMEgxNzAuN3pNLTI1NiAxNzAuN3YxNzAuNkg3NjhWMTcwLjdILTI1NnoiLz4KICAgICAgPHBhdGggZmlsbD0iI2M4MTAyZSIgZD0iTS0yNTYgMjA0Ljh2MTAyLjRINzY4VjIwNC44SC0yNTZ6TTIwNC44IDB2NTEyaDEwMi40VjBIMjA0Ljh6TS0yNTYgNTEyTDg1LjMgMzQxLjNoNzYuNEwtMTc5LjcgNTEySC0yNTZ6bTAtNTEyTDg1LjMgMTcwLjdIOUwtMjU2IDM4LjJWMHptNjA2LjQgMTcwLjdMNjkxLjcgMEg3NjhMNDI2LjcgMTcwLjdoLTc2LjN6TTc2OCA1MTJMNDI2LjcgMzQxLjNINTAzbDI2NSAxMzIuNVY1MTJ6Ii8+CiAgICA8L2c+CiAgPC9nPgo8L3N2Zz4K);
}
.languages {
  padding: 2em;
  padding-top: 0em;
}
.flag-icon {
  margin-right: 0.5em;
}
.locale-container {
  margin-top: 0.5em;
}
a {
  color: $linkColor;
  text-decoration: none;
}
</style>