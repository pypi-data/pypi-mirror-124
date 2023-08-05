/*! For license information please see ef49bbd1.js.LICENSE.txt */
"use strict";(self.webpackChunksas_frontend=self.webpackChunksas_frontend||[]).push([[5683],{54930:function(e,r,t){t.d(r,{D:function(){return D}});var n,o,i,c,a=t(87480),s=t(32207),l=t(38103),u=t(59685),p=t(88668),d=t(84298);function f(e){return f="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},f(e)}function m(e,r){return r||(r=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(r)}}))}function y(e,r){if(!(e instanceof r))throw new TypeError("Cannot call a class as a function")}function h(e,r){for(var t=0;t<r.length;t++){var n=r[t];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(e,n.key,n)}}function b(e,r,t){return b="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,r,t){var n=function(e,r){for(;!Object.prototype.hasOwnProperty.call(e,r)&&null!==(e=w(e)););return e}(e,r);if(n){var o=Object.getOwnPropertyDescriptor(n,r);return o.get?o.get.call(t):o.value}},b(e,r,t||e)}function g(e,r){return g=Object.setPrototypeOf||function(e,r){return e.__proto__=r,e},g(e,r)}function _(e){var r=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var t,n=w(e);if(r){var o=w(this).constructor;t=Reflect.construct(n,arguments,o)}else t=n.apply(this,arguments);return v(this,t)}}function v(e,r){if(r&&("object"===f(r)||"function"==typeof r))return r;if(void 0!==r)throw new TypeError("Derived constructors may only return object or undefined");return function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e)}function w(e){return w=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},w(e)}var k,O=function(e){!function(e,r){if("function"!=typeof r&&null!==r)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(r&&r.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),r&&g(e,r)}(f,e);var r,t,a,l=_(f);function f(){var e;return y(this,f),(e=l.apply(this,arguments)).indeterminate=!1,e.progress=0,e.density=0,e.closed=!1,e}return r=f,t=[{key:"open",value:function(){this.closed=!1}},{key:"close",value:function(){this.closed=!0}},{key:"render",value:function(){var e={"mdc-circular-progress--closed":this.closed,"mdc-circular-progress--indeterminate":this.indeterminate},r=48+4*this.density,t={width:"".concat(r,"px"),height:"".concat(r,"px")};return(0,s.dy)(n||(n=m(['\n      <div\n        class="mdc-circular-progress ','"\n        style="','"\n        role="progressbar"\n        aria-label="','"\n        aria-valuemin="0"\n        aria-valuemax="1"\n        aria-valuenow="','">\n        ',"\n        ","\n      </div>"])),(0,u.$)(e),(0,d.V)(t),(0,p.o)(this.ariaLabel),(0,p.o)(this.indeterminate?void 0:this.progress),this.renderDeterminateContainer(),this.renderIndeterminateContainer())}},{key:"renderDeterminateContainer",value:function(){var e=48+4*this.density,r=e/2,t=this.density>=-3?18+11*this.density/6:12.5+5*(this.density+3)/4,n=6.2831852*t,i=(1-this.progress)*n,c=this.density>=-3?4+this.density*(1/3):3+(this.density+3)*(1/6);return(0,s.dy)(o||(o=m(['\n      <div class="mdc-circular-progress__determinate-container">\n        <svg class="mdc-circular-progress__determinate-circle-graphic"\n             viewBox="0 0 '," ",'">\n          <circle class="mdc-circular-progress__determinate-track"\n                  cx="','" cy="','" r="','"\n                  stroke-width="','"></circle>\n          <circle class="mdc-circular-progress__determinate-circle"\n                  cx="','" cy="','" r="','"\n                  stroke-dasharray="','"\n                  stroke-dashoffset="','"\n                  stroke-width="','"></circle>\n        </svg>\n      </div>'])),e,e,r,r,t,c,r,r,t,6.2831852*t,i,c)}},{key:"renderIndeterminateContainer",value:function(){return(0,s.dy)(i||(i=m(['\n      <div class="mdc-circular-progress__indeterminate-container">\n        <div class="mdc-circular-progress__spinner-layer">\n          ',"\n        </div>\n      </div>"])),this.renderIndeterminateSpinnerLayer())}},{key:"renderIndeterminateSpinnerLayer",value:function(){var e=48+4*this.density,r=e/2,t=this.density>=-3?18+11*this.density/6:12.5+5*(this.density+3)/4,n=6.2831852*t,o=.5*n,i=this.density>=-3?4+this.density*(1/3):3+(this.density+3)*(1/6);return(0,s.dy)(c||(c=m(['\n        <div class="mdc-circular-progress__circle-clipper mdc-circular-progress__circle-left">\n          <svg class="mdc-circular-progress__indeterminate-circle-graphic"\n               viewBox="0 0 '," ",'">\n            <circle cx="','" cy="','" r="','"\n                    stroke-dasharray="','"\n                    stroke-dashoffset="','"\n                    stroke-width="','"></circle>\n          </svg>\n        </div>\n        <div class="mdc-circular-progress__gap-patch">\n          <svg class="mdc-circular-progress__indeterminate-circle-graphic"\n               viewBox="0 0 '," ",'">\n            <circle cx="','" cy="','" r="','"\n                    stroke-dasharray="','"\n                    stroke-dashoffset="','"\n                    stroke-width="','"></circle>\n          </svg>\n        </div>\n        <div class="mdc-circular-progress__circle-clipper mdc-circular-progress__circle-right">\n          <svg class="mdc-circular-progress__indeterminate-circle-graphic"\n               viewBox="0 0 '," ",'">\n            <circle cx="','" cy="','" r="','"\n                    stroke-dasharray="','"\n                    stroke-dashoffset="','"\n                    stroke-width="','"></circle>\n          </svg>\n        </div>'])),e,e,r,r,t,n,o,i,e,e,r,r,t,n,o,.8*i,e,e,r,r,t,n,o,i)}},{key:"update",value:function(e){b(w(f.prototype),"update",this).call(this,e),e.has("progress")&&(this.progress>1&&(this.progress=1),this.progress<0&&(this.progress=0))}}],t&&h(r.prototype,t),a&&h(r,a),f}(s.oi);(0,a.__decorate)([(0,s.Cb)({type:Boolean,reflect:!0})],O.prototype,"indeterminate",void 0),(0,a.__decorate)([(0,s.Cb)({type:Number,reflect:!0})],O.prototype,"progress",void 0),(0,a.__decorate)([(0,s.Cb)({type:Number,reflect:!0})],O.prototype,"density",void 0),(0,a.__decorate)([(0,s.Cb)({type:Boolean,reflect:!0})],O.prototype,"closed",void 0),(0,a.__decorate)([l.L,(0,s.Cb)({type:String,attribute:"aria-label"})],O.prototype,"ariaLabel",void 0);var x,R,j=(0,s.iv)(k||(x=[".mdc-circular-progress__determinate-circle,.mdc-circular-progress__indeterminate-circle-graphic{stroke:#6200ee;stroke:var(--mdc-theme-primary, #6200ee)}.mdc-circular-progress__determinate-track{stroke:transparent}@keyframes mdc-circular-progress-container-rotate{to{transform:rotate(360deg)}}@keyframes mdc-circular-progress-spinner-layer-rotate{12.5%{transform:rotate(135deg)}25%{transform:rotate(270deg)}37.5%{transform:rotate(405deg)}50%{transform:rotate(540deg)}62.5%{transform:rotate(675deg)}75%{transform:rotate(810deg)}87.5%{transform:rotate(945deg)}100%{transform:rotate(1080deg)}}@keyframes mdc-circular-progress-color-1-fade-in-out{from{opacity:.99}25%{opacity:.99}26%{opacity:0}89%{opacity:0}90%{opacity:.99}to{opacity:.99}}@keyframes mdc-circular-progress-color-2-fade-in-out{from{opacity:0}15%{opacity:0}25%{opacity:.99}50%{opacity:.99}51%{opacity:0}to{opacity:0}}@keyframes mdc-circular-progress-color-3-fade-in-out{from{opacity:0}40%{opacity:0}50%{opacity:.99}75%{opacity:.99}76%{opacity:0}to{opacity:0}}@keyframes mdc-circular-progress-color-4-fade-in-out{from{opacity:0}65%{opacity:0}75%{opacity:.99}90%{opacity:.99}to{opacity:0}}@keyframes mdc-circular-progress-left-spin{from{transform:rotate(265deg)}50%{transform:rotate(130deg)}to{transform:rotate(265deg)}}@keyframes mdc-circular-progress-right-spin{from{transform:rotate(-265deg)}50%{transform:rotate(-130deg)}to{transform:rotate(-265deg)}}.mdc-circular-progress{display:inline-flex;position:relative;direction:ltr;line-height:0;transition:opacity 250ms 0ms cubic-bezier(0.4, 0, 0.6, 1)}.mdc-circular-progress__determinate-container,.mdc-circular-progress__indeterminate-circle-graphic,.mdc-circular-progress__indeterminate-container,.mdc-circular-progress__spinner-layer{position:absolute;width:100%;height:100%}.mdc-circular-progress__determinate-container{transform:rotate(-90deg)}.mdc-circular-progress__indeterminate-container{font-size:0;letter-spacing:0;white-space:nowrap;opacity:0}.mdc-circular-progress__determinate-circle-graphic,.mdc-circular-progress__indeterminate-circle-graphic{fill:transparent}.mdc-circular-progress__determinate-circle{transition:stroke-dashoffset 500ms 0ms cubic-bezier(0, 0, 0.2, 1)}.mdc-circular-progress__gap-patch{position:absolute;top:0;left:47.5%;box-sizing:border-box;width:5%;height:100%;overflow:hidden}.mdc-circular-progress__gap-patch .mdc-circular-progress__indeterminate-circle-graphic{left:-900%;width:2000%;transform:rotate(180deg)}.mdc-circular-progress__circle-clipper{display:inline-flex;position:relative;width:50%;height:100%;overflow:hidden}.mdc-circular-progress__circle-clipper .mdc-circular-progress__indeterminate-circle-graphic{width:200%}.mdc-circular-progress__circle-right .mdc-circular-progress__indeterminate-circle-graphic{left:-100%}.mdc-circular-progress--indeterminate .mdc-circular-progress__determinate-container{opacity:0}.mdc-circular-progress--indeterminate .mdc-circular-progress__indeterminate-container{opacity:1}.mdc-circular-progress--indeterminate .mdc-circular-progress__indeterminate-container{animation:mdc-circular-progress-container-rotate 1568.2352941176ms linear infinite}.mdc-circular-progress--indeterminate .mdc-circular-progress__spinner-layer{animation:mdc-circular-progress-spinner-layer-rotate 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--indeterminate .mdc-circular-progress__color-1{animation:mdc-circular-progress-spinner-layer-rotate 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both,mdc-circular-progress-color-1-fade-in-out 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--indeterminate .mdc-circular-progress__color-2{animation:mdc-circular-progress-spinner-layer-rotate 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both,mdc-circular-progress-color-2-fade-in-out 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--indeterminate .mdc-circular-progress__color-3{animation:mdc-circular-progress-spinner-layer-rotate 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both,mdc-circular-progress-color-3-fade-in-out 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--indeterminate .mdc-circular-progress__color-4{animation:mdc-circular-progress-spinner-layer-rotate 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both,mdc-circular-progress-color-4-fade-in-out 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--indeterminate .mdc-circular-progress__circle-left .mdc-circular-progress__indeterminate-circle-graphic{animation:mdc-circular-progress-left-spin 1333ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--indeterminate .mdc-circular-progress__circle-right .mdc-circular-progress__indeterminate-circle-graphic{animation:mdc-circular-progress-right-spin 1333ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--closed{opacity:0}:host{display:inline-flex}.mdc-circular-progress__determinate-track{stroke:transparent;stroke:var(--mdc-circular-progress-track-color, transparent)}"],R||(R=x.slice(0)),k=Object.freeze(Object.defineProperties(x,{raw:{value:Object.freeze(R)}}))));function z(e){return z="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},z(e)}function S(e,r){if(!(e instanceof r))throw new TypeError("Cannot call a class as a function")}function P(e,r){return P=Object.setPrototypeOf||function(e,r){return e.__proto__=r,e},P(e,r)}function E(e){var r=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var t,n=B(e);if(r){var o=B(this).constructor;t=Reflect.construct(n,arguments,o)}else t=n.apply(this,arguments);return C(this,t)}}function C(e,r){if(r&&("object"===z(r)||"function"==typeof r))return r;if(void 0!==r)throw new TypeError("Derived constructors may only return object or undefined");return function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e)}function B(e){return B=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},B(e)}var D=function(e){!function(e,r){if("function"!=typeof r&&null!==r)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(r&&r.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),r&&P(e,r)}(t,e);var r=E(t);function t(){return S(this,t),r.apply(this,arguments)}return t}(O);D.styles=[j],D=(0,a.__decorate)([(0,s.Mo)("mwc-circular-progress")],D)},68646:function(e,r,t){t.d(r,{B:function(){return g}});var n,o,i=t(87480),c=(t(66702),t(38103)),a=t(98734),s=t(32207),l=t(88668);function u(e){return u="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},u(e)}function p(e,r){return r||(r=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(r)}}))}function d(e,r){if(!(e instanceof r))throw new TypeError("Cannot call a class as a function")}function f(e,r){for(var t=0;t<r.length;t++){var n=r[t];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(e,n.key,n)}}function m(e,r){return m=Object.setPrototypeOf||function(e,r){return e.__proto__=r,e},m(e,r)}function y(e){var r=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var t,n=b(e);if(r){var o=b(this).constructor;t=Reflect.construct(n,arguments,o)}else t=n.apply(this,arguments);return h(this,t)}}function h(e,r){if(r&&("object"===u(r)||"function"==typeof r))return r;if(void 0!==r)throw new TypeError("Derived constructors may only return object or undefined");return function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e)}function b(e){return b=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},b(e)}var g=function(e){!function(e,r){if("function"!=typeof r&&null!==r)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(r&&r.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),r&&m(e,r)}(u,e);var r,t,i,c=y(u);function u(){var e;return d(this,u),(e=c.apply(this,arguments)).disabled=!1,e.icon="",e.shouldRenderRipple=!1,e.rippleHandlers=new a.A((function(){return e.shouldRenderRipple=!0,e.ripple})),e}return r=u,(t=[{key:"renderRipple",value:function(){return this.shouldRenderRipple?(0,s.dy)(n||(n=p(['\n            <mwc-ripple\n                .disabled="','"\n                unbounded>\n            </mwc-ripple>'])),this.disabled):""}},{key:"focus",value:function(){var e=this.buttonElement;e&&(this.rippleHandlers.startFocus(),e.focus())}},{key:"blur",value:function(){var e=this.buttonElement;e&&(this.rippleHandlers.endFocus(),e.blur())}},{key:"render",value:function(){return(0,s.dy)(o||(o=p(['<button\n        class="mdc-icon-button"\n        aria-label="','"\n        aria-haspopup="','"\n        ?disabled="','"\n        @focus="','"\n        @blur="','"\n        @mousedown="','"\n        @mouseenter="','"\n        @mouseleave="','"\n        @touchstart="','"\n        @touchend="','"\n        @touchcancel="','"\n    >','\n    <i class="material-icons">',"</i>\n    <span\n      ><slot></slot\n    ></span>\n  </button>"])),this.ariaLabel||this.icon,(0,l.o)(this.ariaHasPopup),this.disabled,this.handleRippleFocus,this.handleRippleBlur,this.handleRippleMouseDown,this.handleRippleMouseEnter,this.handleRippleMouseLeave,this.handleRippleTouchStart,this.handleRippleDeactivate,this.handleRippleDeactivate,this.renderRipple(),this.icon)}},{key:"handleRippleMouseDown",value:function(e){var r=this;window.addEventListener("mouseup",(function e(){window.removeEventListener("mouseup",e),r.handleRippleDeactivate()})),this.rippleHandlers.startPress(e)}},{key:"handleRippleTouchStart",value:function(e){this.rippleHandlers.startPress(e)}},{key:"handleRippleDeactivate",value:function(){this.rippleHandlers.endPress()}},{key:"handleRippleMouseEnter",value:function(){this.rippleHandlers.startHover()}},{key:"handleRippleMouseLeave",value:function(){this.rippleHandlers.endHover()}},{key:"handleRippleFocus",value:function(){this.rippleHandlers.startFocus()}},{key:"handleRippleBlur",value:function(){this.rippleHandlers.endFocus()}}])&&f(r.prototype,t),i&&f(r,i),u}(s.oi);(0,i.__decorate)([(0,s.Cb)({type:Boolean,reflect:!0})],g.prototype,"disabled",void 0),(0,i.__decorate)([(0,s.Cb)({type:String})],g.prototype,"icon",void 0),(0,i.__decorate)([c.L,(0,s.Cb)({type:String,attribute:"aria-label"})],g.prototype,"ariaLabel",void 0),(0,i.__decorate)([c.L,(0,s.Cb)({type:String,attribute:"aria-haspopup"})],g.prototype,"ariaHasPopup",void 0),(0,i.__decorate)([(0,s.IO)("button")],g.prototype,"buttonElement",void 0),(0,i.__decorate)([(0,s.GC)("mwc-ripple")],g.prototype,"ripple",void 0),(0,i.__decorate)([(0,s.SB)()],g.prototype,"shouldRenderRipple",void 0),(0,i.__decorate)([(0,s.hO)({passive:!0})],g.prototype,"handleRippleMouseDown",null),(0,i.__decorate)([(0,s.hO)({passive:!0})],g.prototype,"handleRippleTouchStart",null)},90779:function(e,r,t){var n;t.d(r,{W:function(){return c}});var o,i,c=(0,t(32207).iv)(n||(o=['.material-icons{font-family:var(--mdc-icon-font, "Material Icons");font-weight:normal;font-style:normal;font-size:var(--mdc-icon-size, 24px);line-height:1;letter-spacing:normal;text-transform:none;display:inline-block;white-space:nowrap;word-wrap:normal;direction:ltr;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;-moz-osx-font-smoothing:grayscale;font-feature-settings:"liga"}.mdc-icon-button{font-size:24px;width:48px;height:48px;padding:12px}.mdc-icon-button:disabled{color:rgba(0, 0, 0, 0.38);color:var(--mdc-theme-text-disabled-on-light, rgba(0, 0, 0, 0.38))}.mdc-icon-button svg,.mdc-icon-button img{width:24px;height:24px}.mdc-icon-button{display:inline-block;position:relative;box-sizing:border-box;border:none;outline:none;background-color:transparent;fill:currentColor;color:inherit;text-decoration:none;cursor:pointer;user-select:none}.mdc-icon-button .mdc-icon-button__touch{position:absolute;top:50%;height:48px;left:50%;width:48px;transform:translate(-50%, -50%)}.mdc-icon-button:disabled{cursor:default;pointer-events:none}.mdc-icon-button--display-flex{align-items:center;display:inline-flex;justify-content:center}.mdc-icon-button__icon{display:inline-block}.mdc-icon-button__icon.mdc-icon-button__icon--on{display:none}.mdc-icon-button--touch{margin-top:0px;margin-bottom:0px}.mdc-icon-button--on .mdc-icon-button__icon{display:none}.mdc-icon-button--on .mdc-icon-button__icon.mdc-icon-button__icon--on{display:inline-block}.mdc-icon-button{display:inline-block;position:relative;box-sizing:border-box;border:none;outline:none;background-color:transparent;fill:currentColor;color:inherit;text-decoration:none;cursor:pointer;user-select:none}.mdc-icon-button .mdc-icon-button__touch{position:absolute;top:50%;height:48px;left:50%;width:48px;transform:translate(-50%, -50%)}.mdc-icon-button:disabled{cursor:default;pointer-events:none}.mdc-icon-button--display-flex{align-items:center;display:inline-flex;justify-content:center}.mdc-icon-button__icon{display:inline-block}.mdc-icon-button__icon.mdc-icon-button__icon--on{display:none}.mdc-icon-button--touch{margin-top:0px;margin-bottom:0px}.mdc-icon-button--on .mdc-icon-button__icon{display:none}.mdc-icon-button--on .mdc-icon-button__icon.mdc-icon-button__icon--on{display:inline-block}:host{display:inline-block;outline:none}:host([disabled]){pointer-events:none}:host{--mdc-ripple-color: currentcolor;-webkit-tap-highlight-color:transparent}:host,.mdc-icon-button{vertical-align:top}.mdc-icon-button{width:var(--mdc-icon-button-size, 48px);height:var(--mdc-icon-button-size, 48px);padding:calc( (var(--mdc-icon-button-size, 48px) - var(--mdc-icon-size, 24px)) / 2 )}.mdc-icon-button>i{position:absolute;top:0;padding-top:inherit}.mdc-icon-button i,.mdc-icon-button svg,.mdc-icon-button img,.mdc-icon-button ::slotted(*){display:block;width:var(--mdc-icon-size, 24px);height:var(--mdc-icon-size, 24px)}'],i||(i=o.slice(0)),n=Object.freeze(Object.defineProperties(o,{raw:{value:Object.freeze(i)}}))))},25230:function(e,r,t){var n=t(87480),o=t(32207),i=t(68646),c=t(90779);function a(e){return a="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},a(e)}function s(e,r){if(!(e instanceof r))throw new TypeError("Cannot call a class as a function")}function l(e,r){return l=Object.setPrototypeOf||function(e,r){return e.__proto__=r,e},l(e,r)}function u(e){var r=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var t,n=d(e);if(r){var o=d(this).constructor;t=Reflect.construct(n,arguments,o)}else t=n.apply(this,arguments);return p(this,t)}}function p(e,r){if(r&&("object"===a(r)||"function"==typeof r))return r;if(void 0!==r)throw new TypeError("Derived constructors may only return object or undefined");return function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e)}function d(e){return d=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},d(e)}var f=function(e){!function(e,r){if("function"!=typeof r&&null!==r)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(r&&r.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),r&&l(e,r)}(t,e);var r=u(t);function t(){return s(this,t),r.apply(this,arguments)}return t}(i.B);f.styles=[c.W],f=(0,n.__decorate)([(0,o.Mo)("mwc-icon-button")],f)}}]);