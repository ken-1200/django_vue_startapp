<template>
  <div id="app">
    <v-container fluid style="height: 800px">
      <v-layout wrap row>
        <v-flex cols=12 md=3 xl=4>
          <v-card-title>ユーザーホーム</v-card-title>

          <!-- 注文 -->
          <v-card
            class="mx-auto"
            max-width="600"
            style="text-align: initial"
            tile
          >
            <v-card-title>注文<img src="../../../public/image/truck.jpg" alt="" style="width: 1.2rem; margin-left: 2%;"></v-card-title>
            <v-list-item three-line>
              <v-list-item-content>
                <v-list-item-title
                  @click="orderHistory"
                  style="cursor: pointer"
                >購入履歴・キャンセル・返品</v-list-item-title>
                <v-list-item-subtitle>
                  現在ご注文いただいている商品のキャンセル・返品・配送状況の確認、過去の購入履歴を確認できます。
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
        
            <v-list-item three-line>
              <v-list-item-content>
                <v-list-item-title>注文検索</v-list-item-title>
                <v-list-item-subtitle>
                  注文番号とメールアドレスを入力することで配達状況や詳細をご覧いただけます。また、注文のキャンセル・返品リクエストを行うことができます。
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-card>

          <v-divider class="my-4"></v-divider>

          <!-- 会員情報 -->
          <v-card
            class="mx-auto"
            max-width="600"
            style="text-align: initial"
            tile
          >
            <v-card-title>会員情報<img src="../../../public/image/pencil.jpg" alt="" style="width: 1.2rem; margin-left: 2%;"></v-card-title>
            <v-list-item three-line>
              <v-list-item-content>
                <v-list-item-title>会員情報変更</v-list-item-title>
                <v-list-item-subtitle>
                  お客様の会員様情報の変更はこちらから行ってください。
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
        
            <v-list-item three-line>
              <v-list-item-content>
                <v-list-item-title>パスワードの変更</v-list-item-title>
                <v-list-item-subtitle>
                  パスワードを忘れた方はこちらからお問い合せください。
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>

            <v-list-item three-line>
              <v-list-item-content>
                <v-dialog
                  v-model="dialog"
                  persistent
                  max-width="290"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-list-item-title
                      v-bind="attrs"
                      v-on="on"
                    >
                      退会手続き
                    </v-list-item-title>
                    <v-list-item-subtitle>
                      退会手続きはこちらから行ってください。
                    </v-list-item-subtitle>
                  </template>
                  <v-card>
                    <v-card-title class="headline">
                      退会手続きを行ってもよろしいですか？
                    </v-card-title>
                    <v-card-text style="color: red">退会手続きをした場合、ご注文履歴の確認が行えなくなりますのでご注意ください。</v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn
                        color="green darken-1"
                        text
                        @click="dialog = false"
                      >
                        キャンセル
                      </v-btn>
                      <v-btn
                        color="green darken-1"
                        text
                        @click="dialog = false"
                        @click.stop="withDrawal"
                      >
                        OK
                      </v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
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
    return {
      dialog: false,
    }
  },
  methods: {
    orderHistory() {
      this.$router.push('/member/order/history');
    },
    withDrawal() {
      this.$store.dispatch('user_withDrawal', this.$store.getters.user_id);
    },
  },
}
</script>

<style lang="scss">

</style>