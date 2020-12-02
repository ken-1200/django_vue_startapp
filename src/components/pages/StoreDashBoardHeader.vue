<template>
  <div id="app">
    <header class='globalNav'>
      <div class="globalNav__wrap">
        <div class="globalNav__logo">
          <router-link to="/">
            <img src="../../assets/logo.png" alt="logo" class="globalNav__logo img">
          </router-link>
          <span class="globalNav__logo kimono">KIMONO</span>
          <span class="globalNav__logo style">STYLE</span>
        </div>
        <nav class="globalNav__textNav">
          <ul class="globalNav__textNavList">
            <li class="globalNav__textNavListItem">
              <router-link to="/item_list">商品一覧</router-link>
            </li>
            <li>
              <router-link to="/">ホーム</router-link>
            </li>
          </ul>
        </nav>
        <!-- dorpdownメニュー -->
        <ul class="globalNav__listBtn">
          <li class="globalNav__listBtnItem">
            <router-link to="/">ショップ設定</router-link><br>
            <router-link to="/item_register">商品を登録</router-link><br>
            <router-link :to="{ name: 'item_detail', query: { page: $store.getters.store_id } }">商品をみる</router-link>
          </li>
          <li>
            <router-link to="/">ユーザー情報</router-link>
          </li>
          <li>
            <router-link to="/">設定</router-link>
          </li>
          <li>
            <a @click="logout()">ログアウト</a>
          </li>
        </ul>
      </div>
    </header>
  </div>
</template>

<script>
export default {
  name: 'StoreDashBoardHeader',
  // beforeRouteEnter (to, from, next) {
  //     next(vm => {
  //       console.log(vm);
  //       `item_detail/${vm.id}`
  //     });
  // },
  methods: {
    logout() {
      this.$store.dispatch('logout');
    },
  }
}
</script>