import Vue from "vue";
import BarcodeScanner from "../components/BarcodeScanner.vue";

// @ts-ignore
window.bs = new Vue({
  el: "#barcode-scanner",
  render(h) {
    return h(BarcodeScanner);
  }
});
