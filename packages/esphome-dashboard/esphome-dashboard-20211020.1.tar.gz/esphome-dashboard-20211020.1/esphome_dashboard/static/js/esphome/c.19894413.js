import{_ as o,e as i,t,n as e,a as s,y as a,J as n,K as l}from"./index-372adaf5.js";import"./c.9b6c5dac.js";let d=class extends s{render(){const o=void 0===this._valid?"":this._valid?"✅":"❌";return a`
      <esphome-process-dialog
        .heading=${`Validate ${this.configuration} ${o}`}
        .type=${"validate"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Edit"
          @click=${this._openEdit}
        ></mwc-button>
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Install"
          @click=${this._openInstall}
        ></mwc-button>
      </esphome-process-dialog>
    `}_openEdit(){n(this.configuration)}_openInstall(){l(this.configuration)}_handleProcessDone(o){this._valid=0==o.detail}_handleClose(){this.parentNode.removeChild(this)}};o([i()],d.prototype,"configuration",void 0),o([t()],d.prototype,"_valid",void 0),d=o([e("esphome-validate-dialog")],d);
