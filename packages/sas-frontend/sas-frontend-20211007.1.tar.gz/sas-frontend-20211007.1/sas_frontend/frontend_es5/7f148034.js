"use strict";(self.webpackChunksas_frontend=self.webpackChunksas_frontend||[]).push([[2958],{2958:function(e,n,r){r.r(n);r(30879);var t,o=r(50856),i=r(28426),a=(r(98762),r(22098),r(60010),r(11052)),s=r(1265);r(3426);function l(e){return l="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},l(e)}function c(e,n){if(!(e instanceof n))throw new TypeError("Cannot call a class as a function")}function u(e,n){for(var r=0;r<n.length;r++){var t=n[r];t.enumerable=t.enumerable||!1,t.configurable=!0,"value"in t&&(t.writable=!0),Object.defineProperty(e,t.key,t)}}function f(e,n){return f=Object.setPrototypeOf||function(e,n){return e.__proto__=n,e},f(e,n)}function p(e){var n=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var r,t=y(e);if(n){var o=y(this).constructor;r=Reflect.construct(t,arguments,o)}else r=t.apply(this,arguments);return d(this,r)}}function d(e,n){if(n&&("object"===l(n)||"function"==typeof n))return n;if(void 0!==n)throw new TypeError("Derived constructors may only return object or undefined");return function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e)}function y(e){return y=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},y(e)}var h=function(e){!function(e,n){if("function"!=typeof n&&null!==n)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(n&&n.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),n&&f(e,n)}(s,e);var n,r,i,a=p(s);function s(){return c(this,s),a.apply(this,arguments)}return n=s,i=[{key:"template",get:function(){return(0,o.d)(t||(e=['\n      <style include="iron-flex ha-style">\n        .content {\n          padding-bottom: 24px;\n        }\n\n        ha-card {\n          max-width: 600px;\n          margin: 0 auto;\n          margin-top: 24px;\n        }\n        h1 {\n          @apply --paper-font-headline;\n          margin: 0;\n        }\n        .error {\n          color: var(--error-color);\n        }\n        .card-actions {\n          display: flex;\n          justify-content: space-between;\n          align-items: center;\n        }\n        .card-actions a {\n          color: var(--primary-text-color);\n        }\n        [hidden] {\n          display: none;\n        }\n      </style>\n      <hass-subpage\n        hass="[[hass]]"\n        narrow="[[narrow]]"\n        header="[[localize(\'ui.panel.config.cloud.forgot_password.title\')]]"\n      >\n        <div class="content">\n          <ha-card\n            header="[[localize(\'ui.panel.config.cloud.forgot_password.subtitle\')]]"\n          >\n            <div class="card-content">\n              <p>\n                [[localize(\'ui.panel.config.cloud.forgot_password.instructions\')]]\n              </p>\n              <div class="error" hidden$="[[!_error]]">[[_error]]</div>\n              <paper-input\n                autofocus=""\n                id="email"\n                label="[[localize(\'ui.panel.config.cloud.forgot_password.email\')]]"\n                value="{{email}}"\n                type="email"\n                on-keydown="_keyDown"\n                error-message="[[localize(\'ui.panel.config.cloud.forgot_password.email_error_msg\')]]"\n              ></paper-input>\n            </div>\n            <div class="card-actions">\n              <ha-progress-button\n                on-click="_handleEmailPasswordReset"\n                progress="[[_requestInProgress]]"\n                >[[localize(\'ui.panel.config.cloud.forgot_password.send_reset_email\')]]</ha-progress-button\n              >\n            </div>\n          </ha-card>\n        </div>\n      </hass-subpage>\n    '],n||(n=e.slice(0)),t=Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(n)}}))));var e,n}},{key:"properties",get:function(){return{hass:Object,narrow:Boolean,email:{type:String,notify:!0,observer:"_emailChanged"},_requestInProgress:{type:Boolean,value:!1},_error:{type:String,value:""}}}}],(r=[{key:"_emailChanged",value:function(){this._error="",this.$.email.invalid=!1}},{key:"_keyDown",value:function(e){13===e.keyCode&&(this._handleEmailPasswordReset(),e.preventDefault())}},{key:"_handleEmailPasswordReset",value:function(){var e=this;this.email&&this.email.includes("@")||(this.$.email.invalid=!0),this.$.email.invalid||(this._requestInProgress=!0,this.hass.callApi("post","cloud/forgot_password",{email:this.email}).then((function(){e._requestInProgress=!1,e.fire("cloud-done",{flashMessage:e.hass.localize("ui.panel.config.cloud.forgot_password.check_your_email")})}),(function(n){return e.setProperties({_requestInProgress:!1,_error:n&&n.body&&n.body.message?n.body.message:"Unknown error"})})))}}])&&u(n.prototype,r),i&&u(n,i),s}((0,s.Z)((0,a.I)(i.H3)));customElements.define("cloud-forgot-password",h)}}]);