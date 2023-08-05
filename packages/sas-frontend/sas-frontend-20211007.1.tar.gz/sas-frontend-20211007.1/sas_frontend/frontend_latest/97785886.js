"use strict";(self.webpackChunksas_frontend=self.webpackChunksas_frontend||[]).push([[60999],{60999:(e,t,r)=>{r.r(t),r.d(t,{SideBarView:()=>g});var i=r(7599),n=r(5701),o=r(17717),a=r(228),s=r(47181),l=r(87744),d=r(54324);function c(){c=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!u(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],t);r.push.apply(r,d)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return y(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?y(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=v(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:m(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=m(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function f(e){var t,r=v(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function p(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function u(e){return e.decorators&&e.decorators.length}function h(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function m(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function v(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function y(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function b(e,t,r){return b="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=k(e)););return e}(e,t);if(i){var n=Object.getOwnPropertyDescriptor(i,t);return n.get?n.get.call(r):n.value}},b(e,t,r||e)}function k(e){return k=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},k(e)}let g=function(e,t,r,i){var n=c();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var a=t((function(e){n.initializeInstanceElements(e,s.elements)}),r),s=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(h(o.descriptor)||h(n.descriptor)){if(u(o)||u(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(u(o)){if(u(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}p(o,n)}else t.push(o)}return t}(a.d.map(f)),e);return n.initializeClassElements(a.F,s.elements),n.runClassFinishers(a.F,s.finishers)}(null,(function(e,t){class c extends t{constructor(...t){super(...t),e(this)}}return{F:c,d:[{kind:"field",decorators:[(0,n.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.C)({attribute:!1})],key:"lovelace",value:void 0},{kind:"field",decorators:[(0,n.C)({type:Number})],key:"index",value:void 0},{kind:"field",decorators:[(0,n.C)({type:Boolean})],key:"isStrategy",value:()=>!1},{kind:"field",decorators:[(0,n.C)({attribute:!1})],key:"cards",value:()=>[]},{kind:"field",decorators:[(0,o.S)()],key:"_config",value:void 0},{kind:"field",key:"_mqlListenerRef",value:void 0},{kind:"field",key:"_mql",value:void 0},{kind:"method",key:"connectedCallback",value:function(){b(k(c.prototype),"connectedCallback",this).call(this),this._mql=window.matchMedia("(min-width: 760px)"),this._mqlListenerRef=this._createCards.bind(this),this._mql.addListener(this._mqlListenerRef)}},{kind:"method",key:"disconnectedCallback",value:function(){var e;b(k(c.prototype),"disconnectedCallback",this).call(this),null===(e=this._mql)||void 0===e||e.removeListener(this._mqlListenerRef),this._mqlListenerRef=void 0,this._mql=void 0}},{kind:"method",key:"setConfig",value:function(e){this._config=e}},{kind:"method",key:"willUpdate",value:function(e){var t,i,n;if(b(k(c.prototype),"willUpdate",this).call(this,e),null!==(t=this.lovelace)&&void 0!==t&&t.editMode&&Promise.all([r.e(62613),r.e(59799),r.e(6294),r.e(95916),r.e(70741)]).then(r.bind(r,70741)),e.has("cards")&&this._createCards(),!e.has("lovelace"))return;const o=e.get("lovelace");(!e.has("cards")&&(null==o?void 0:o.config)!==(null===(i=this.lovelace)||void 0===i?void 0:i.config)||o&&(null==o?void 0:o.editMode)!==(null===(n=this.lovelace)||void 0===n?void 0:n.editMode))&&this._createCards()}},{kind:"method",key:"render",value:function(){var e;return i.dy`
      <div class="container"></div>
      ${null!==(e=this.lovelace)&&void 0!==e&&e.editMode?i.dy`
            <ha-fab
              .label=${this.hass.localize("ui.panel.lovelace.editor.edit_card.add")}
              extended
              @click=${this._addCard}
              class=${(0,a.$)({rtl:(0,l.HE)(this.hass)})}
            >
              <ha-svg-icon slot="icon" .path=${"M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"}></ha-svg-icon>
            </ha-fab>
          `:""}
    `}},{kind:"method",key:"_addCard",value:function(){(0,s.B)(this,"ll-create-card")}},{kind:"method",key:"_createCards",value:function(){var e;const t=document.createElement("div");let r;if(t.id="main",null!==(e=this._mql)&&void 0!==e&&e.matches?(r=document.createElement("div"),r.id="sidebar"):r=t,this.hasUpdated){const e=this.renderRoot.querySelector("#main"),i=this.renderRoot.querySelector("#sidebar"),n=this.renderRoot.querySelector(".container");e&&n.removeChild(e),i&&n.removeChild(i),n.appendChild(t),n.appendChild(r)}else this.updateComplete.then((()=>{const e=this.renderRoot.querySelector(".container");e.appendChild(t),e.appendChild(r)}));this.cards.forEach(((e,i)=>{var n,o,a,s;const l=null===(n=this._config)||void 0===n||null===(o=n.cards)||void 0===o?void 0:o[i];let c;if(this.isStrategy||null===(a=this.lovelace)||void 0===a||!a.editMode)e.editMode=!1,c=e;else{var f;c=document.createElement("hui-card-options"),c.hass=this.hass,c.lovelace=this.lovelace,c.path=[this.index,i],e.editMode=!0;const t=document.createElement("mwc-icon-button");t.slot="buttons";const r=document.createElement("ha-svg-icon");r.path="sidebar"!==(null==l||null===(f=l.view_layout)||void 0===f?void 0:f.position)?"M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z":"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z",t.appendChild(r),t.addEventListener("click",(()=>{var e;this.lovelace.saveConfig((0,d.LG)(this.lovelace.config,[this.index,i],{...l,view_layout:{position:"sidebar"!==(null==l||null===(e=l.view_layout)||void 0===e?void 0:e.position)?"sidebar":"main"}}))})),c.appendChild(t),c.appendChild(e)}"sidebar"!==(null==l||null===(s=l.view_layout)||void 0===s?void 0:s.position)?t.appendChild(c):r.appendChild(c)}))}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`
      :host {
        display: block;
        padding-top: 4px;
        height: 100%;
        box-sizing: border-box;
      }

      .container {
        display: flex;
        justify-content: center;
        margin-left: 4px;
        margin-right: 4px;
      }

      #main {
        max-width: 1620px;
        flex-grow: 2;
      }

      #sidebar {
        flex-grow: 1;
        flex-shrink: 0;
        max-width: 380px;
      }

      .container > div {
        min-width: 0;
        box-sizing: border-box;
      }

      .container > div > * {
        display: block;
        margin: var(--masonry-view-card-margin, 4px 4px 8px);
      }

      @media (max-width: 500px) {
        .container > div > * {
          margin-left: 0;
          margin-right: 0;
        }
      }

      ha-fab {
        position: sticky;
        float: right;
        right: calc(16px + env(safe-area-inset-right));
        bottom: calc(16px + env(safe-area-inset-bottom));
        z-index: 1;
      }

      ha-fab.rtl {
        float: left;
        right: auto;
        left: calc(16px + env(safe-area-inset-left));
      }
    `}}]}}),i.oi);customElements.define("hui-sidebar-view",g)}}]);
//# sourceMappingURL=97785886.js.map