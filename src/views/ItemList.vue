<template>
  <div id="app">
    <ul>
      <li>
        <router-link to="/user_register">ユーザー登録</router-link>
      <li>
        <router-link to="/user_login">ユーザーLogin</router-link>
      </li> 
      <li>
        <a @click="logout()">ユーザーログアウト</a>
      </li>
    </ul>
    <hr>
    <!-- 商品一覧 -->
    <h1>商品一覧画面</h1>
    <div v-for="item in items" :key="item.index">
      <div>商品名：{{ item.fields.item_name}}</div>
      <div>詳細：{{ item.fields.item_detail}}</div>
      <div>値段：{{ item.fields.item_price}}円</div>
      <div>品数：{{ item.fields.item_total}}個</div>
      <img src=""/>
      <br><br>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      items: [],
    }
  },
  methods: {
    logout() {
      this.$store.dispatch('user_logout');
    },
  },
  created() {
    // ここは、ユーザー側、ストア側両方が見れる商品一覧
    axios.get('/all/items_list/')
    .then(response => {
      console.log(response.data)
      this.items = response.data
    })
    .catch(error => {
      console.log(error)
    });
  },
}
</script>