Vue.component('subscribed-feeds-section', {
  props: ['subscribed-feeds', 'selected-feed-id'],
  template: `
    <section class="subscribed-feeds-section">
      <div class="uk-child-width-1-1 uk-child-width-1-2@s" uk-grid>
        <div><h2 class="uk-margin-top-remove uk-margin-small-bottom">Subscribed Feeds</h2></div>
        <div class="uk-text-right uk-visible@s">
          <a class="uk-button uk-button-primary" href="#add-new-feed-modal" uk-toggle>
            + Add new Feed
          </a>
        </div>
      </div>

      <div class="subscribed-feeds-list uk-width-1-1">
        <label
          class="subscribed-feed"
          :class="{'active': isSelectedFeed(feed.id)}"
          v-for="feed in subscribedFeeds"
          @click="getFeedPosts(feed.id)"
        >
          {{ feed.name }}
        </label>
      </div>

      <a class="uk-button uk-button-primary uk-width-1-1 uk-margin-top uk-hidden@s"
        href="#add-new-feed-modal" uk-toggle
      >
        + Add new Feed
      </a>
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