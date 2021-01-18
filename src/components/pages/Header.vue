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
      <img src="../../assets/logo.png" alt="" @click="goToHome">
    </v-app-bar-nav-icon>

  <!-- タイトル -->
    <v-toolbar-title
      id="toolbar__title"
    >
      <router-link
        to="/"
        class="toolbar__link"
      >
        FURISODE
      </router-link>
      <!-- <span
        class="toolbar__style"
      >
        STYLE
      </span> -->
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
          @click.stop="clickMenu(i)"
        >
          <v-list-item-title>
            <v-row
              align="center"
              justify="space-around"
            >
              <v-btn
                class="ma-2"
                color="success"
                depressed
              >
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
        <v-tab to="/">
          HOME
        </v-tab>
        <v-tab to="/item_list">
          SHOP LISTS
        </v-tab>
        <v-tab>
          ABOUT(仮)
        </v-tab>
        <v-tab>
          BLOG(仮)
        </v-tab>
        <v-tab>
          CATEGORY(仮)
        </v-tab>
        <v-tab>
          CONTACT(仮)
        </v-tab>
      </v-tabs>
    </template>
  </v-app-bar>
</template>

<script>
export default {
  name: 'Header',
  data() {
    return {
      items: [
        { title: 'ショップオーナー'},
        { title: 'ユーザーログイン' },
      ],
    }
  },
  methods: {
    clickMenu(index) {
      switch (index) {
        case 0:
          this.$router.push('/store_login');
          break;
        case 1:
          this.$router.push('/user_login');
          break;
        default:
          this.$router.push('/');
      }
    },
    goToHome() {
      // ホーム画面遷移時コールバック関数を呼びエラー回避
      this.$router.push('/', () => {});
    }
  }
}
</script>

<style lang="scss">
#toolbar {
  &__title {
    padding-left: 7px;
    padding-top: 0px;
    padding-bottom: 0px;
    display: flex;
  }
}
.toolbar {
  &__link {
    color: $cVueBlack !important;
    font-weight: 400;
    font-size: 1.7rem;
    font-family: "YuMincho" !important;
  }
}
.tabs {
  &__link {
    color: rgba(0,0,0,.54) !important;
  }
}
img {
  width: 3.2em;
}
</style>
