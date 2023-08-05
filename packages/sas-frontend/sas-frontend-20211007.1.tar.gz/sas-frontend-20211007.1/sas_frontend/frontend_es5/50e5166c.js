/*! For license information please see 50e5166c.js.LICENSE.txt */
"use strict";(self.webpackChunksas_frontend=self.webpackChunksas_frontend||[]).push([[975],{51654:function(e,t,n){n.d(t,{Z:function(){return i},n:function(){return a}});n(94604);var o=n(75009),r=n(87156),i={hostAttributes:{role:"dialog",tabindex:"-1"},properties:{modal:{type:Boolean,value:!1},__readied:{type:Boolean,value:!1}},observers:["_modalChanged(modal, __readied)"],listeners:{tap:"_onDialogClick"},ready:function(){this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.__readied=!0},_modalChanged:function(e,t){t&&(e?(this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.noCancelOnOutsideClick=!0,this.noCancelOnEscKey=!0,this.withBackdrop=!0):(this.noCancelOnOutsideClick=this.noCancelOnOutsideClick&&this.__prevNoCancelOnOutsideClick,this.noCancelOnEscKey=this.noCancelOnEscKey&&this.__prevNoCancelOnEscKey,this.withBackdrop=this.withBackdrop&&this.__prevWithBackdrop))},_updateClosingReasonConfirmed:function(e){this.closingReason=this.closingReason||{},this.closingReason.confirmed=e},_onDialogClick:function(e){for(var t=(0,r.vz)(e).path,n=0,o=t.indexOf(this);n<o;n++){var i=t[n];if(i.hasAttribute&&(i.hasAttribute("dialog-dismiss")||i.hasAttribute("dialog-confirm"))){this._updateClosingReasonConfirmed(i.hasAttribute("dialog-confirm")),this.close(),e.stopPropagation();break}}}},a=[o.$,i]},22626:function(e,t,n){n(94604),n(65660),n(1656);var o,r,i,a=n(51654),s=n(9672),l=n(50856);(0,s.k)({_template:(0,l.d)(o||(r=['\n    <style>\n\n      :host {\n        display: block;\n        @apply --layout-relative;\n      }\n\n      :host(.is-scrolled:not(:first-child))::before {\n        content: \'\';\n        position: absolute;\n        top: 0;\n        left: 0;\n        right: 0;\n        height: 1px;\n        background: var(--divider-color);\n      }\n\n      :host(.can-scroll:not(.scrolled-to-bottom):not(:last-child))::after {\n        content: \'\';\n        position: absolute;\n        bottom: 0;\n        left: 0;\n        right: 0;\n        height: 1px;\n        background: var(--divider-color);\n      }\n\n      .scrollable {\n        padding: 0 24px;\n\n        @apply --layout-scroll;\n        @apply --paper-dialog-scrollable;\n      }\n\n      .fit {\n        @apply --layout-fit;\n      }\n    </style>\n\n    <div id="scrollable" class="scrollable" on-scroll="updateScrollState">\n      <slot></slot>\n    </div>\n'],i||(i=r.slice(0)),o=Object.freeze(Object.defineProperties(r,{raw:{value:Object.freeze(i)}})))),is:"paper-dialog-scrollable",properties:{dialogElement:{type:Object}},get scrollTarget(){return this.$.scrollable},ready:function(){this._ensureTarget(),this.classList.add("no-padding")},attached:function(){this._ensureTarget(),requestAnimationFrame(this.updateScrollState.bind(this))},updateScrollState:function(){this.toggleClass("is-scrolled",this.scrollTarget.scrollTop>0),this.toggleClass("can-scroll",this.scrollTarget.offsetHeight<this.scrollTarget.scrollHeight),this.toggleClass("scrolled-to-bottom",this.scrollTarget.scrollTop+this.scrollTarget.offsetHeight>=this.scrollTarget.scrollHeight)},_ensureTarget:function(){this.dialogElement=this.dialogElement||this.parentElement,this.dialogElement&&this.dialogElement.behaviors&&this.dialogElement.behaviors.indexOf(a.Z)>=0?(this.dialogElement.sizingTarget=this.scrollTarget,this.scrollTarget.classList.remove("fit")):this.dialogElement&&this.scrollTarget.classList.add("fit")}})},50808:function(e,t,n){n(94604),n(65660),n(1656),n(47686),n(54242);var o=document.createElement("template");o.setAttribute("style","display: none;"),o.innerHTML='<dom-module id="paper-dialog-shared-styles">\n  <template>\n    <style>\n      :host {\n        display: block;\n        margin: 24px 40px;\n\n        background: var(--paper-dialog-background-color, var(--primary-background-color));\n        color: var(--paper-dialog-color, var(--primary-text-color));\n\n        @apply --paper-font-body1;\n        @apply --shadow-elevation-16dp;\n        @apply --paper-dialog;\n      }\n\n      :host > ::slotted(*) {\n        margin-top: 20px;\n        padding: 0 24px;\n      }\n\n      :host > ::slotted(.no-padding) {\n        padding: 0;\n      }\n\n      \n      :host > ::slotted(*:first-child) {\n        margin-top: 24px;\n      }\n\n      :host > ::slotted(*:last-child) {\n        margin-bottom: 24px;\n      }\n\n      /* In 1.x, this selector was `:host > ::content h2`. In 2.x <slot> allows\n      to select direct children only, which increases the weight of this\n      selector, so we have to re-define first-child/last-child margins below. */\n      :host > ::slotted(h2) {\n        position: relative;\n        margin: 0;\n\n        @apply --paper-font-title;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-top. */\n      :host > ::slotted(h2:first-child) {\n        margin-top: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-bottom. */\n      :host > ::slotted(h2:last-child) {\n        margin-bottom: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      :host > ::slotted(.paper-dialog-buttons),\n      :host > ::slotted(.buttons) {\n        position: relative;\n        padding: 8px 8px 8px 24px;\n        margin: 0;\n\n        color: var(--paper-dialog-button-color, var(--primary-color));\n\n        @apply --layout-horizontal;\n        @apply --layout-end-justified;\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(o.content);var r,i,a,s=n(96540),l=n(51654),c=n(9672),u=n(50856);(0,c.k)({_template:(0,u.d)(r||(i=['\n    <style include="paper-dialog-shared-styles"></style>\n    <slot></slot>\n'],a||(a=i.slice(0)),r=Object.freeze(Object.defineProperties(i,{raw:{value:Object.freeze(a)}})))),is:"paper-dialog",behaviors:[l.n,s.t],listeners:{"neon-animation-finish":"_onNeonAnimationFinish"},_renderOpened:function(){this.cancelAnimation(),this.playAnimation("entry")},_renderClosed:function(){this.cancelAnimation(),this.playAnimation("exit")},_onNeonAnimationFinish:function(){this.opened?this._finishRenderOpened():this._finishRenderClosed()}})},28417:function(e,t,n){n(50808);var o=n(33367),r=n(93592),i=n(87156),a={getTabbableNodes:function(e){var t=[];return this._collectTabbableNodes(e,t)?r.H._sortByTabIndex(t):t},_collectTabbableNodes:function(e,t){if(e.nodeType!==Node.ELEMENT_NODE||!r.H._isVisible(e))return!1;var n,o=e,a=r.H._normalizedTabIndex(o),s=a>0;a>=0&&t.push(o),n="content"===o.localName||"slot"===o.localName?(0,i.vz)(o).getDistributedNodes():(0,i.vz)(o.shadowRoot||o.root||o).children;for(var l=0;l<n.length;l++)s=this._collectTabbableNodes(n[l],t)||s;return s}};function s(e){return s="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},s(e)}function l(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function c(e,t){return c=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},c(e,t)}function u(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,o=p(e);if(t){var r=p(this).constructor;n=Reflect.construct(o,arguments,r)}else n=o.apply(this,arguments);return d(this,n)}}function d(e,t){if(t&&("object"===s(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e)}function p(e){return p=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},p(e)}var f=customElements.get("paper-dialog"),h={get _focusableNodes(){return a.getTabbableNodes(this)}},m=function(e){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&c(e,t)}(n,e);var t=u(n);function n(){return l(this,n),t.apply(this,arguments)}return n}((0,o.P)([h],f));customElements.define("ha-paper-dialog",m)},70975:function(e,t,n){n.r(t),n.d(t,{DialogManageCloudhook:function(){return j}});n(53918),n(22626),n(30879);var o,r,i,a,s,l=n(7599),c=n(17717),u=(n(28417),n(26765)),d=n(11654),p=n(27322);function f(e){return f="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},f(e)}function h(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function m(e,t,n,o,r,i,a){try{var s=e[i](a),l=s.value}catch(c){return void n(c)}s.done?t(l):Promise.resolve(l).then(o,r)}function y(e){return function(){var t=this,n=arguments;return new Promise((function(o,r){var i=e.apply(t,n);function a(e){m(i,o,r,a,s,"next",e)}function s(e){m(i,o,r,a,s,"throw",e)}a(void 0)}))}}function g(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function b(e,t){return b=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},b(e,t)}function v(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,o=_(e);if(t){var r=_(this).constructor;n=Reflect.construct(o,arguments,r)}else n=o.apply(this,arguments);return k(this,n)}}function k(e,t){if(t&&("object"===f(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return w(e)}function w(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function _(e){return _=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},_(e)}function E(){E=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(n){t.forEach((function(t){t.kind===n&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var n=e.prototype;["method","field"].forEach((function(o){t.forEach((function(t){var r=t.placement;if(t.kind===o&&("static"===r||"prototype"===r)){var i="static"===r?e:n;this.defineClassElement(i,t)}}),this)}),this)},defineClassElement:function(e,t){var n=t.descriptor;if("field"===t.kind){var o=t.initializer;n={enumerable:n.enumerable,writable:n.writable,configurable:n.configurable,value:void 0===o?void 0:o.call(e)}}Object.defineProperty(e,t.key,n)},decorateClass:function(e,t){var n=[],o=[],r={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,r)}),this),e.forEach((function(e){if(!x(e))return n.push(e);var t=this.decorateElement(e,r);n.push(t.element),n.push.apply(n,t.extras),o.push.apply(o,t.finishers)}),this),!t)return{elements:n,finishers:o};var i=this.decorateConstructor(n,t);return o.push.apply(o,i.finishers),i.finishers=o,i},addElementPlacement:function(e,t,n){var o=t[e.placement];if(!n&&-1!==o.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");o.push(e.key)},decorateElement:function(e,t){for(var n=[],o=[],r=e.decorators,i=r.length-1;i>=0;i--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,r[i])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&o.push(l.finisher);var c=l.extras;if(c){for(var u=0;u<c.length;u++)this.addElementPlacement(c[u],t);n.push.apply(n,c)}}return{element:e,finishers:o,extras:n}},decorateConstructor:function(e,t){for(var n=[],o=t.length-1;o>=0;o--){var r=this.fromClassDescriptor(e),i=this.toClassDescriptor((0,t[o])(r)||r);if(void 0!==i.finisher&&n.push(i.finisher),void 0!==i.elements){e=i.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:n}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return z(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?z(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var n=S(e.key),o=String(e.placement);if("static"!==o&&"prototype"!==o&&"own"!==o)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+o+'"');var r=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var i={kind:t,key:n,placement:o,descriptor:Object.assign({},r)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(r,"get","The property descriptor of a field descriptor"),this.disallowProperty(r,"set","The property descriptor of a field descriptor"),this.disallowProperty(r,"value","The property descriptor of a field descriptor"),i.initializer=e.initializer),i},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:P(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var n=P(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:n}},runClassFinishers:function(e,t){for(var n=0;n<t.length;n++){var o=(0,t[n])(e);if(void 0!==o){if("function"!=typeof o)throw new TypeError("Finishers must return a constructor.");e=o}}return e},disallowProperty:function(e,t,n){if(void 0!==e[t])throw new TypeError(n+" can't have a ."+t+" property.")}};return e}function O(e){var t,n=S(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var o={kind:"field"===e.kind?"field":"method",key:n,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(o.decorators=e.decorators),"field"===e.kind&&(o.initializer=e.value),o}function C(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function x(e){return e.decorators&&e.decorators.length}function T(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function P(e,t){var n=e[t];if(void 0!==n&&"function"!=typeof n)throw new TypeError("Expected '"+t+"' to be a function");return n}function S(e){var t=function(e,t){if("object"!==f(e)||null===e)return e;var n=e[Symbol.toPrimitive];if(void 0!==n){var o=n.call(e,t||"default");if("object"!==f(o))return o;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===f(t)?t:String(t)}function z(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,o=new Array(t);n<t;n++)o[n]=e[n];return o}var A="Public URL – Click to copy to clipboard",j=function(e,t,n,o){var r=E();if(o)for(var i=0;i<o.length;i++)r=o[i](r);var a=t((function(e){r.initializeInstanceElements(e,s.elements)}),n),s=r.decorateClass(function(e){for(var t=[],n=function(e){return"method"===e.kind&&e.key===i.key&&e.placement===i.placement},o=0;o<e.length;o++){var r,i=e[o];if("method"===i.kind&&(r=t.find(n)))if(T(i.descriptor)||T(r.descriptor)){if(x(i)||x(r))throw new ReferenceError("Duplicated methods ("+i.key+") can't be decorated.");r.descriptor=i.descriptor}else{if(x(i)){if(x(r))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+i.key+").");r.decorators=i.decorators}C(i,r)}else t.push(i)}return t}(a.d.map(O)),e);return r.initializeClassElements(a.F,s.elements),r.runClassFinishers(a.F,s.finishers)}(null,(function(e,t){var n,f,m=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&b(e,t)}(o,t);var n=v(o);function o(){var t;g(this,o);for(var r=arguments.length,i=new Array(r),a=0;a<r;a++)i[a]=arguments[a];return t=n.call.apply(n,[this].concat(i)),e(w(t)),t}return o}(t);return{F:m,d:[{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[(0,c.S)()],key:"_params",value:void 0},{kind:"method",key:"showDialog",value:(f=y(regeneratorRuntime.mark((function e(t){return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return this._params=t,e.next=3,this.updateComplete;case 3:this._dialog.open();case 4:case"end":return e.stop()}}),e,this)}))),function(e){return f.apply(this,arguments)})},{kind:"method",key:"render",value:function(){if(!this._params)return(0,l.dy)(o||(o=h([""])));var e=this._params,t=e.webhook,n=e.cloudhook,s="automation"===t.domain?(0,p.R)(this.hass,"/docs/automation/trigger/#webhook-trigger"):(0,p.R)(this.hass,"/integrations/".concat(t.domain,"/"));return(0,l.dy)(r||(r=h(["\n      <ha-paper-dialog with-backdrop>\n        <h2>\n          ","\n        </h2>\n        <div>\n          <p>\n            ","\n          </p>\n          <paper-input\n            label=","\n            value=","\n            @click=","\n            @blur=","\n          ></paper-input>\n          <p>\n            ",'\n          </p>\n        </div>\n\n        <div class="paper-dialog-buttons">\n          <a href=',' target="_blank" rel="noreferrer">\n            <mwc-button\n              >',"</mwc-button\n            >\n          </a>\n          <mwc-button @click=","\n            >","</mwc-button\n          >\n        </div>\n      </ha-paper-dialog>\n    "])),this.hass.localize("ui.panel.config.cloud.dialog_cloudhook.webhook_for","name",t.name),this.hass.localize("ui.panel.config.cloud.dialog_cloudhook.available_at"),A,n.cloudhook_url,this._copyClipboard,this._restoreLabel,n.managed?(0,l.dy)(i||(i=h(["\n                  ","\n                "])),this.hass.localize("ui.panel.config.cloud.dialog_cloudhook.managed_by_integration")):(0,l.dy)(a||(a=h(["\n                  ",'\n                  <button class="link" @click=',">\n                    ","</button\n                  >.\n                "])),this.hass.localize("ui.panel.config.cloud.dialog_cloudhook.info_disable_webhook"),this._disableWebhook,this.hass.localize("ui.panel.config.cloud.dialog_cloudhook.link_disable_webhook")),s,this.hass.localize("ui.panel.config.cloud.dialog_cloudhook.view_documentation"),this._closeDialog,this.hass.localize("ui.panel.config.cloud.dialog_cloudhook.close"))}},{kind:"get",key:"_dialog",value:function(){return this.shadowRoot.querySelector("ha-paper-dialog")}},{kind:"get",key:"_paperInput",value:function(){return this.shadowRoot.querySelector("paper-input")}},{kind:"method",key:"_closeDialog",value:function(){this._dialog.close()}},{kind:"method",key:"_disableWebhook",value:(n=y(regeneratorRuntime.mark((function e(){var t=this;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:(0,u.g7)(this,{text:this.hass.localize("ui.panel.config.cloud.dialog_cloudhook.confirm_disable"),dismissText:this.hass.localize("ui.common.cancel"),confirmText:this.hass.localize("ui.common.disable"),confirm:function(){t._params.disableHook(),t._closeDialog()}});case 1:case"end":return e.stop()}}),e,this)}))),function(){return n.apply(this,arguments)})},{kind:"method",key:"_copyClipboard",value:function(e){var t=e.currentTarget,n=t.inputElement.inputElement;n.setSelectionRange(0,n.value.length);try{document.execCommand("copy"),t.label=this.hass.localize("ui.panel.config.cloud.dialog_cloudhook.copied_to_clipboard")}catch(o){}}},{kind:"method",key:"_restoreLabel",value:function(){this._paperInput.label=A}},{kind:"get",static:!0,key:"styles",value:function(){return[d.Qx,(0,l.iv)(s||(s=h(["\n        ha-paper-dialog {\n          width: 650px;\n        }\n        paper-input {\n          margin-top: -8px;\n        }\n        button.link {\n          color: var(--primary-color);\n        }\n        .paper-dialog-buttons a {\n          text-decoration: none;\n        }\n      "])))]}}]}}),l.oi);customElements.define("dialog-manage-cloudhook",j)},27322:function(e,t,n){n.d(t,{R:function(){return o}});var o=function(e,t){return"https://".concat(e.config.version.includes("b")?"rc":e.config.version.includes("dev")?"next":"www",".smartautomatic.duckdns.org:8091").concat(t)}}}]);