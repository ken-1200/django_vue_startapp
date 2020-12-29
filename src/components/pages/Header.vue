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
        <v-tab to="/item_list">
          HOME
        </v-tab>
        <v-tab to="/">
          SHOP OWNER
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
        <v-tab>
          CONTACT
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
        { title: '新規登録'},
        { title: 'ログイン' },
      ],
      home: "/item_list",
      shopOwner: "/",
    }
  },
  methods: {
    clickMenu(index) {
      switch (index) {
        case 0:
          this.$router.push('/store_register');
          break;
        case 1:
          this.$router.push('/store_login');
          break;
        default:
          this.$router.push('/');
      }
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

  &__style {
    font-size: 12px;
    color: $cSubBlack;
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
