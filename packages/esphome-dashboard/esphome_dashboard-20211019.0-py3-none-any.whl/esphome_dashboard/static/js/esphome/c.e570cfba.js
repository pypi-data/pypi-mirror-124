import{r as o,_ as e,e as t,t as n,n as i,a as s,y as a}from"./index-875ce5f6.js";import"./c.e1749e91.js";import{a as r}from"./c.33d5f9b8.js";import"./c.0760b28b.js";import"./c.ee4c7919.js";import"./c.5ba66d0f.js";let c=class extends s{render(){return a`
      <esphome-process-dialog
        .heading=${`Download ${this.configuration}`}
        .type=${"compile"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        ${void 0===this._result?"":0===this._result?a`
              <a
                slot="secondaryAction"
                href="${`./download.bin?configuration=${encodeURIComponent(this.configuration)}`}"
              >
                <mwc-button label="Download"></mwc-button>
              </a>
            `:a`
              <mwc-button
                slot="secondaryAction"
                dialogAction="close"
                label="Retry"
                @click=${this._handleRetry}
              ></mwc-button>
            `}
      </esphome-process-dialog>
    `}_handleProcessDone(o){if(this._result=o.detail,0!==o.detail)return;const e=document.createElement("a");e.download=this.configuration+".bin",e.href=`./download.bin?configuration=${encodeURIComponent(this.configuration)}`,document.body.appendChild(e),e.click(),e.remove()}_handleRetry(){r(this.configuration)}_handleClose(){this.parentNode.removeChild(this)}};c.styles=o`
    a {
      text-decoration: none;
    }
  `,e([t()],c.prototype,"configuration",void 0),e([n()],c.prototype,"_result",void 0),c=e([i("esphome-compile-dialog")],c);
