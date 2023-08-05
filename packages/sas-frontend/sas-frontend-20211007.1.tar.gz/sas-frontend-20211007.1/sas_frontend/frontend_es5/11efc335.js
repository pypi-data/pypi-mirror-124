"use strict";(self.webpackChunksas_frontend=self.webpackChunksas_frontend||[]).push([[8101],{68101:function(e,t,r){r(25230),r(30879),r(53973),r(89194),r(51095),r(33076);var n,i,o,a,s,c=r(7599),l=r(25209),u=r(26767),d=r(5701),f=r(17717),p=r(67352),h=r(228),m=r(14516),v=r(47181),y=r(58831),b=r(57066),k=r(57292),w=r(74186),g=r(26765),_=r(73826);r(52039);function E(e){return E="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},E(e)}function C(e,t,r,n,i,o,a){try{var s=e[o](a),c=s.value}catch(l){return void r(l)}s.done?t(c):Promise.resolve(c).then(n,i)}function P(e){return function(e){if(Array.isArray(e))return V(e)}(e)||Z(e)||B(e)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function x(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function S(e,t){return S=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},S(e,t)}function A(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var r,n=T(e);if(t){var i=T(this).constructor;r=Reflect.construct(n,arguments,i)}else r=n.apply(this,arguments);return D(this,r)}}function D(e,t){if(t&&("object"===E(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return O(e)}function O(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function T(e){return T=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},T(e)}function j(){j=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(n){t.forEach((function(t){var i=t.placement;if(t.kind===n&&("static"===i||"prototype"===i)){var o="static"===i?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var n=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],n=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!R(e))return r.push(e);var t=this.decorateElement(e,i);r.push(t.element),r.push.apply(r,t.extras),n.push.apply(n,t.finishers)}),this),!t)return{elements:r,finishers:n};var o=this.decorateConstructor(r,t);return n.push.apply(n,o.finishers),o.finishers=n,o},addElementPlacement:function(e,t,r){var n=t[e.placement];if(!r&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var r=[],n=[],i=e.decorators,o=i.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,i[o])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&n.push(c.finisher);var l=c.extras;if(l){for(var u=0;u<l.length;u++)this.addElementPlacement(l[u],t);r.push.apply(r,l)}}return{element:e,finishers:n,extras:r}},decorateConstructor:function(e,t){for(var r=[],n=t.length-1;n>=0;n--){var i=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[n])(i)||i);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||Z(t)||B(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=M(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:n,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:I(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=I(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var n=(0,t[r])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function z(e){var t,r=M(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function L(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function R(e){return e.decorators&&e.decorators.length}function F(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function I(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function M(e){var t=function(e,t){if("object"!==E(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!==E(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===E(t)?t:String(t)}function B(e,t){if(e){if("string"==typeof e)return V(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?V(e,t):void 0}}function V(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function Z(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}function q(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}var $=function(e){return(0,c.dy)(n||(n=q(["<style>\n    paper-item {\n      padding: 0;\n      margin: -10px;\n      margin-left: 0;\n    }\n    #content {\n      display: flex;\n      align-items: center;\n    }\n    ha-svg-icon {\n      padding-left: 2px;\n      margin-right: -2px;\n      color: var(--secondary-text-color);\n    }\n    :host(:not([selected])) ha-svg-icon {\n      display: none;\n    }\n    :host([selected]) paper-item {\n      margin-left: 10px;\n    }\n  </style>\n  <ha-svg-icon .path=","></ha-svg-icon>\n  <paper-item class=",">\n    <paper-item-body two-line>","</paper-item-body>\n  </paper-item>"])),"M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z",(0,h.$)({"add-new":"add_new"===e.area_id}),e.name)};!function(e,t,r,n){var i=j();if(n)for(var o=0;o<n.length;o++)i=n[o](i);var a=t((function(e){i.initializeInstanceElements(e,s.elements)}),r),s=i.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},n=0;n<e.length;n++){var i,o=e[n];if("method"===o.kind&&(i=t.find(r)))if(F(o.descriptor)||F(i.descriptor)){if(R(o)||R(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(R(o)){if(R(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}L(o,i)}else t.push(o)}return t}(a.d.map(z)),e);i.initializeClassElements(a.F,s.elements),i.runClassFinishers(a.F,s.finishers)}([(0,u.M)("ha-area-picker")],(function(e,t){var r=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&S(e,t)}(n,t);var r=A(n);function n(){var t;x(this,n);for(var i=arguments.length,o=new Array(i),a=0;a<i;a++)o[a]=arguments[a];return t=r.call.apply(r,[this].concat(o)),e(O(t)),t}return n}(t);return{F:r,d:[{kind:"field",decorators:[(0,d.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,d.C)()],key:"label",value:void 0},{kind:"field",decorators:[(0,d.C)()],key:"value",value:void 0},{kind:"field",decorators:[(0,d.C)()],key:"placeholder",value:void 0},{kind:"field",decorators:[(0,d.C)({type:Boolean,attribute:"no-add"})],key:"noAdd",value:void 0},{kind:"field",decorators:[(0,d.C)({type:Array,attribute:"include-domains"})],key:"includeDomains",value:void 0},{kind:"field",decorators:[(0,d.C)({type:Array,attribute:"exclude-domains"})],key:"excludeDomains",value:void 0},{kind:"field",decorators:[(0,d.C)({type:Array,attribute:"include-device-classes"})],key:"includeDeviceClasses",value:void 0},{kind:"field",decorators:[(0,d.C)()],key:"deviceFilter",value:void 0},{kind:"field",decorators:[(0,d.C)()],key:"entityFilter",value:void 0},{kind:"field",decorators:[(0,d.C)({type:Boolean})],key:"disabled",value:void 0},{kind:"field",decorators:[(0,f.S)()],key:"_areas",value:void 0},{kind:"field",decorators:[(0,f.S)()],key:"_devices",value:void 0},{kind:"field",decorators:[(0,f.S)()],key:"_entities",value:void 0},{kind:"field",decorators:[(0,f.S)()],key:"_opened",value:void 0},{kind:"field",decorators:[(0,p.I)("vaadin-combo-box-light",!0)],key:"comboBox",value:void 0},{kind:"field",key:"_init",value:function(){return!1}},{kind:"method",key:"hassSubscribe",value:function(){var e=this;return[(0,b.sG)(this.hass.connection,(function(t){e._areas=t})),(0,k.q4)(this.hass.connection,(function(t){e._devices=t})),(0,w.LM)(this.hass.connection,(function(t){e._entities=t}))]}},{kind:"method",key:"open",value:function(){var e=this;this.updateComplete.then((function(){var t,r;null===(t=e.shadowRoot)||void 0===t||null===(r=t.querySelector("vaadin-combo-box-light"))||void 0===r||r.open()}))}},{kind:"method",key:"focus",value:function(){var e=this;this.updateComplete.then((function(){var t,r;null===(t=e.shadowRoot)||void 0===t||null===(r=t.querySelector("paper-input"))||void 0===r||r.focus()}))}},{kind:"field",key:"_getAreas",value:function(){var e=this;return(0,m.Z)((function(t,r,n,i,o,a,s,c,l){if(!t.length)return[{area_id:"",name:e.hass.localize("ui.components.area-picker.no_areas")}];var u,d,f={};if(i||o||a){var p,h=function(e,t){var r="undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(!r){if(Array.isArray(e)||(r=B(e))||t&&e&&"number"==typeof e.length){r&&(e=r);var n=0,i=function(){};return{s:i,n:function(){return n>=e.length?{done:!0}:{done:!1,value:e[n++]}},e:function(e){throw e},f:i}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var o,a=!0,s=!1;return{s:function(){r=r.call(e)},n:function(){var e=r.next();return a=e.done,e},e:function(e){s=!0,o=e},f:function(){try{a||null==r.return||r.return()}finally{if(s)throw o}}}}(n);try{for(h.s();!(p=h.n()).done;){var m=p.value;m.device_id&&(m.device_id in f||(f[m.device_id]=[]),f[m.device_id].push(m))}}catch(w){h.e(w)}finally{h.f()}u=r,d=n.filter((function(e){return e.area_id}))}else s&&(u=r),c&&(d=n.filter((function(e){return e.area_id})));i&&(u=u.filter((function(e){var t=f[e.id];return!(!t||!t.length)&&f[e.id].some((function(e){return i.includes((0,y.M)(e.entity_id))}))})),d=d.filter((function(e){return i.includes((0,y.M)(e.entity_id))}))),o&&(u=u.filter((function(e){var t=f[e.id];return!t||!t.length||n.every((function(e){return!o.includes((0,y.M)(e.entity_id))}))})),d=d.filter((function(e){return!o.includes((0,y.M)(e.entity_id))}))),a&&(u=u.filter((function(t){var r=f[t.id];return!(!r||!r.length)&&f[t.id].some((function(t){var r=e.hass.states[t.entity_id];return!!r&&(r.attributes.device_class&&a.includes(r.attributes.device_class))}))})),d=d.filter((function(t){var r=e.hass.states[t.entity_id];return r.attributes.device_class&&a.includes(r.attributes.device_class)}))),s&&(u=u.filter((function(e){return s(e)}))),c&&(d=d.filter((function(e){return c(e)})));var v,b,k=t;(u&&(v=u.filter((function(e){return e.area_id})).map((function(e){return e.area_id}))),d)&&(v=(null!==(b=v)&&void 0!==b?b:[]).concat(d.filter((function(e){return e.area_id})).map((function(e){return e.area_id}))));return v&&(k=t.filter((function(e){return v.includes(e.area_id)}))),k.length||(k=[{area_id:"",name:e.hass.localize("ui.components.area-picker.no_match")}]),l?k:[].concat(P(k),[{area_id:"add_new",name:e.hass.localize("ui.components.area-picker.add_new")}])}))}},{kind:"method",key:"updated",value:function(e){(!this._init&&this._devices&&this._areas&&this._entities||e.has("_opened")&&this._opened)&&(this._init=!0,this.comboBox.items=this._getAreas(this._areas,this._devices,this._entities,this.includeDomains,this.excludeDomains,this.includeDeviceClasses,this.deviceFilter,this.entityFilter,this.noAdd))}},{kind:"method",key:"render",value:function(){var e;return this._devices&&this._areas&&this._entities?(0,c.dy)(o||(o=q(['\n      <vaadin-combo-box-light\n        item-value-path="area_id"\n        item-id-path="area_id"\n        item-label-path="name"\n        .value=',"\n        .disabled=","\n        ","\n        @opened-changed=","\n        @value-changed=","\n      >\n        <paper-input\n          .label=","\n          .placeholder=","\n          .disabled=",'\n          class="input"\n          autocapitalize="none"\n          autocomplete="off"\n          autocorrect="off"\n          spellcheck="false"\n        >\n          ',"\n\n          <mwc-icon-button\n            .label=",'\n            slot="suffix"\n            class="toggle-button"\n          >\n            <ha-svg-icon\n              .path=',"\n            ></ha-svg-icon>\n          </mwc-icon-button>\n        </paper-input>\n      </vaadin-combo-box-light>\n    "])),this._value,this.disabled,(0,l.t7)($),this._openedChanged,this._areaChanged,void 0===this.label&&this.hass?this.hass.localize("ui.components.area-picker.area"):this.label,this.placeholder?null===(e=this._area(this.placeholder))||void 0===e?void 0:e.name:void 0,this.disabled,this.value?(0,c.dy)(a||(a=q(["\n                <mwc-icon-button\n                  .label=",'\n                  slot="suffix"\n                  class="clear-button"\n                  @click=',"\n                >\n                  <ha-svg-icon .path=","></ha-svg-icon>\n                </mwc-icon-button>\n              "])),this.hass.localize("ui.components.area-picker.clear"),this._clearValue,"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"):"",this.hass.localize("ui.components.area-picker.toggle"),this._opened?"M7,15L12,10L17,15H7Z":"M7,10L12,15L17,10H7Z"):(0,c.dy)(i||(i=q([""])))}},{kind:"field",key:"_area",value:function(){var e=this;return(0,m.Z)((function(t){var r;return null===(r=e._areas)||void 0===r?void 0:r.find((function(e){return e.area_id===t}))}))}},{kind:"method",key:"_clearValue",value:function(e){e.stopPropagation(),this._setValue("")}},{kind:"get",key:"_value",value:function(){return this.value||""}},{kind:"method",key:"_openedChanged",value:function(e){this._opened=e.detail.value}},{kind:"method",key:"_areaChanged",value:function(e){var t,r,n=this,i=e.detail.value;"add_new"===i?(e.target.value=this._value,(0,g.D9)(this,{title:this.hass.localize("ui.components.area-picker.add_dialog.title"),text:this.hass.localize("ui.components.area-picker.add_dialog.text"),confirmText:this.hass.localize("ui.components.area-picker.add_dialog.add"),inputLabel:this.hass.localize("ui.components.area-picker.add_dialog.name"),confirm:(t=regeneratorRuntime.mark((function e(t){var r;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(t){e.next=2;break}return e.abrupt("return");case 2:return e.prev=2,e.next=5,(0,b.Lo)(n.hass,{name:t});case 5:r=e.sent,n._areas=[].concat(P(n._areas),[r]),n._setValue(r.area_id),e.next=13;break;case 10:e.prev=10,e.t0=e.catch(2),(0,g.Ys)(n,{text:n.hass.localize("ui.components.area-picker.add_dialog.failed_create_area")});case 13:case"end":return e.stop()}}),e,null,[[2,10]])})),r=function(){var e=this,r=arguments;return new Promise((function(n,i){var o=t.apply(e,r);function a(e){C(o,n,i,a,s,"next",e)}function s(e){C(o,n,i,a,s,"throw",e)}a(void 0)}))},function(e){return r.apply(this,arguments)})})):i!==this._value&&this._setValue(i)}},{kind:"method",key:"_setValue",value:function(e){var t=this;this.value=e,setTimeout((function(){(0,v.B)(t,"value-changed",{value:e}),(0,v.B)(t,"change")}),0)}},{kind:"get",static:!0,key:"styles",value:function(){return(0,c.iv)(s||(s=q(["\n      paper-input > mwc-icon-button {\n        --mdc-icon-button-size: 24px;\n        padding: 2px;\n        color: var(--secondary-text-color);\n      }\n      [hidden] {\n        display: none;\n      }\n    "])))}}]}}),(0,_.f)(c.oi))},73826:function(e,t,r){r.d(t,{f:function(){return g}});var n=r(5701);function i(e){return i="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},i(e)}function o(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function a(e,t){return a=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},a(e,t)}function s(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var r,n=w(e);if(t){var i=w(this).constructor;r=Reflect.construct(n,arguments,i)}else r=n.apply(this,arguments);return c(this,r)}}function c(e,t){if(t&&("object"===i(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return l(e)}function l(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function u(e,t,r,n){var i=d();if(n)for(var o=0;o<n.length;o++)i=n[o](i);var a=t((function(e){i.initializeInstanceElements(e,s.elements)}),r),s=i.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},n=0;n<e.length;n++){var i,o=e[n];if("method"===o.kind&&(i=t.find(r)))if(m(o.descriptor)||m(i.descriptor)){if(h(o)||h(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(h(o)){if(h(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}p(o,i)}else t.push(o)}return t}(a.d.map(f)),e);return i.initializeClassElements(a.F,s.elements),i.runClassFinishers(a.F,s.finishers)}function d(){d=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(n){t.forEach((function(t){var i=t.placement;if(t.kind===n&&("static"===i||"prototype"===i)){var o="static"===i?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var n=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],n=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!h(e))return r.push(e);var t=this.decorateElement(e,i);r.push(t.element),r.push.apply(r,t.extras),n.push.apply(n,t.finishers)}),this),!t)return{elements:r,finishers:n};var o=this.decorateConstructor(r,t);return n.push.apply(n,o.finishers),o.finishers=n,o},addElementPlacement:function(e,t,r){var n=t[e.placement];if(!r&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var r=[],n=[],i=e.decorators,o=i.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,i[o])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&n.push(c.finisher);var l=c.extras;if(l){for(var u=0;u<l.length;u++)this.addElementPlacement(l[u],t);r.push.apply(r,l)}}return{element:e,finishers:n,extras:r}},decorateConstructor:function(e,t){for(var r=[],n=t.length-1;n>=0;n--){var i=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[n])(i)||i);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return b(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?b(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=y(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:n,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:v(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=v(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var n=(0,t[r])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function f(e){var t,r=y(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function p(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function h(e){return e.decorators&&e.decorators.length}function m(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function v(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function y(e){var t=function(e,t){if("object"!==i(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!==i(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===i(t)?t:String(t)}function b(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function k(e,t,r){return k="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var n=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=w(e)););return e}(e,t);if(n){var i=Object.getOwnPropertyDescriptor(n,t);return i.get?i.get.call(r):i.value}},k(e,t,r||e)}function w(e){return w=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},w(e)}var g=function(e){var t=u(null,(function(e,t){var r=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&a(e,t)}(n,t);var r=s(n);function n(){var t;o(this,n);for(var i=arguments.length,a=new Array(i),s=0;s<i;s++)a[s]=arguments[s];return t=r.call.apply(r,[this].concat(a)),e(l(t)),t}return n}(t);return{F:r,d:[{kind:"field",decorators:[(0,n.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",key:"__unsubs",value:void 0},{kind:"method",key:"connectedCallback",value:function(){k(w(r.prototype),"connectedCallback",this).call(this),this.__checkSubscribed()}},{kind:"method",key:"disconnectedCallback",value:function(){if(k(w(r.prototype),"disconnectedCallback",this).call(this),this.__unsubs){for(;this.__unsubs.length;){var e=this.__unsubs.pop();e instanceof Promise?e.then((function(e){return e()})):e()}this.__unsubs=void 0}}},{kind:"method",key:"updated",value:function(e){k(w(r.prototype),"updated",this).call(this,e),e.has("hass")&&this.__checkSubscribed()}},{kind:"method",key:"hassSubscribe",value:function(){return[]}},{kind:"method",key:"__checkSubscribed",value:function(){void 0===this.__unsubs&&this.isConnected&&void 0!==this.hass&&(this.__unsubs=this.hassSubscribe())}}]}}),e);return t}}}]);