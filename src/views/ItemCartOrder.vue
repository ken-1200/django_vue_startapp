<template>
  <div id="app">
    <!-- logoにしたいな -->
    <h1>FURISODE</h1>
    <v-container fluid>
      <v-layout wrap row>
        <v-flex cols=12 md=3 xl=4>

        <!-- 購入確定ボタン -->
          <v-card
            width="100%"
            outlined
          >
            <v-btn
              class="ma-10"
              width="80%"
              height="60px"
              color="success"
              @click.stop="purchase"
            >
              購入を確定する
            </v-btn>
          </v-card>
          <!-- 購入者情報 -->
          <v-card-subtitle>購入者情報</v-card-subtitle>

          <v-card outlined>
            <v-simple-table>
              <template v-slot:default>
                <tbody>
                  <tr>
                    <td>氏名</td>
                    <td>{{ getUserName }}</td>
                  </tr>
                  <tr>
                    <td>メールアドレス</td>
                    <td>{{ getUserEmail }}</td>
                  </tr>
                </tbody>
              </template>
            </v-simple-table>
          </v-card>

            <!-- 注文内容 -->
          <v-card outlined>
            <v-card-subtitle>注文内容</v-card-subtitle>

            <!-- <v-img
              flex
              contain
              lazy-src="https://picsum.photos/id/11/10/6"
              max-height="114"
              max-width="76"
              src="https://picsum.photos/id/11/500/600"
            ></v-img> -->

            <v-data-table
              :headers="headers"
              :items="cartInfo"
              hide-default-footer
              no-data-text="カートに商品がありません。"
            >
            </v-data-table>

            <v-divider></v-divider>

            <!-- 小計 -->
            <v-row>
              <v-col
                cols="12"
                sm="6"
                md="4"
              >
                <div class="subTotalBlock__list listTable">
                  <span class="listTable__heading">送料</span>
                  <span class="listTable__content">¥ 0</span>
                </div>
                <div class="subTotalBlock__list listTable">
                  <span class="listTable__heading">合計</span>
                  <span class="listTable__content">¥ {{ totalPrice | addComma }}</span>
                </div>
              </v-col>
            </v-row>

            <!-- 購入確定ボタン -->
            <v-divider></v-divider>
            <v-container
              outlined
              width="100%"
            >
              <div class="btn__left">
                <v-btn
                  class="ma-10"
                  height="60px"
                  color="grey"
                  @click="backToPage"
                >
                  購入画面へ戻る
                </v-btn>
              </div>
              <div class="btn__right">
                <v-btn
                  class="ma-10"
                  height="60px"
                  color="success"
                  @click.stop="purchase"
                >
                  購入を確定する
                </v-btn>
              </div>
            </v-container>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      totalPrice: 0,
      headers: [
        {
          text: '商品名',
          align: 'start',
          sortable: false,
          value: 'name',
        },
        { text: '値段', value: 'price', sortable: false  },
        { text: '個数', value: 'quantity' },
        { text: '小計', value: 'subtotal', sortable: false  },
        { text: '編集', value: 'actions', sortable: false },
      ],
      cartInfo: [],
      userName: "",
      userEmail: "",
      role: [],
    }
  },
  methods: {
    backToPage() {
      this.$router.push('/order/cart/furisode');
    },
    async purchase() {
      await axios.post('/payments_post/', {
        // 商品情報+購入者情報
        "role": this.role,
        "pay_totalprice": this.totalPrice,
        "user_email": this.userEmail,
      })
      .then(response => {
        console.log(response.data);
        // 決済確認画面遷移
        this.$router.push('/payment');

        response.data.payments.role.forEach(el => {
          // カート中削除
          this.$store.dispatch('deleteCart', el.item_id);

          // カート内の情報削除
          this.$store.dispatch('deleteCartInfo', el.item_id);
        });

        // 初期化
        this.totalPrice = 0;
        this.userEmail = "";
        this.userEmail = "";
        this.cartInfo = [];
        this.role = [];
      })
      .catch(error => {
        console.log(error);
      });
    }
  },
  computed: {
    getUserName() {
      return this.userName;
    },
    getUserEmail() {
      return this.userEmail;
    }
  },
  created() {
    // ログイン情報を取得
    this.userName = this.$store.getters.userInfo.user_name;
    this.userEmail = this.$store.getters.userInfo.user_email;

    // Vuexから商品情報を取得
    const itemInfo = this.$store.getters.itemInfo;

    itemInfo.forEach(el => {
      const inc = String(el.item_price).includes('¥');
      if (inc) {
        // 文字が含まれる場合
        const price = el.item_price.replace(/,/g, '').replace(/¥/g, '');

        // カート情報セット
        this.cartInfo.push(
          {
            pk: el.item_id,
            name: el.item_name,
            price: '¥' + price.toLocaleString(),
            quantity: el.item_total,
            subtotal: '¥' + (price * el.item_total).toLocaleString(),
            itemQuantity: el.itemQuantity,
          }
        );
        // 支払い情報
        this.role.push(
          {
            item_id: el.item_id,
            item_quantity: el.item_total,
          }
        );
      } else {
        // カート情報セット
        this.cartInfo.push(
          {
            pk: el.item_id,
            name: el.item_name,
            price: '¥' + el.item_price.toLocaleString(),
            quantity: el.item_total,
            subtotal: '¥' + (el.item_price * el.item_total).toLocaleString(),
            itemQuantity: el.itemQuantity,
          }
        );
        // 支払い情報
        this.role.push(
          {
            item_id: el.item_id,
            item_quantity: el.item_total,
          }
        );
      }
    });

    // 合計金額表示
    this.totalPrice = this.cartInfo.reduce((acc, cur) => {
      return acc + Number(cur.subtotal.replace(/,/g, '').replace(/¥/g, ''));
    }, 0);

    console.log(this.cartInfo);
    console.log(this.role);
  },
}
</script>

<style lang="scss" scoped>
h1 {
  font-family: 'YuMincho';
  font-size: 5rem;
  font-weight: 400;
  letter-spacing: -.015625em;
}
.v-card__subtitle {
  align-items: center;
  display: flex;
  justify-content: center;
  padding: 0px;
  height: 100px;
  background-color: #dbdbdb;
  font-size: 21px;
}
.row {
  display: flex;
  flex-wrap: wrap;
  flex: 1 1 auto;
  margin-right: -12px;
  margin-left: -12px;
  justify-content: flex-end;
}
.subTotalBlock {
  padding: 10px 0;

  &__list {
    margin: 0 0 0 auto;
    width: 100%;
  }
}
.listTable {
  display: table;
  padding: 5px 15px;

  &__heading {
    color: #666;
    display: table-cell;
    font-size: 13px;
    text-align: right;
  }

  &__content {
    display: table-cell;
    font-size: 16px;
    font-weight: 700;
    text-align: right;
    width: 60%;
  }
}
.v-btn {
  color: white !important;

  &__content {
    align-items: center;
    color: inherit;
    display: flex;
    flex: 1 0 auto;
    justify-content: inherit;
    line-height: normal;
    position: relative;
  }
}
.btn {
  &__left {
    display: inline-block;
    vertical-align: top;
  }

  &__right {
    display: inline-block;
    vertical-align: top;
  }
}
</style>