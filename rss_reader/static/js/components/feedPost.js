Vue.component('feed-post', {
  props: ['post'],
  template: `
    <div class="feed-post">
      <div class="uk-card uk-card-default uk-card-body" @click="readPost">
        <h4 class="">{{ post.title }}</h4>
        <p v-html="formatPostSummary()"></p>
      </div>
    </div>
  `,
  methods: {
    formatPostSummary() {
      return this.post.summary.slice(0, 150) + '...';
    },
    readPost() {
      // Select the current post so the modal can get it
      this.$emit('read-post', this.post.id);
    }
  }
});