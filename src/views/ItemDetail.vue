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
        <v-flex cols=2 md=3 xl=4>
          <v-img
            flex
            contain
            lazy-src="https://picsum.photos/id/11/10/6"
            max-height="600"
            max-width="500"
            src="https://picsum.photos/id/11/500/600"
          ></v-img>

          <v-card outlined>
            <v-card-title>{{ items.item_name }}</v-card-title>

            <v-card-subtitle>¥{{ items.item_price | addComma }}</v-card-subtitle>

            <v-row align="center">
              <v-col
                class="d-flex"
                cols="12"
                sm="6"
              >
                <v-select
                  v-model="addCart.item_total"
                  :items="itemQuantity"
                  :rules="quantityRules"
                  label="数量"
                  dense
                  solo
                  no-data-text="在庫がありません。"
                ></v-select>
              </v-col>
            </v-row>

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
      this.$router.push('/order/cart/kinomo');
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

    this.error = this.$store.getters.error;

    // エラー表示
    if (this.items.length != 0) {
      // エラー内容表示(ex)Notfound..)
      this.error = this.$store.getters.error;
    } else {
      // 商品がない時(0個返却された)
      this.error = ' 商品がありません。';
    }
  },
}
</script>

<style lang="scss" scoped>
.v-image {
  width: 40%;
  float: left;
  margin: 5% 5% 0 5%;
}
.v-card {
  width: 45%;
  float: right;
  margin: 8% 5% 0 0;

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