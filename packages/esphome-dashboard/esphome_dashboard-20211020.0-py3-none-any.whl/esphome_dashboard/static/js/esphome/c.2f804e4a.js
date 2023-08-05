import{r as o,_ as e,e as t,t as n,n as i,a as s,y as c}from"./index-9f84ce7c.js";import"./c.38c1ed92.js";import{a}from"./c.55cec96c.js";import"./c.32a957d2.js";import"./c.be57b2c6.js";import"./c.f521922d.js";let r=class extends s{render(){return c`
      <esphome-process-dialog
        .heading=${`Download ${this.configuration}`}
        .type=${"compile"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        ${void 0===this._result?"":0===this._result?c`
              <a
                slot="secondaryAction"
                href="${`./download.bin?configuration=${encodeURIComponent(this.configuration)}`}"
              >
                <mwc-button label="Download"></mwc-button>
              </a>
            `:c`
              <mwc-button
                slot="secondaryAction"
                dialogAction="close"
                label="Retry"
                @click=${this._handleRetry}
              ></mwc-button>
            `}
      </esphome-process-dialog>
    `}_handleProcessDone(o){if(this._result=o.detail,0!==o.detail)return;const e=document.createElement("a");e.download=this.configuration+".bin",e.href=`./download.bin?configuration=${encodeURIComponent(this.configuration)}`,document.body.appendChild(e),e.click(),e.remove()}_handleRetry(){a(this.configuration)}_handleClose(){this.parentNode.removeChild(this)}};r.styles=o`
    a {
      text-decoration: none;
    }
  `,e([t()],r.prototype,"configuration",void 0),e([n()],r.prototype,"_result",void 0),r=e([i("esphome-compile-dialog")],r);
