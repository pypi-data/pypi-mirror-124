/*! For license information please see 918aa3f8.js.LICENSE.txt */
"use strict";(self.webpackChunksas_frontend=self.webpackChunksas_frontend||[]).push([[22179],{79332:(e,n,i)=>{i.d(n,{a:()=>t});i(94604);const t={properties:{animationConfig:{type:Object},entryAnimation:{observer:"_entryAnimationChanged",type:String},exitAnimation:{observer:"_exitAnimationChanged",type:String}},_entryAnimationChanged:function(){this.animationConfig=this.animationConfig||{},this.animationConfig.entry=[{name:this.entryAnimation,node:this}]},_exitAnimationChanged:function(){this.animationConfig=this.animationConfig||{},this.animationConfig.exit=[{name:this.exitAnimation,node:this}]},_copyProperties:function(e,n){for(var i in n)e[i]=n[i]},_cloneConfig:function(e){var n={isClone:!0};return this._copyProperties(n,e),n},_getAnimationConfigRecursive:function(e,n,i){var t;if(this.animationConfig)if(this.animationConfig.value&&"function"==typeof this.animationConfig.value)this._warn(this._logf("playAnimation","Please put 'animationConfig' inside of your components 'properties' object instead of outside of it."));else if(t=e?this.animationConfig[e]:this.animationConfig,Array.isArray(t)||(t=[t]),t)for(var o,a=0;o=t[a];a++)if(o.animatable)o.animatable._getAnimationConfigRecursive(o.type||e,n,i);else if(o.id){var s=n[o.id];s?(s.isClone||(n[o.id]=this._cloneConfig(s),s=n[o.id]),this._copyProperties(s,o)):n[o.id]=o}else i.push(o)},getAnimationConfig:function(e){var n={},i=[];for(var t in this._getAnimationConfigRecursive(e,n,i),n)i.push(n[t]);return i}}},96540:(e,n,i)=>{i.d(n,{t:()=>o});i(94604);const t={_configureAnimations:function(e){var n=[],i=[];if(e.length>0)for(let n,t=0;n=e[t];t++){let e=document.createElement(n.name);if(e.isNeonAnimation){let t=null;e.configure||(e.configure=function(e){return null}),t=e.configure(n),i.push({result:t,config:n,neonAnimation:e})}else console.warn(this.is+":",n.name,"not found!")}for(var t=0;t<i.length;t++){let e=i[t].result,o=i[t].config,a=i[t].neonAnimation;try{"function"!=typeof e.cancel&&(e=document.timeline.play(e))}catch(n){e=null,console.warn("Couldnt play","(",o.name,").",n)}e&&n.push({neonAnimation:a,config:o,animation:e})}return n},_shouldComplete:function(e){for(var n=!0,i=0;i<e.length;i++)if("finished"!=e[i].animation.playState){n=!1;break}return n},_complete:function(e){for(var n=0;n<e.length;n++)e[n].neonAnimation.complete(e[n].config);for(n=0;n<e.length;n++)e[n].animation.cancel()},playAnimation:function(e,n){var i=this.getAnimationConfig(e);if(i){this._active=this._active||{},this._active[e]&&(this._complete(this._active[e]),delete this._active[e]);var t=this._configureAnimations(i);if(0!=t.length){this._active[e]=t;for(var o=0;o<t.length;o++)t[o].animation.onfinish=function(){this._shouldComplete(t)&&(this._complete(t),delete this._active[e],this.fire("neon-animation-finish",n,{bubbles:!1}))}.bind(this)}else this.fire("neon-animation-finish",n,{bubbles:!1})}},cancelAnimation:function(){for(var e in this._active){var n=this._active[e];for(var i in n)n[i].animation.cancel()}this._active={}}},o=[i(79332).a,t]},51654:(e,n,i)=>{i.d(n,{Z:()=>a,n:()=>s});i(94604);var t=i(75009),o=i(87156);const a={hostAttributes:{role:"dialog",tabindex:"-1"},properties:{modal:{type:Boolean,value:!1},__readied:{type:Boolean,value:!1}},observers:["_modalChanged(modal, __readied)"],listeners:{tap:"_onDialogClick"},ready:function(){this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.__readied=!0},_modalChanged:function(e,n){n&&(e?(this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.noCancelOnOutsideClick=!0,this.noCancelOnEscKey=!0,this.withBackdrop=!0):(this.noCancelOnOutsideClick=this.noCancelOnOutsideClick&&this.__prevNoCancelOnOutsideClick,this.noCancelOnEscKey=this.noCancelOnEscKey&&this.__prevNoCancelOnEscKey,this.withBackdrop=this.withBackdrop&&this.__prevWithBackdrop))},_updateClosingReasonConfirmed:function(e){this.closingReason=this.closingReason||{},this.closingReason.confirmed=e},_onDialogClick:function(e){for(var n=(0,o.vz)(e).path,i=0,t=n.indexOf(this);i<t;i++){var a=n[i];if(a.hasAttribute&&(a.hasAttribute("dialog-dismiss")||a.hasAttribute("dialog-confirm"))){this._updateClosingReasonConfirmed(a.hasAttribute("dialog-confirm")),this.close(),e.stopPropagation();break}}}},s=[t.$,a]},50808:(e,n,i)=>{i(94604),i(65660),i(1656),i(47686),i(54242);const t=document.createElement("template");t.setAttribute("style","display: none;"),t.innerHTML='<dom-module id="paper-dialog-shared-styles">\n  <template>\n    <style>\n      :host {\n        display: block;\n        margin: 24px 40px;\n\n        background: var(--paper-dialog-background-color, var(--primary-background-color));\n        color: var(--paper-dialog-color, var(--primary-text-color));\n\n        @apply --paper-font-body1;\n        @apply --shadow-elevation-16dp;\n        @apply --paper-dialog;\n      }\n\n      :host > ::slotted(*) {\n        margin-top: 20px;\n        padding: 0 24px;\n      }\n\n      :host > ::slotted(.no-padding) {\n        padding: 0;\n      }\n\n      \n      :host > ::slotted(*:first-child) {\n        margin-top: 24px;\n      }\n\n      :host > ::slotted(*:last-child) {\n        margin-bottom: 24px;\n      }\n\n      /* In 1.x, this selector was `:host > ::content h2`. In 2.x <slot> allows\n      to select direct children only, which increases the weight of this\n      selector, so we have to re-define first-child/last-child margins below. */\n      :host > ::slotted(h2) {\n        position: relative;\n        margin: 0;\n\n        @apply --paper-font-title;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-top. */\n      :host > ::slotted(h2:first-child) {\n        margin-top: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-bottom. */\n      :host > ::slotted(h2:last-child) {\n        margin-bottom: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      :host > ::slotted(.paper-dialog-buttons),\n      :host > ::slotted(.buttons) {\n        position: relative;\n        padding: 8px 8px 8px 24px;\n        margin: 0;\n\n        color: var(--paper-dialog-button-color, var(--primary-color));\n\n        @apply --layout-horizontal;\n        @apply --layout-end-justified;\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(t.content);var o=i(96540),a=i(51654),s=i(9672),l=i(50856);(0,s.k)({_template:l.d`
    <style include="paper-dialog-shared-styles"></style>
    <slot></slot>
`,is:"paper-dialog",behaviors:[a.n,o.t],listeners:{"neon-animation-finish":"_onNeonAnimationFinish"},_renderOpened:function(){this.cancelAnimation(),this.playAnimation("entry")},_renderClosed:function(){this.cancelAnimation(),this.playAnimation("exit")},_onNeonAnimationFinish:function(){this.opened?this._finishRenderOpened():this._finishRenderClosed()}})},28417:(e,n,i)=>{i(50808);var t=i(33367),o=i(93592),a=i(87156);const s={getTabbableNodes:function(e){const n=[];return this._collectTabbableNodes(e,n)?o.H._sortByTabIndex(n):n},_collectTabbableNodes:function(e,n){if(e.nodeType!==Node.ELEMENT_NODE||!o.H._isVisible(e))return!1;const i=e,t=o.H._normalizedTabIndex(i);let s,l=t>0;t>=0&&n.push(i),s="content"===i.localName||"slot"===i.localName?(0,a.vz)(i).getDistributedNodes():(0,a.vz)(i.shadowRoot||i.root||i).children;for(let e=0;e<s.length;e++)l=this._collectTabbableNodes(s[e],n)||l;return l}},l=customElements.get("paper-dialog"),r={get _focusableNodes(){return s.getTabbableNodes(this)}};class d extends((0,t.P)([r],l)){}customElements.define("ha-paper-dialog",d)},22179:(e,n,i)=>{i.r(n);i(53918);var t=i(50856),o=i(28426),a=(i(28417),i(31206),i(1265));i(36436);class s extends((0,a.Z)(o.H3)){static get template(){return t.d`
      <style include="ha-style-dialog">
        .error {
          color: red;
        }
        @media all and (max-width: 500px) {
          ha-paper-dialog {
            margin: 0;
            width: 100%;
            max-height: calc(100% - var(--header-height));

            position: fixed !important;
            bottom: 0px;
            left: 0px;
            right: 0px;
            overflow: scroll;
            border-bottom-left-radius: 0px;
            border-bottom-right-radius: 0px;
          }
        }

        ha-paper-dialog {
          border-radius: 2px;
        }
        ha-paper-dialog p {
          color: var(--secondary-text-color);
        }

        .icon {
          float: right;
        }
      </style>
      <ha-paper-dialog
        id="mp3dialog"
        with-backdrop
        opened="{{_opened}}"
        on-opened-changed="_openedChanged"
      >
        <h2>
          [[localize('ui.panel.mailbox.playback_title')]]
          <div class="icon">
            <template is="dom-if" if="[[_loading]]">
              <ha-circular-progress active></ha-circular-progress>
            </template>
            <ha-icon-button
              id="delicon"
              on-click="openDeleteDialog"
              icon="hass:delete"
            ></ha-icon-button>
          </div>
        </h2>
        <div id="transcribe"></div>
        <div>
          <template is="dom-if" if="[[_errorMsg]]">
            <div class="error">[[_errorMsg]]</div>
          </template>
          <audio id="mp3" preload="none" controls>
            <source id="mp3src" src="" type="audio/mpeg" />
          </audio>
        </div>
      </ha-paper-dialog>
    `}static get properties(){return{hass:Object,_currentMessage:Object,_errorMsg:String,_loading:{type:Boolean,value:!1},_opened:{type:Boolean,value:!1}}}showDialog({hass:e,message:n}){this.hass=e,this._errorMsg=null,this._currentMessage=n,this._opened=!0,this.$.transcribe.innerText=n.message;const i=n.platform,t=this.$.mp3;if(i.has_media){t.style.display="",this._showLoading(!0),t.src=null;const e=`/api/mailbox/media/${i.name}/${n.sha}`;this.hass.fetchWithAuth(e).then((e=>e.ok?e.blob():Promise.reject({status:e.status,statusText:e.statusText}))).then((e=>{this._showLoading(!1),t.src=window.URL.createObjectURL(e),t.play()})).catch((e=>{this._showLoading(!1),this._errorMsg=`Error loading audio: ${e.statusText}`}))}else t.style.display="none",this._showLoading(!1)}openDeleteDialog(){confirm(this.localize("ui.panel.mailbox.delete_prompt"))&&this.deleteSelected()}deleteSelected(){const e=this._currentMessage;this.hass.callApi("DELETE",`mailbox/delete/${e.platform.name}/${e.sha}`),this._dialogDone()}_dialogDone(){this.$.mp3.pause(),this.setProperties({_currentMessage:null,_errorMsg:null,_loading:!1,_opened:!1})}_openedChanged(e){e.detail.value||this._dialogDone()}_showLoading(e){const n=this.$.delicon;if(e)this._loading=!0,n.style.display="none";else{const e=this._currentMessage.platform;this._loading=!1,n.style.display=e.can_delete?"":"none"}}}customElements.define("ha-dialog-show-audio-message",s)},36436:(e,n,i)=>{i(21384);var t=i(11654);const o=document.createElement("template");o.setAttribute("style","display: none;"),o.innerHTML=`<dom-module id="ha-style-dialog">\n<template>\n  <style>\n    ${t.yu.cssText}\n  </style>\n</template>\n</dom-module>`,document.head.appendChild(o.content)}}]);
//# sourceMappingURL=918aa3f8.js.map