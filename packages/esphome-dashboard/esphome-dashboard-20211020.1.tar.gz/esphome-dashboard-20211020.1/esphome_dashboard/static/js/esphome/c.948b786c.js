import{_ as e,e as o,n as s,a,y as i}from"./index-372adaf5.js";import"./c.9b6c5dac.js";let t=class extends a{render(){return i`
      <esphome-process-dialog
        .heading=${`Clean MQTT discovery topics for ${this.configuration}`}
        .type=${"clean-mqtt"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
      >
      </esphome-process-dialog>
    `}_handleClose(){this.parentNode.removeChild(this)}};e([o()],t.prototype,"configuration",void 0),t=e([s("esphome-clean-mqtt-dialog")],t);
