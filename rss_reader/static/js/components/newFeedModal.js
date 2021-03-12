Vue.component('new-feed-modal', {
  data() {
    return {
      name: null,
      category: null,
      url: null
    }
  },
  template: `
    <div id="add-new-feed-modal" uk-modal>
      <div class="uk-modal-dialog">
        <button class="uk-modal-close-default" type="button" uk-close></button>
        <div class="uk-modal-header">
          <h2 class="uk-modal-title">Add Feed</h2>
        </div>
        <div class="uk-modal-body">
          <form class="uk-form-stacked" @submit.prevent="addNewFeed">
            <div class="uk-margin">
              <label class="uk-form-label" for="form-stacked-text">Name</label>
              <div class="uk-form-controls">
                <input class="uk-input" id="feed-name" type="text" v-model="name" placeholder="Name" required>
              </div>
            </div>

            <div class="uk-margin">
              <label class="uk-form-label" for="feed-category">Category</label>
              <div class="uk-form-controls">
                <select class="uk-select" id="feed-category" v-model="category">
                  <option :value="null">Ninguna</option>
                </select>
              </div>
            </div>

            <div class="uk-margin">
              <label class="uk-form-label" for="feed-url">Feed URL</label>
              <div class="uk-form-controls">
                <input class="uk-input" id="feed-url" type="url" v-model="url" placeholder="Feed URL" required>
              </div>
            </div>

            <div class="uk-margin-medium-top uk-text-right">
              <button class="uk-button uk-button-default uk-modal-close" type="button">Cancel</button>
              <button type="submit" class="uk-button uk-button-primary">Save</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  `,
  methods: {
    addNewFeed() {
      let data = {
        user: currentUserId,
        name: this.name,
        category: this.category,
        url: this.url
      }
      console.log('DAT TO SEND ->', data);
      this.$http.post('/api/feeds/', data).then((response) => {
        console.log('SDSD ->', response.data);
      });
    }
  }
});