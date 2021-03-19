Vue.component('read-post-modal', {
  props: ['post'],
  template: `
    <div id="read-post-modal" class="uk-modal-full" uk-modal>
      <div class="uk-modal-dialog">
        <button class="uk-modal-close-full uk-close-large" type="button" uk-close></button>

        <div class="uk-width-2-3@m uk-width-1-2@l uk-padding-large uk-padding-remove-top uk-margin-auto" uk-height-viewport>
          <h1 class="uk-text-bold" v-html="post.title"></h1>
          <div v-if="post.content" v-html="post.content[0].value"></div>
          <a v-else :href="post.link" target="_blank" class="uk-button uk-button-text">Read more</a>
        </div>
      </div>
    </div>
  `
});