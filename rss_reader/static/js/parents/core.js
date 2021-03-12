Vue.http.headers.common['X-CSRFToken'] = token;

new Vue({
  el: '#core-page',
  delimiters: ['${','}'],
  data: {
    currentUser: null
  },
  created() {
    this.$http.get('/api/users/me/').then((response) => {
      console.log('USER ->', response.data);
      this.currentUser = response.data;
    });
  }
})