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
              <router-link to="/">仮</router-link>
            </li>
            <li>
              <router-link to="/">ダッシュボード</router-link>
            </li>
          </ul>
        </nav>
        <ul class="globalNav__listBtn">
          <li class="globalNav__listBtnItem">
            <router-link to="/store_register">新規登録</router-link>
          </li>
          <li>
            <router-link to="/store_login">ログイン</router-link>
          </li>
        </ul>
      </div>
    </header>
  </div>
</template>

<script>
export default {
  name: 'Header',
}
</script>

<style lang="scss">
.globalNav {
  align-items: center;
  margin: auto;
  width: 100%;
  height: 71px;
  border-bottom: 1px solid #d9dee6;

  &__wrap {
    display: flex;
    justify-content: start;
    align-items: center;
    padding: 0 20px;
    max-width: 1240px;
    margin: 0 auto;
    height: 72px;
  }

  &__logo {
    font-size: 42px;
    display: flex;

    & img {
      width: 0.7em;
    }

    & .kimono {
      font-size: 23px;
    }
    & .style {
      font-size: 12px;
      color: #444f61;
    }
  }

  &__listBtn {
    margin-left: auto;
  }

  &__listBtnItem,
  &__textNavListItem {
    padding-right: 16px;
  }
}
</style>
