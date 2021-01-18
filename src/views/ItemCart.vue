<template>
  <div id="app">
    <!-- logoにしたいな -->
    <h1>FURISODE</h1>
    <v-container fluid>
      <v-layout wrap row>
        <v-flex cols=12 md=3 xl=4>

          <!-- ヘッダー -->
          <v-card
            width="100%"
            outlined
          >
            <v-btn
              class="ma-10"
              width="80%"
              height="60px"
              to="/item_list"
            >
              買い物を続ける
            </v-btn>
          </v-card>

          <!-- テーブル -->
          <v-card outlined>
            <v-card-subtitle>カートの中身</v-card-subtitle>

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
              :items-per-page="5"
              sort-by="price"
              no-data-text="カートに商品がありません。"
            >
            <!-- 編集ダイアログ -->
              <template v-slot:top>
                <v-toolbar
                  flat
                >
                  <v-dialog
                    v-model="dialog"
                    max-width="500px"
                  >
                    <v-card outlined>
                      <v-card-text>
                        <v-container>
                          <v-row class="row-select">
                            <v-col
                              cols="12"
                              sm="6"
                              md="4"
                            >
                              <v-card-title>個数</v-card-title>
                              <v-select
                                v-model="editedItem.quantity"
                                :items="itemQuantity"
                                label="個数"
                                dense
                                solo
                                no-data-text="在庫がありません。"
                              ></v-select>
                            </v-col>
                          </v-row>
                        </v-container>
                      </v-card-text>

                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                          color="blue darken-1"
                          text
                          @click="close"
                        >
                          Cancel
                        </v-btn>
                        <v-btn
                          color="blue darken-1"
                          text
                          @click="save"
                        >
                          OK
                        </v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-dialog>

                  <!-- 削除確認ダイアログ -->
                  <v-dialog v-model="dialogDelete" max-width="500px">
                    <v-card outlined>
                      <v-card-title class="headline">この商品を本当に削除しても良いですか？</v-card-title>
                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="blue darken-1" text @click="closeDelete">Cancel</v-btn>
                        <v-btn color="blue darken-1" text @click="deleteItemConfirm">OK</v-btn>
                        <v-spacer></v-spacer>
                      </v-card-actions>
                    </v-card>
                  </v-dialog>
                </v-toolbar>
              </template>

              <!-- 編集テーブル -->
              <template v-slot:[`item.actions`]="{ item }">
                <v-icon
                  small
                  class="mr-2"
                  @click="editItem(item)"
                >
                  mdi-pencil
                </v-icon>
                <v-icon
                  small
                  @click="deleteItem(item)"
                >
                  mdi-delete
                </v-icon>
              </template>
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
                  <span class="listTable__heading">商品</span>
                  <span class="listTable__content">¥ {{ totalPrice | addComma }}</span>
                </div>
                <div class="subTotalBlock__list listTable">
                  <span class="listTable__heading">送料</span>
                  <span class="listTable__content">¥ 0</span>
                </div>
              </v-col>
            </v-row>

            <!-- 合計ボタン -->
            <!-- 認証無しの時に表示 -->
            <template v-if="!isAuthenticatedUser">
              <v-container>
                <v-row>
                  <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-btn
                      min-width="100%"
                      color="success"
                      class="mr-4"
                      @click="validate"
                    >
                      会員登録/ログインして購入する
                    </v-btn>
                  </v-col>
                </v-row>
              </v-container>
            </template>
            <!-- 認証あり -->
            <template v-if="isAuthenticatedUser">
              <v-container>
                <v-row>
                  <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-btn
                      min-width="100%"
                      color="success"
                      class="mr-4"
                      @click="goToPage"
                    >
                      確認ページへ
                    </v-btn>
                  </v-col>
                </v-row>
              </v-container>
            </template>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
