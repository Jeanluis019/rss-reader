Vue.component('feed-post', {
  props: ['post', 'feed-name'],
  template: `
    <div class="feed-post">
      <div class="uk-card uk-card-default">
        <div class="feed-name-badge uk-card-badge uk-label">{{ feedName }}</div>

        <div class="uk-card-body" @click="readPost">
          <h4 class="post-title uk-text-bold">{{ post.title }}</h4>
          <p class="uk-margin-top" v-html="formatPostSummary()"></p>
        </div>
        <div class="uk-card-footer">
          <span style="color: #333;">Autor:</span>
          <span>{{ post.author }}</span>
        </div>
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