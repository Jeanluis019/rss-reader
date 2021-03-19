Vue.http.headers.common['X-CSRFToken'] = token;

new Vue({
  el: '#core-page',
  delimiters: ['${','}'],
  data: {
    currentUser: null,
    subscribedFeeds: [],
    subscribedFeedsFetched: false,
    selectedFeed: {},
    selectedPost: null
  },
  created() {
    this.getCurrentUser();
    this.getSubscribedFeeds();
  },
  methods: {
    getCurrentUser() {
      this.$http.get('/api/users/me/').then((response) => {
        this.currentUser = response.data;
      });
    },
    getSubscribedFeeds() {
      this.$http.get('/api/feeds/').then((response) => {
        this.subscribedFeeds = response.data;
        // Select the first feed by default
        if (this.subscribedFeeds.length > 0) {
          this.selectFeed(this.subscribedFeeds[0].id);
        }
        this.subscribedFeedsFetched = true;
      });
    },
    selectFeed(feedId) {
      this.selectedFeed = this.subscribedFeeds.find(feed => feed.id === feedId);
    },
    selectPostToRead(postId) {
      this.selectedPost = this.selectedFeed.posts.find(post => post.id === postId);
      
      // Wait until the modal is displayed
      setTimeout(() => {
        UIkit.modal('#read-post-modal').show();
      }, 100);
    },
    addFeed(feed) {
      this.subscribedFeeds.push(feed);
      this.selectFeed(feed.id);
    }
  }
})