export default {
  data () {
    return {
      itemQuantity: "",
      totalPrice: 0,
      dialog: false,
      dialogDelete: false,
      editedIndex: -1,
      editedItem: {
        name: '',
        price: 0,
        quantity: 0,
        subtotal: 0,
        itemQuantity: 0
      },
      defaultItem: {
        name: '',
        price: 0,
        quantity: 0,
        subtotal: 0,
        itemQuantity: 0
      },
      deletedItemPk: null,
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
    }
  },
  methods: {
    // ボタン
    validate() {
      // 会員登録/ログイン画面遷移
      this.$router.push('/user_register');
    },
    goToPage() {
      // 確認ページへ遷移
      const id = this.$store.getters.user_id;
      this.$router.push(`/order/cart/furisode/${id}`);
    },
    editItem(item) {
      this.editedIndex = this.cartInfo.indexOf(item);
      this.editedItem = Object.assign({}, item);

      // 在庫数の範囲の連番
      const range = (start, end) => [...Array((end - start) + 1)].map((_, i) => start + i);
      this.itemQuantity = range(1, item.itemQuantity);

      this.dialog = true;
    },
    deleteItem(item) {
      this.editedIndex = this.cartInfo.indexOf(item);
      this.editedItem = Object.assign({}, item);

      // 削除する商品のpk
      this.deletedItemPk = item.pk;
      this.dialogDelete = true;
    },
    deleteItemConfirm() {
      // カート情報削除
      this.cartInfo.splice(this.editedIndex, 1);

      // カート中削除
      this.$store.dispatch('deleteCart', this.deletedItemPk);

      // カート内の情報削除
      this.$store.dispatch('deleteCartInfo', this.deletedItemPk);

      // ダイアログを閉じる/初期化
      this.closeDelete();
    },
    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },
    closeDelete() {
      this.dialogDelete = false;
      this.$nextTick(() => {
        // 合計金額再計算
        this.totalPrice = this.cartInfo.reduce((acc, cur) => {
          return acc + Number(cur.subtotal.replace(/,/g, '').replace(/¥/g, ''));
        }, 0);

        this.editedItem = Object.assign({}, this.defaultItem);

        // 初期化
        this.editedIndex = -1;
      });
    },
    save() {
      if (this.editedIndex > -1) {
        // 値段を数値に戻す
        let moji = String(this.editedItem.price).replace(/,/g, '').replace(/¥/g, '');

        // 編集した内容
        this.editedItem = {
          name: this.editedItem.name,
          price: this.editedItem.price,
          quantity: this.editedItem.quantity,
          subtotal: '¥' + (Number(moji) * this.editedItem.quantity).toLocaleString(),
        }

        // カート内の情報を修正
        Object.assign(this.cartInfo[this.editedIndex], this.editedItem);

        // ItemInfoも合わせて修正
        const id = Object.assign(this.cartInfo[this.editedIndex], this.editedItem).pk;
        const index = this.$store.getters.itemInfo.findIndex(el => el.item_id == id);

        // 編集した内容
        const editedItemInfo = {
          alert: false,
          itemQuantity: this.cartInfo[this.editedIndex].itemQuantity,
          item_id: id,
          item_name: this.cartInfo[this.editedIndex].name,
          item_price: this.cartInfo[this.editedIndex].price,
          item_total: this.cartInfo[this.editedIndex].quantity,
        }

        // ItemInfo修正
        Object.assign(this.$store.getters.itemInfo[index], editedItemInfo);

        // 合計金額表示
        this.totalPrice = this.cartInfo.reduce((acc, cur) => {
          return acc + Number(cur.subtotal.replace(/,/g, '').replace(/¥/g, ''));
        }, 0);
      } else {
        this.cartInfo.push(this.editedItem);
      }
      this.close();
    },
  },
  computed: {
    isAuthenticatedUser() {
      // access_tokenがある場合
      return this.$store.getters.user_access_token != null; 
    },
  },
  watch: {
    dialog(val) {
      val || this.close();
    },
    dialogDelete(val) {
      val || this.closeDelete();
    },
  },
  created() {
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
      }
    });

    // 合計金額表示
    this.totalPrice = this.cartInfo.reduce((acc, cur) => {
      return acc + Number(cur.subtotal.replace(/,/g, '').replace(/¥/g, ''));
    }, 0);
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
.row-select {
  display: flex !important;
  flex-wrap: wrap !important;
  flex: 1 1 auto !important;
  margin-right: -12px !important;
  margin-left: -12px !important;
  justify-content: start !important;
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
</style>