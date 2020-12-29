<template>
<!-- バー -->
  <v-app-bar
    app
    fixed
    max-height="112"
    color="#ECEFF1"
    elevate-on-scroll
  >

  <!-- 左のアイコン -->
    <v-app-bar-nav-icon>
      <img src="../../assets/logo.png" alt="">
    </v-app-bar-nav-icon>

  <!-- タイトル -->
    <v-toolbar-title
      id="toolbar__title"
    >
      <router-link
        to="/"
        class="toolbar__link"
      >
        Kimono
      </router-link>
      <span
        class="toolbar__style"
      >
        STYLE
      </span>
    </v-toolbar-title>

    <v-spacer></v-spacer>

  <!-- ３点ドットリスト -->
    <v-menu
      bottom
      left
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          icon
          v-bind="attrs"
          v-on="on"
        >
          <v-icon>mdi-dots-vertical</v-icon>
        </v-btn>
      </template>

      <v-list>
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
          @click="clickMenu(i)"
        >
          <v-list-item-title>
            <v-row
              align="center"
              justify="space-around"
            >
              <v-btn depressed>
                {{ item.title }}
              </v-btn>
            </v-row>
          </v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>

<!-- タブバー -->
    <template v-slot:extension>
      <v-tabs
        center-active
        grow
      >
        <v-tab to="/item_register">
          PRODUCT CREATE
        </v-tab>
        <v-tab :to="{ name: 'item_detail', query: { page: $store.getters.store_id } }">
          PRODUCT DETAIL
        </v-tab>
        <v-tab>
          ABOUT
        </v-tab>
        <v-tab>
          BLOG
        </v-tab>
        <v-tab>
          CATEGORY
        </v-tab>
        <v-tab @click.prevent="logout()">
          LOGOUT
        </v-tab>
      </v-tabs>
    </template>
  </v-app-bar>
</template>

<script>
export default {
  name: 'StoreDashBoardHeader',
  data() {
    return {
      items: [
        { title: 'ショップ設定'},
        { title: '商品を登録' },
        { title: '商品をみる' },
        { title: 'ログアウト' },         
      ],
    }
  },
  methods: {
    clickMenu(index) {
      switch (index) {
        case 0:
          this.$router.push('/');
          break;
        case 1:
          this.$router.push('/item_register');
          break;        
        case 2:
          this.$router.push({ name: 'item_detail', query: { page: this.$store.getters.store_id } });
          break;
        case 3:
          this.logout();
          break;
        default:
          this.$router.push('/');
      }
    },
    logout() {
      this.$store.dispatch('logout');
    },
  }
}
</script>