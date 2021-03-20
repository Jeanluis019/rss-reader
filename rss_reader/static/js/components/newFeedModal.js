Vue.component('new-feed-modal', {
  props: ['current-user-id'],
  data() {
    return {
      feed: {},
      errorMessages: [],
      isSendingData: false
    }
  },
  created() {
    this.createNewFeedObject();
  },
  template: `
    <div id="add-new-feed-modal" uk-modal>
      <div class="uk-modal-dialog">
        <button class="uk-modal-close-default" type="button" uk-close></button>
        <div class="uk-modal-header">
          <h2 class="uk-modal-title">Add Feed</h2>
        </div>
        <div class="uk-modal-body">
          <p class="uk-text-danger" v-for="message in errorMessages">
            *{{ message }}
          </p>

          <form class="uk-form-stacked" @submit.prevent="addNewFeed">
            <div class="uk-margin">
              <label class="uk-form-label" for="form-stacked-text">Name</label>
              <div class="uk-form-controls">
                <input class="uk-input" id="feed-name" type="text" v-model="feed.name" placeholder="Name">
                <small style="color:gray;">* Leave blank to get default Name from Feed's URL</small>
              </div>
            </div>

            <div class="uk-margin">
              <label class="uk-form-label" for="feed-category">Category</label>
              <div class="uk-form-controls">
                <select class="uk-select" id="feed-category" v-model="feed.category">
                  <option :value="null" selected>News</option>
                </select>
              </div>
            </div>

            <div class="uk-margin">
              <label class="uk-form-label" for="feed-url">Feed URL</label>
              <div class="uk-form-controls">
                <input class="uk-input" id="feed-url" type="url" v-model="feed.url" placeholder="Feed URL" required>
              </div>
            </div>

            <div class="uk-margin-medium-top uk-text-right">
              <button class="uk-button uk-button-default uk-modal-close" type="button">Cancel</button>
              <button type="submit" class="uk-button uk-button-primary" :disabled="isSendingData">
                <span v-show="!isSendingData">Save</span>
                <div class="loading-bar" v-show="isSendingData"></div>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  `,
  methods: {
    createNewFeedObject() {
      this.errorMessages = [];
      this.feed = {
        user: this.currentUserId,
        name: null,
        category: null,
        url: null
      }
    },
    addNewFeed() {
      this.errorMessages = [];

      if (!this.isSendingData) {
        this.isSendingData = true;

        this.$http.post('/api/feeds/', this.feed).then((response) => {
          this.isSendingData = false;

          if (response.ok) {
            this.$emit('feed:add', response.data);
            UIkit.modal('#add-new-feed-modal').hide();
            UIkit.notification({message: 'Feed added!', status: 'primary'});

            this.createNewFeedObject();
          }
        }).catch((response) => {
          this.isSendingData = false;
          for (let k in response.data) {
            for (let v of response.data[k]) this.errorMessages.push(v);
          }
        });
      }
    }
  }
});