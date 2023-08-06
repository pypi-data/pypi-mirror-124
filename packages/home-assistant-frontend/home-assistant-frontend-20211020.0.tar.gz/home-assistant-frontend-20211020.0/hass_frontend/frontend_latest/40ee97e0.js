"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[6169],{6169:(e,t,s)=>{s.a(e,(async e=>{s.r(t);var r=s(7599),i=s(50467),n=s(99476),o=e([n]);n=(o.then?await o:o)[0];const a={1:5,2:3,3:2};class d extends n.p{static async getConfigElement(){return await Promise.all([s.e(8161),s.e(5009),s.e(2955),s.e(8985),s.e(8055),s.e(4040),s.e(7502),s.e(2017),s.e(9505),s.e(1536),s.e(3883),s.e(3098),s.e(7426),s.e(4074),s.e(6087),s.e(8183),s.e(6002),s.e(3303),s.e(1480),s.e(809),s.e(4535),s.e(8331),s.e(8101),s.e(6902),s.e(515),s.e(9216),s.e(9665),s.e(8175),s.e(8194),s.e(2382)]).then(s.bind(s,22382)),document.createElement("hui-grid-card-editor")}async getCardSize(){if(!this._cards||!this._config)return 0;if(this.square){const e=a[this.columns]||1;return(this._cards.length<this.columns?e:this._cards.length/this.columns*e)+(this._config.title?1:0)}const e=[];for(const t of this._cards)e.push((0,i.N)(t));const t=await Promise.all(e);let s=this._config.title?1:0;for(let e=0;e<t.length;e+=this.columns)s+=Math.max(...t.slice(e,e+this.columns));return s}get columns(){var e;return(null===(e=this._config)||void 0===e?void 0:e.columns)||3}get square(){var e;return!1!==(null===(e=this._config)||void 0===e?void 0:e.square)}setConfig(e){super.setConfig(e),this.style.setProperty("--grid-card-column-count",String(this.columns)),this.square?this.setAttribute("square",""):this.removeAttribute("square")}static get styles(){return[super.sharedStyles,r.iv`
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
//# sourceMappingURL=40ee97e0.js.map