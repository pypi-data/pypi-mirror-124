"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[8723],{48723:(e,t,r)=>{r.r(t);var i=r(7599),n=r(26767),o=r(5701),s=r(17717),a=r(62877),c=r(47181),l=r(44634),d=r(91741),u=(r(22098),r(52039),r(93491)),p=r(15688),f=r(53658),h=r(75502);function m(){m=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!g(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[o])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return w(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?w(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=C(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:k(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=k(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function y(e){var t,r=C(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function v(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function g(e){return e.decorators&&e.decorators.length}function b(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function k(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function C(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function w(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function E(e,t,r){return E="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=x(e)););return e}(e,t);if(i){var n=Object.getOwnPropertyDescriptor(i,t);return n.get?n.get.call(r):n.value}},E(e,t,r||e)}function x(e){return x=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},x(e)}const A={moisture:"M12,20A6,6 0 0,1 6,14C6,10 12,3.25 12,3.25C12,3.25 18,10 18,14A6,6 0 0,1 12,20Z",temperature:"M15 13V5A3 3 0 0 0 9 5V13A5 5 0 1 0 15 13M12 4A1 1 0 0 1 13 5V8H11V5A1 1 0 0 1 12 4Z",brightness:"M3.55,18.54L4.96,19.95L6.76,18.16L5.34,16.74M11,22.45C11.32,22.45 13,22.45 13,22.45V19.5H11M12,5.5A6,6 0 0,0 6,11.5A6,6 0 0,0 12,17.5A6,6 0 0,0 18,11.5C18,8.18 15.31,5.5 12,5.5M20,12.5H23V10.5H20M17.24,18.16L19.04,19.95L20.45,18.54L18.66,16.74M20.45,4.46L19.04,3.05L17.24,4.84L18.66,6.26M13,0.55H11V3.5H13M4,10.5H1V12.5H4M6.76,4.84L4.96,3.05L3.55,4.46L5.34,6.26L6.76,4.84Z",conductivity:"M11.36,2C11.15,2 10.87,2.12 10.57,2.32C10,2.7 8.85,3.9 8.4,5.1C8.06,6 8.05,6.82 8.19,7.43C7.63,7.53 7.22,7.71 7.06,7.78C6.55,8 5.47,8.96 5.37,10.45C5.34,10.97 5.41,11.5 5.57,12C4.91,12.19 4.53,12.43 4.5,12.44C4.18,12.56 3.65,12.93 3.5,13.13C3.15,13.53 2.92,14 2.79,14.5C2.5,15.59 2.6,16.83 3.13,17.83C3.42,18.39 3.82,19 4.26,19.43C5.7,20.91 8.18,21.47 10.14,21.79C12.53,22.19 15.03,22.05 17.26,21.13C20.61,19.74 21.5,17.5 21.64,16.89C21.93,15.5 21.57,14.19 21.42,13.87C21.2,13.41 20.84,12.94 20.25,12.64C19.85,12.39 19.5,12.26 19.24,12.2C19.5,11.25 19.13,10.5 18.62,9.94C17.85,9.12 17.06,9 17.06,9V9C17.32,8.5 17.42,7.9 17.28,7.32C17.12,6.61 16.73,6.16 16.22,5.86C15.7,5.55 15.06,5.4 14.4,5.28C14.08,5.22 12.75,5.03 12.2,4.27C11.75,3.65 11.74,2.53 11.62,2.2C11.57,2.07 11.5,2 11.36,2M16,9.61C16.07,9.61 16.13,9.62 16.19,9.62C17.62,9.78 18.64,11.16 18.47,12.69C18.3,14.22 17,15.34 15.57,15.18V15.18C14.14,15 13.12,13.65 13.29,12.11C13.45,10.66 14.64,9.56 16,9.61M8.62,9.61C9.95,9.65 11.06,10.78 11.16,12.21C11.28,13.75 10.21,15.08 8.78,15.19H8.77C7.34,15.3 6.08,14.14 5.96,12.6V12.6C5.85,11.06 6.92,9.73 8.35,9.62V9.62C8.44,9.61 8.53,9.61 8.62,9.61M8.64,11.31C8.6,11.31 8.57,11.31 8.53,11.32C7.97,11.39 7.57,11.9 7.64,12.45C7.7,13 8.21,13.39 8.77,13.32C9.33,13.25 9.73,12.74 9.67,12.19C9.61,11.67 9.15,11.3 8.64,11.31M15.94,11.33C15.42,11.35 15,11.75 14.96,12.28C14.92,12.83 15.35,13.31 15.91,13.34C16.5,13.38 16.96,12.95 17,12.4C17.04,11.84 16.61,11.36 16.05,11.33C16,11.33 16,11.33 15.94,11.33M8.71,16.15C9,16.14 9.26,16.23 9.5,16.28C10.68,16.5 11.7,16.53 12.19,16.53C12.68,16.53 13.69,16.5 14.86,16.28C15.27,16.2 15.74,16.03 16.11,16.28C16.59,16.6 16.24,17.75 15.5,18.53C15.04,19 13.97,19.91 12.19,19.91C10.41,19.91 9.33,19 8.88,18.53C8.14,17.75 7.79,16.6 8.26,16.28C8.4,16.19 8.55,16.15 8.71,16.15Z",battery:void 0};!function(e,t,r,i){var n=m();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(b(o.descriptor)||b(n.descriptor)){if(g(o)||g(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(g(o)){if(g(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}v(o,n)}else t.push(o)}return t}(s.d.map(y)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,n.M)("hui-plant-status-card")],(function(e,t){class n extends t{constructor(...t){super(...t),e(this)}}return{F:n,d:[{kind:"method",static:!0,key:"getConfigElement",value:async function(){return await Promise.all([r.e(8161),r.e(5009),r.e(2955),r.e(8985),r.e(8055),r.e(9505),r.e(3098),r.e(7082),r.e(4535),r.e(2669)]).then(r.bind(r,92669)),document.createElement("hui-plant-status-card-editor")}},{kind:"method",static:!0,key:"getStubConfig",value:function(e,t,r){return{type:"plant-status",entity:(0,p.j)(e,1,t,r,["plant"])[0]||""}}},{kind:"field",decorators:[(0,o.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.S)()],key:"_config",value:void 0},{kind:"method",key:"getCardSize",value:function(){return 3}},{kind:"method",key:"setConfig",value:function(e){if(!e.entity||"plant"!==e.entity.split(".")[0])throw new Error("Specify an entity from within the plant domain");this._config=e}},{kind:"method",key:"shouldUpdate",value:function(e){return(0,f.G)(this,e)}},{kind:"method",key:"updated",value:function(e){if(E(x(n.prototype),"updated",this).call(this,e),!this._config||!this.hass)return;const t=e.get("hass"),r=e.get("_config");t&&r&&t.themes===this.hass.themes&&r.theme===this._config.theme||(0,a.R)(this,this.hass.themes,this._config.theme)}},{kind:"method",key:"render",value:function(){if(!this.hass||!this._config)return i.dy``;const e=this.hass.states[this._config.entity];return e?i.dy`
      <ha-card
        class=${e.attributes.entity_picture?"has-plant-image":""}
      >
        <div
          class="banner"
          style="background-image:url(${e.attributes.entity_picture})"
        >
          <div class="header">
            ${this._config.name||(0,d.C)(e)}
          </div>
        </div>
        <div class="content">
          ${this.computeAttributes(e).map((t=>i.dy`
              <div
                class="attributes"
                @action=${this._handleMoreInfo}
                .actionHandler=${(0,u.K)()}
                tabindex="0"
                .value=${t}
              >
                <div>
                  <ha-svg-icon
                    .path=${this.computeIcon(t,e.attributes.battery)}
                  ></ha-svg-icon>
                </div>
                <div
                  class=${-1===e.attributes.problem.indexOf(t)?"":"problem"}
                >
                  ${e.attributes[t]}
                </div>
                <div class="uom">
                  ${e.attributes.unit_of_measurement_dict[t]||""}
                </div>
              </div>
            `))}
        </div>
      </ha-card>
    `:i.dy`
        <hui-warning>
          ${(0,h.i)(this.hass,this._config.entity)}
        </hui-warning>
      `}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`
      ha-card {
        height: 100%;
        box-sizing: border-box;
      }
      .banner {
        display: flex;
        align-items: flex-end;
        background-repeat: no-repeat;
        background-size: cover;
        background-position: center;
        padding-top: 12px;
      }

      .has-plant-image .banner {
        padding-top: 30%;
      }

      .header {
        /* start paper-font-headline style */
        font-family: "Roboto", "Noto", sans-serif;
        -webkit-font-smoothing: antialiased; /* OS X subpixel AA bleed bug */
        text-rendering: optimizeLegibility;
        font-size: 24px;
        font-weight: 400;
        letter-spacing: -0.012em;
        /* end paper-font-headline style */

        line-height: 40px;
        padding: 8px 16px;
      }

      .has-plant-image .header {
        font-size: 16px;
        font-weight: 500;
        line-height: 16px;
        padding: 16px;
        color: white;
        width: 100%;
        background: rgba(0, 0, 0, var(--dark-secondary-opacity));
      }

      .content {
        display: flex;
        justify-content: space-between;
        padding: 16px 32px 24px 32px;
      }

      .has-plant-image .content {
        padding-bottom: 16px;
      }

      ha-svg-icon {
        color: var(--paper-item-icon-color);
        margin-bottom: 8px;
      }

      .attributes {
        cursor: pointer;
      }

      .attributes:focus {
        outline: none;
        background: var(--divider-color);
        border-radius: 100%;
      }

      .attributes div {
        text-align: center;
      }

      .problem {
        color: var(--error-color);
        font-weight: bold;
      }

      .uom {
        color: var(--secondary-text-color);
      }
    `}},{kind:"method",key:"computeAttributes",value:function(e){return Object.keys(A).filter((t=>t in e.attributes))}},{kind:"method",key:"computeIcon",value:function(e,t){return"battery"===e?(0,l.M)(t):A[e]}},{kind:"method",key:"_handleMoreInfo",value:function(e){const t=e.currentTarget,r=this.hass.states[this._config.entity];t.value&&(0,c.B)(this,"hass-more-info",{entityId:r.attributes.sensors[t.value]})}}]}}),i.oi)}}]);
//# sourceMappingURL=0f971349.js.map