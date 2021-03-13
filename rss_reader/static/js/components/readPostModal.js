Vue.component('read-post-modal', {
  props: ['post'],
  template: `
    <div id="read-post-modal" class="uk-modal-full" uk-modal>
      <div class="uk-modal-dialog">
        <button class="uk-modal-close-full uk-close-large" type="button" uk-close></button>

        <div class="uk-width-1-2 uk-padding-large uk-padding-remove-top uk-margin-auto" uk-height-viewport>
          <h1 class="uk-text-bold" v-html="post.title"></h1>
          <div v-html="post.content[0].value"></div>
        </div>
      </div>
    </div>
  `
});