"use strict";(self.webpackChunksas_frontend=self.webpackChunksas_frontend||[]).push([[6169],{6169:(e,t,r)=>{r.a(e,(async e=>{r.r(t);var s=r(7599),i=r(50467),n=r(99476),o=e([n]);n=(o.then?await o:o)[0];const a={1:5,2:3,3:2};class d extends n.p{static async getConfigElement(){return await Promise.all([r.e(75009),r.e(78161),r.e(42955),r.e(14409),r.e(28055),r.e(26561),r.e(69505),r.e(62613),r.e(59799),r.e(6294),r.e(93098),r.e(89841),r.e(77426),r.e(56087),r.e(22001),r.e(46002),r.e(14497),r.e(12990),r.e(81480),r.e(87482),r.e(74535),r.e(68331),r.e(68101),r.e(36902),r.e(20515),r.e(20259),r.e(9665),r.e(68175),r.e(37504),r.e(22382)]).then(r.bind(r,22382)),document.createElement("hui-grid-card-editor")}async getCardSize(){if(!this._cards||!this._config)return 0;if(this.square){const e=a[this.columns]||1;return(this._cards.length<this.columns?e:this._cards.length/this.columns*e)+(this._config.title?1:0)}const e=[];for(const t of this._cards)e.push((0,i.N)(t));const t=await Promise.all(e);let r=this._config.title?1:0;for(let e=0;e<t.length;e+=this.columns)r+=Math.max(...t.slice(e,e+this.columns));return r}get columns(){var e;return(null===(e=this._config)||void 0===e?void 0:e.columns)||3}get square(){var e;return!1!==(null===(e=this._config)||void 0===e?void 0:e.square)}setConfig(e){super.setConfig(e),this.style.setProperty("--grid-card-column-count",String(this.columns)),this.square?this.setAttribute("square",""):this.removeAttribute("square")}static get styles(){return[super.sharedStyles,s.iv`
        #root {
          display: grid;
          grid-template-columns: repeat(
            var(--grid-card-column-count, ${3}),
            minmax(0, 1fr)
          );
          grid-gap: var(--grid-card-gap, 8px);
        }
        :host([square]) #root {
          grid-auto-rows: 1fr;
        }
        :host([square]) #root::before {
          content: "";
          width: 0;
          padding-bottom: 100%;
          grid-row: 1 / 1;
          grid-column: 1 / 1;
        }

        :host([square]) #root > *:not([hidden]) {
          grid-row: 1 / 1;
          grid-column: 1 / 1;
        }
        :host([square]) #root > *:not([hidden]) ~ *:not([hidden]) {
          /*
	       * Remove grid-row and grid-column from every element that comes after
	       * the first not-hidden element
	       */
          grid-row: unset;
          grid-column: unset;
        }
      `]}}customElements.define("hui-grid-card",d)}))}}]);
//# sourceMappingURL=e79938ac.js.map