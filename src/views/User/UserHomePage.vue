<template>
  <div id="app">
    <v-container fluid>
      <v-layout wrap row>
        <v-flex cols=12 md=3 xl=4>
          <v-card-title>ユーザーホーム</v-card-title>

          <!-- エラー -->
          <template v-if="isErrored">{{ error }}</template>

          <!-- 注文 -->
          <v-card
            class="mx-auto"
            max-width="400"
            style="text-align: initial"
            tile
          >
            <v-card-title>注文</v-card-title>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>Single-line item</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
        
            <v-list-item two-line>
              <v-list-item-content>
                <v-list-item-title>Two-line item</v-list-item-title>
                <v-list-item-subtitle>Secondary text</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
        
            <v-list-item three-line>
              <v-list-item-content>
                <v-list-item-title>Three-line item</v-list-item-title>
                <v-list-item-subtitle>
                  Secondary line text Lorem ipsum dolor sit amet,
                </v-list-item-subtitle>
                <v-list-item-subtitle>
                  consectetur adipiscing elit.
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-card>

          <v-divider class="my-4"></v-divider>

          <!-- 会員情報 -->
          <v-card
            class="mx-auto"
            max-width="400"
            style="text-align: initial"
            tile
          >
            <v-card-title>注文</v-card-title>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>Single-line item</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
        
            <v-list-item two-line>
              <v-list-item-content>
                <v-list-item-title>Two-line item</v-list-item-title>
                <v-list-item-subtitle>Secondary text</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
        
            <v-list-item three-line>
              <v-list-item-content>
                <v-list-item-title>Three-line item</v-list-item-title>
                <v-list-item-subtitle>
                  Secondary line text Lorem ipsum dolor sit amet,
                </v-list-item-subtitle>
                <v-list-item-subtitle>
                  consectetur adipiscing elit.
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
export default {
  data() {
    return{
      error: null,
    }
  },
  computed: {
    isErrored() {
      return this.error != null;
    },
  },
  created() {
    // 購入情報
    this.$store.dispatch('getPaymentInfo');

    // エラー
    this.error = this.$store.getters.error;
  }
}
</script>

<style lang="scss">

</style>