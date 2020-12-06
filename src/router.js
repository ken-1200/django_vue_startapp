import Vue from 'vue';
import Router from 'vue-router';
import store from './store';

const StoreLogin = () => import(/* webpackChunkName: "StoreLogin" */"./views/StoreLogin.vue");
const ItemList = () => import(/* webpackChunkName: "ItemList" */"./views/ItemList.vue");
const StoreRegister = () => import(/* webpackChunkName: "StoreRegister" */"./views/StoreRegister.vue");
const StoreDashBoard = () => import(/* webpackChunkName: "StoreDashBoard" */"./views/StoreDashBoard.vue");
const ItemRegister = () => import(/* webpackChunkName: "ItemRegister" */"./views/ItemRegister.vue");
const StoreItemList = () => import(/* webpackChunkName: "StoreItemList" */"./views/StoreItemList.vue");
const StoreItemDetail = () => import(/* webpackChunkName: "StoreItemDetail" */"./views/StoreItemDetail.vue");

const UserRegister = () => import(/* webpackChunkName: "UserRegister" */"./views/User/UserRegister.vue");
const UserLogin = () => import(/* webpackChunkName: "UserLogin" */"./views/User/UserLogin.vue");


Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      component: StoreDashBoard,
    },
    {
      path: '/store_register',
      component: StoreRegister,
      beforeEnter(to, from, next) {
        if (store.getters.access_token) {//access_tokenがある場合は登録せず、ダッシュボード画面へ
          next('/');
        } else {
          next();
        }
      }
    },
    {
      path: '/store_login',
      component: StoreLogin,
      beforeEnter(to, from, next) {
        if (store.getters.access_token) {//access_tokenがある場合はログインぜず、ダッシュボード画面へ
          next('/');
        } else {
          next();
        }
      }
    },
    {
      path: '/item_register',
      component: ItemRegister,
      beforeEnter(to, from, next) {
        if (store.getters.access_token) {//access_tokenがない時は、ログイン画面へ
          next();
        } else {
          next('/store_login');
        }
      }
    },
    {
      path: '/item_list',
      component: ItemList
    },
    {
      path: '/item_detail',
      name: 'item_detail',
      component: StoreItemList,
      beforeEnter(to, from, next) {
        if (store.getters.store_id) { // ストアidがない場合は、ダッシュボードへ
          next();
        } else {
          next('/');
        }
      }
    },
    {
      path: '/item_detail/edit/:id',
      component: StoreItemDetail,
      beforeEnter(to, from, next) {
        if (store.getters.store_id) { // ストアidがない場合は、商品詳細へ
          next();
        } else {
          next('/item_detail/');
        }
      }
    },
    {
      path: '/user_register',
      component: UserRegister,
    },
    {
      path: '/user_login',
      component: UserLogin,
    },
    // {
    //   path: '/item_page',
    //   component: Home
    // },
    // {
    //   path: '/item_cart',
    //   component: Home
    // },
    // {
    //   path: '/payment',
    //   component: Home
    // },
    {
      // 定義されていないパスへの対応。トップページへリダイレクトする。
      path: '*',
      redirect: '/'
    }
  ]
})