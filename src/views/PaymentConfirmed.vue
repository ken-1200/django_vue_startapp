<template>
  <div id="app">
    <v-container fluid style="height: 1000px">
      <v-layout wrap row>
        <v-flex cols=12 md=3 xl=4>
          <v-card-title>決済確定画面</v-card-title>
          <v-card-text>購入が完了しました。</v-card-text>

          <!-- 購入情報 -->
          <h2>{{ userName }}さんお買い上げありがとうございました！</h2>
          <v-card-text style="padding-bottom: 0">注文内容がショップに送信されました。ご登録いただいたアドレスに確認のメールをお送りいたします。</v-card-text>
          <v-card-text style="padding-top: 0">この度はご購入いただきまして、誠にありがとうございます。商品は発送され次第、ご登録頂いているメールアドレスに改めてご連絡いたします。</v-card-text>

          <v-divider></v-divider>

          <!-- ショップからクーポンなどのお得情報 -->
          <v-row>
            <v-col cols="12">
              <v-card
                class="ma-10"
                height="300px"
              >
                <v-card-subtitle
                  class="mb-10"
                  style="font-size: 1.12rem"
                >ご購入いただいたあなたへのクーポン!</v-card-subtitle>
                <img class="coupon__img" src="../../public/image/coupon1.jpg" alt="">
              </v-card>
            </v-col>
          </v-row>

          <!-- ボタン -->
          <v-btn
            class="ma-10"
            height="60px"
            color="grey"
            to="/item_list"
          >
            商品一覧に戻る
          </v-btn>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userName: "",
    }
  },
  created() {
    // ログイン情報を取得
    this.userName = this.$store.getters.userInfo.user_name;
  }
}
</script>

<style lang="scss" scoped>
.coupon__img {
  width: 10rem;
}
a {
  color: $cWhite !important;
}
</style>