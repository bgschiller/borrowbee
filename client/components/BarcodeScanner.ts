import Quagga from "@ericblade/quagga2";
export default {
  el: '[data-vue-component="barcode-scanner"]',
  name: "BarcodeScanner",
  data() {
    return {
      mostRecentIsbn: null,
      isbns: "",
      error: null,
    };
  },
  methods: {
    appendIsbn(num: string) {
      if (num === this.mostRecentIsbn) return;
      this.mostRecentIsbn = num;
      this.isbns += num + "\n";
    },
    initCamera() {
      Quagga.init(
        {
          inputStream: {
            type: "LiveStream",
            target: this.$refs.viewport,
            constraints: {
              width: 800,
              height: 600,
              facingMode: "environment",
            },
          },
          decoder: {
            readers: ["ean_reader"],
            debug: {
              drawBoundingBox: true,
              showFrequency: true,
              drawScanline: true,
              showPattern: true,
            },
          },
        },
        (err) => {
          if (err) {
            this.error = err;
            return;
          }
          Quagga.start();
          Quagga.onDetected((a) => this.appendIsbn(a.codeResult.code));
        }
      );
    },
  },
};
