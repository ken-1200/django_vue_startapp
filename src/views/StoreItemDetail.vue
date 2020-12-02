<template>
  <div id="app">
    <!-- <p>{{ getItem }}</p> -->
    <div v-for="item in getItemName" :key="item.index">
      <p>{{item.pk}}</p>
      <p>{{getItemName}}</p>
      <p>id: {{ $route.params.id }}</p>
    </div>
    <p><label>商品名：<input type="text" name="name" size="40" placeholder="商品名" required=true :value="getItemName" change="items.item_name"></label></p>
    <p><label>詳細：<input v-model="items.item_detail" id="item_detail" type="text" name="item_detail" size="30" maxlength="40" placeholder="詳細" required=true></label></p>
    <p><label>値段：<input v-model="items.item_price" id="item_price" type="number" name="item_price" size="10" maxlength="16" placeholder="値段" required=true></label></p>
    <p><label>品数：<input v-model="items.item_total" id="item_total" type="number" name="item_total" size="10" maxlength="16" placeholder="品数" required=true></label></p>
    <p><label>画像：<input v-model="items.item_img" id="item_img" type="image" name="item_img" size="10" maxlength="16" placeholder="画像"></label></p>
    <button @click.stop="itemEdit">商品を編集する</button>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  props: ['id'],
  data() {
    return {
      items: {
        item_id: null,
        item_name: '',
        item_detail: '',
        item_price: null,
        item_total: null,
        item_img: '',
      },
      getItems: []
    }
  },
  computed: {
    accessToken() {
      return this.$store.getters.access_token;
    },
    getByStoreId() {
      return this.$store.getters.store_id;
    },
    getItem() {
      return this.$store.getters.item_data;
    },
    getItemName() {
      return this.$store.getters.item_data;
    }
  },
  methods: {
    itemEdit() {
      axios.post(`/items/1/update_item/`, {
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
        this.detailItems = response.data
      })
      .catch(error => {
        console.log(error);
      });
    }
  },
}
</script>