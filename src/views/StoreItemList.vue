<template>
  <div id="app">
    <!-- 商品詳細一覧 -->
    <h1>商品詳細一覧画面</h1>
    <p v-if="isErrored">{{ error }}</p>
    <div v-for="item in detailItems" :key="item.index">
      <div>id：{{ item.pk }}</div>
      <div>商品名：{{ item.fields.item_name}}</div>
      <div>詳細：{{ item.fields.item_detail}}</div>
      <div>値段：{{ item.fields.item_price}}円</div>
      <div>品数：{{ item.fields.item_total}}個</div>
      <img src=""/>
      <br><br>
      <button @click.stop="itemEdit(item.pk)">編集</button>
      <br>
      <button @click.stop="itemDelete(item.pk)">削除</button>
      <p>{{accessToken}}</p>
      <br><br>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      items: {
        item_id: null,
        item_name: '',
        item_detail: '',
        item_price: null,
        item_total: null,
        item_img: ''
      },
      detailItems: [],
      error: null,
    }
  },
  computed: {
    accessToken() {
      return this.$store.getters.access_token;
    },
    getByStoreId() {
      return this.$store.getters.store_id;
    },
    isErrored() {
      return this.error != null;
    },
  },
  methods: {
    itemEdit(item_id) {
      this.$router.push(`/item_detail/edit/${item_id}`);
    },
    itemDelete(item_id) {
      axios.delete(`/items/${item_id}/delete_item/`, {
        headers: {
          Authorization: `Bearer ${this.accessToken}`
        }
      })
      .then(response => {
        console.log(response.data);
      })
      .catch(error => {
        console.log(error);
        this.error = error;
      });
    },
  },
  // 非同期
  async created() {
    // プロミスが帰って来たら(レスポンス)表示する、またはエラー表示
    await this.$store.dispatch('getItem');
    this.detailItems = this.$store.getters.item_data;
    this.error = this.$store.getters.error;

    // エラー表示
    if (this.detailItems.length != 0) {
      // エラー内容表示(ex)Notfound..)
      this.error = this.$store.getters.error;
    } else {
      // 商品がない時(0個返却された)
      this.error = ' 商品がありません。';
    }
  },
}
</script>