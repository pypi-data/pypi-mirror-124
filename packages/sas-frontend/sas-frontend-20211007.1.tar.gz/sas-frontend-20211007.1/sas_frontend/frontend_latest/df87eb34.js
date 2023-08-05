"use strict";(self.webpackChunksas_frontend=self.webpackChunksas_frontend||[]).push([[319],{319:(e,t,r)=>{var i=r(7599),n=r(26767),o=r(5701),s=r(67352),a=r(47181),l=r(96151),c=r(1600);function d(){d=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!p(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return v(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?v(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=m(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:y(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=y(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function u(e){var t,r=m(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function f(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function p(e){return e.decorators&&e.decorators.length}function h(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function y(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function m(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function v(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function k(e,t,r){return k="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=w(e)););return e}(e,t);if(i){var n=Object.getOwnPropertyDescriptor(i,t);return n.get?n.get.call(r):n.value}},k(e,t,r||e)}function w(e){return w=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},w(e)}!function(e,t,r,i){var n=d();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(h(o.descriptor)||h(n.descriptor)){if(p(o)||p(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(p(o)){if(p(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}f(o,n)}else t.push(o)}return t}(s.d.map(u)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,n.M)("ha-hls-player")],(function(e,t){class n extends t{constructor(...t){super(...t),e(this)}}return{F:n,d:[{kind:"field",decorators:[(0,o.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.C)()],key:"url",value:void 0},{kind:"field",decorators:[(0,o.C)({type:Boolean,attribute:"controls"})],key:"controls",value:()=>!1},{kind:"field",decorators:[(0,o.C)({type:Boolean,attribute:"muted"})],key:"muted",value:()=>!1},{kind:"field",decorators:[(0,o.C)({type:Boolean,attribute:"autoplay"})],key:"autoPlay",value:()=>!1},{kind:"field",decorators:[(0,o.C)({type:Boolean,attribute:"playsinline"})],key:"playsInline",value:()=>!1},{kind:"field",decorators:[(0,o.C)({type:Boolean,attribute:"allow-exoplayer"})],key:"allowExoPlayer",value:()=>!1},{kind:"field",decorators:[(0,s.I)("video")],key:"_videoEl",value:void 0},{kind:"field",key:"_hlsPolyfillInstance",value:void 0},{kind:"field",key:"_exoPlayer",value:()=>!1},{kind:"method",key:"connectedCallback",value:function(){k(w(n.prototype),"connectedCallback",this).call(this),this.hasUpdated&&this._startHls()}},{kind:"method",key:"disconnectedCallback",value:function(){k(w(n.prototype),"disconnectedCallback",this).call(this),this._cleanUp()}},{kind:"method",key:"render",value:function(){return i.dy`
      <video
        ?autoplay=${this.autoPlay}
        .muted=${this.muted}
        ?playsinline=${this.playsInline}
        ?controls=${this.controls}
        @loadeddata=${this._elementResized}
      ></video>
    `}},{kind:"method",key:"updated",value:function(e){k(w(n.prototype),"updated",this).call(this,e);e.has("url")&&(this._cleanUp(),this._startHls())}},{kind:"method",key:"_getUseExoPlayer",value:async function(){if(!this.hass.auth.external||!this.allowExoPlayer)return!1;const e=await(0,c.e)(this.hass.auth.external);return e&&e.hasExoPlayer}},{kind:"method",key:"_startHls",value:async function(){const e=this._videoEl,t=this._getUseExoPlayer(),i=fetch(this.url),n=(await r.e(94683).then(r.t.bind(r,94683,23))).default;if(!this.isConnected)return;let o=n.isSupported();if(o||(o=""!==e.canPlayType("application/vnd.apple.mpegurl")),!o)return void(e.innerHTML=this.hass.localize("ui.components.media-browser.video_not_supported"));const s=await t,a=await(await i).text();if(!this.isConnected)return;const l=/#EXT-X-STREAM-INF:.*?(?:CODECS=".*?(hev1|hvc1)?\..*?".*?)?(?:\n|\r\n)(.+)/g,c=l.exec(a),d=l.exec(a);let u;u=null!==c&&null===d?new URL(c[2],this.url).href:this.url,s&&null!==c&&void 0!==c[1]?this._renderHLSExoPlayer(u):n.isSupported()?this._renderHLSPolyfill(e,n,u):this._renderHLSNative(e,u)}},{kind:"method",key:"_renderHLSExoPlayer",value:async function(e){this._exoPlayer=!0,window.addEventListener("resize",this._resizeExoPlayer),this.updateComplete.then((()=>(0,l.y)())).then(this._resizeExoPlayer),this._videoEl.style.visibility="hidden",await this.hass.auth.external.sendMessage({type:"exoplayer/play_hls",payload:{url:new URL(e,window.location.href).toString(),muted:this.muted}})}},{kind:"field",key:"_resizeExoPlayer",value(){return()=>{if(!this._videoEl)return;const e=this._videoEl.getBoundingClientRect();this.hass.auth.external.fireMessage({type:"exoplayer/resize",payload:{left:e.left,top:e.top,right:e.right,bottom:e.bottom}})}}},{kind:"method",key:"_renderHLSPolyfill",value:async function(e,t,r){const i=new t({backBufferLength:60,fragLoadingTimeOut:3e4,manifestLoadingTimeOut:3e4,levelLoadingTimeOut:3e4});this._hlsPolyfillInstance=i,i.attachMedia(e),i.on(t.Events.MEDIA_ATTACHED,(()=>{i.loadSource(r)}))}},{kind:"method",key:"_renderHLSNative",value:async function(e,t){e.src=t,e.addEventListener("loadedmetadata",(()=>{e.play()}))}},{kind:"method",key:"_elementResized",value:function(){(0,a.B)(this,"iron-resize")}},{kind:"method",key:"_cleanUp",value:function(){this._hlsPolyfillInstance&&(this._hlsPolyfillInstance.destroy(),this._hlsPolyfillInstance=void 0),this._exoPlayer&&(window.removeEventListener("resize",this._resizeExoPlayer),this.hass.auth.external.fireMessage({type:"exoplayer/stop"}),this._exoPlayer=!1);const e=this._videoEl;e.removeAttribute("src"),e.load()}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`
      :host,
      video {
        display: block;
      }

      video {
        width: 100%;
      }
    `}}]}}),i.oi)},1600:(e,t,r)=>{r.d(t,{e:()=>i});const i=e=>(e.cache.cfg||(e.cache.cfg=e.sendMessage({type:"config/get"})),e.cache.cfg)}}]);
//# sourceMappingURL=df87eb34.js.map