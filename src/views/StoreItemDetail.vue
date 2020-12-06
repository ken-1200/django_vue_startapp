<template>
  <div id="app">
    <!-- 商品詳細 -->
    <p v-if="isErrored">{{ error }}</p>
    <p><label>商品名：<input v-model="items.item_name" v-bind="items" id="item_name" type="text" name="name" size="40" placeholder="商品名" required=true></label></p>
    <p><label>詳細：<input v-model="items.item_detail" v-bind="items" id="item_detail" type="text" name="item_detail" size="30" maxlength="40" placeholder="詳細" required=true></label></p>
    <p><label>値段：<input v-model="items.item_price" v-bind="items" id="item_price" type="number" name="item_price" size="10" maxlength="16" placeholder="値段" required=true></label></p>
    <p><label>品数：<input v-model="items.item_total" v-bind="items" id="item_total" type="number" name="item_total" size="10" maxlength="16" placeholder="品数" required=true></label></p>
    <p><label>画像：<input v-model="items.item_img" v-bind="items" id="item_img" type="image" name="item_img" size="10" maxlength="16" placeholder="画像"></label></p>
    <button @click.stop="updateItem">商品を編集する</button>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      items: {
        item_id: this.$route.params.id,
        item_name: '',
        item_detail: '',
        item_price: null,
        item_total: null,
        item_img: '',
      },
      error: null,
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
  methods: {
    // Promissが帰ってくるまで、商品一覧に遷移しない処理
    async updateItem() {
      await axios.patch(`/items/${this.$route.params.id}/update_item/`, {
        // オブジェクトを送る
        item_id: this.items.item_id,
        item_name: this.items.item_name,
        item_detail: this.items.item_detail,
        item_price: this.items.item_price,
        item_total: this.items.item_total,
        item_img: this.items.item_img,
      }, {
        headers: {
          Authorization: `Bearer ${this.accessToken}`
        }
      })
      .then(response => {
        console.log(response.data);
        // 商品一覧（オーナーのみ）に遷移する
        this.$router.push('/item_detail/')
      })
      .catch(error => {
        console.log(error);
        this.error = error;
      });
    }
  },
  created() {
    // Vuex gettersからオーナーの商品リストを取得する
    const allItemData = this.$store.getters.item_data;
    // 該当アイテムを取得
    const getApplicableItem = allItemData.filter(element => element.pk == this.$route.params.id);

    // itemsに該当アイテム情報を格納
    getApplicableItem.forEach(el => {
      this.items = {
        item_id: this.$route.params.id,
        item_name: el.fields.item_name,
        item_detail: el.fields.item_detail,
        item_price: el.fields.item_price,
        item_total: el.fields.item_total,
        item_img: el.fields.item_img,
      }
      console.log(this.items);
    });
  },
}
</script>