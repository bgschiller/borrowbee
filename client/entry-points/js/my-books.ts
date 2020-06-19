import Vue from "vue/dist/vue.esm.browser";
import BarcodeScanner from "../../components/BarcodeScanner";

// @ts-ignore
window.bs = new Vue({
  delimiters: ["[[", "]]"],
  ...BarcodeScanner,
});
