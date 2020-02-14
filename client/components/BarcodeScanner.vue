<template>
  <div class="barcode-scanner">
    <div class="viewport" ref="viewport"></div>
  </div>
</template>

<script>
import Quagga from "@ericblade/quagga2";
export default {
  name: "BarcodeScanner",
  mounted() {
    console.log("viewport", this.$refs.viewport);
    Quagga.init(
      {
        inputStream: {
          type: "LiveStream",
          target: this.$refs.viewport
        },
        decoder: {
          readers: ["upc_reader"],
          debug: {
            drawBoundingBox: true,
            showFrequency: true,
            drawScanline: true,
            showPattern: true
          }
        }
      },
      function(err) {
        if (err) {
          console.error(err);
          return;
        }
        Quagga.start();
        Quagga.onDetected(function(a) {
          console.log(a.codeResult.code);
        });
      }
    );
  }
};
</script>

<style lang="scss" scoped></style>
