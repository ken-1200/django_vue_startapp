<template>
  <div id="app">
    <p v-if="isErrored">{{ error }}</p>

    <!-- アラート -->
    <v-alert
      prominent
      type="error"
      :value="addCart.alert"
    >
      <v-row align="center">
        <v-col class="grow">
          同じ商品が既にカートに存在しています。
          カートの中を確認してください。
        </v-col>
        <v-col class="shrink">
          <v-btn
            @click="goToCart"
          >購入ページを確認する</v-btn>
        </v-col>
      </v-row>
    </v-alert>

    <v-container fluid>
      <v-layout wrap row>
        <v-flex cols=12 md=3 xl=4>
          <v-row class="float-md-left">
            <v-col
              cols="auto"
              sm="auto"
            >
              <v-img
                :src="items.item_img"
                contain
                max-height="700"
                max-width="500"
              >
                <!-- プログレス -->
                <template v-slot:placeholder>
                  <v-row
                    class="fill-height ma-0"
                    align="center"
                    justify="center"
                  >
                    <v-progress-circular
                      indeterminate
                      color="grey lighten-5"
                    ></v-progress-circular>
                  </v-row>
                </template>
              </v-img>
            </v-col>
          </v-row>

          <!-- 商品内容 -->
          <v-col
            class="d-flex"
            cols="auto"
          >
            <v-card
              width="100%"
              outlined
            >
              <v-card-title>{{ items.item_name }}</v-card-title>

              <v-card-subtitle>¥{{ items.item_price | addComma }}</v-card-subtitle>

              <v-select
                v-model="addCart.item_total"
                :items="itemQuantity"
                :rules="quantityRules"
                label="数量"
                dense
                solo
                no-data-text="在庫がありません。"
                style="width: 45%"
              ></v-select>

              <v-btn
                min-width="45%"
                :loading="loading"
                color="success"
                class="mr-4"
                @click="validate"
              >
                カートに入れる
              </v-btn>

              <v-card-text class="mt-4">
                {{ items.item_detail }}
              </v-card-text>
            </v-card>
          </v-col>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      items: {
        item_id: this.$route.params.id,
        item_name: '',
        item_detail: '',
        item_price: 0,
        item_total: null,
        item_img: '',
      },
      addCart: {
        item_id: this.$route.params.id,
        item_name: '',
        item_price: 0,
        item_total: null,
        item_img: '',
        itemQuantity: null,
        alert: false, 
      },
      itemQuantity: [],
      error: null,
      loading: false,
      quantityRules: [
        v => Boolean(v) || '数量は必須です。',
      ],
    }
  },
  methods: {
    // ボタン
    validate() {
      // 空文字の場合
      if (this.addCart.item_total == "" || this.addCart.item_total == undefined) return;

      // 在庫数からカートに入れた数量を引く
      this.items.item_total -= this.addCart.item_total;

      // Vuexに送る情報を格納
      this.addCart = {
        item_id: this.$route.params.id,
        item_name: this.items.item_name,
        item_price: this.items.item_price,
        item_total: this.addCart.item_total,
        itemQuantity: this.items.item_total,
        alert: false, 
      }

      // カートに入れる
      this.$store.dispatch('addToCart', this.addCart);
    },
    goToCart() {
      this.$router.push('/order/cart/furisode');
      this.addCart.alert = false;
    }
  },
  computed: {
    accessToken() {
      return this.$store.getters.access_token;
    },
    isErrored() {
      return this.error != null;
    },
  },
  async created() {
    // 商品取得 なくても良さそう
    await this.$store.dispatch('getItemList');

    // 該当する商品を取得
    const getSelectItems = this.$store.getters.selectItems(Number(this.$route.params.id));

    // 該当する商品を格納
    getSelectItems.forEach(el => {
      // 画像がないものはこっち
      if (el.fields.item_img == "") {
        el.fields.item_img = "http://localhost:8001/media/image/sampleImage.jpg";
      } else {
        // 画像あり
        el.fields.item_img = "http://localhost:8001/media/" + el.fields.item_img;
      }

      // 表示する情報を格納
      this.items = {
        item_id: this.$route.params.id,
        item_name: el.fields.item_name,
        item_detail: el.fields.item_detail,
        item_price: el.fields.item_price,
        item_total: el.fields.item_total,
        item_img: el.fields.item_img,
      }

      // 数量リストに格納
      for (let i = 1; i <= this.items.item_total; i++) {
        this.itemQuantity.push(i);
      }
    });

    this.error = this.$store.getters.erroInfo;

    // エラー表示
    if (this.items.length != 0) {
      // エラー内容表示(ex)Notfound..)
      this.error = this.$store.getters.erroInfo;
    } else {
      // 商品がない時(0個返却された)
      this.error = ' 商品がありません。';
    }
  },
}
</script>

<style lang="scss" scoped>
.float-md-left {
  margin: 5% 5% 0 5%;
}
.d-flex {
  display: flex!important;
  margin: 6% 0 0 0;
}
.v-card {
  &__subtitle {
    text-align: left;
  }

  &__text {
    white-space: pre-wrap;
    text-align: left;
  }
}
.v-list {
  text-align: left;
}
</style>