export default function (error, commit) {
  if (error.response.data) {
    error.message = ''
    for (const key in error.response.data) {
      error.message += ' ' + error.response.data[key]
    }
  } else if (error.message === 'Network Error') {
    error.message = 'Сервер недоступен.'
  }
  commit('setError', error)
}
