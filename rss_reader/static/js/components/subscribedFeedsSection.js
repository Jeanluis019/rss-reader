Vue.component('subscribed-feeds-section', {
  props: ['subscribed-feeds', 'selected-feed-id'],
  template: `
    <section class="subscribed-feeds-section">
      <h2 class="uk-margin-top-remove uk-margin-small-bottom">Subscribed Feeds</h2>

      <div class="subscribed-feeds-list">
        <label
          class="subscribed-feed"
          :class="{'active': isSelectedFeed(feed.id)}"
          v-for="feed in subscribedFeeds"
          @click="getFeedPosts(feed.id)"
        >
          {{ feed.name }}
        </label>
      </div>
    </section>
  `,
  methods: {
    isSelectedFeed(feedId) {
      return this.selectedFeedId == feedId;
    },
    getFeedPosts(feedId) {
      this.$emit('get-feed-posts', feedId);
    }
  }
});