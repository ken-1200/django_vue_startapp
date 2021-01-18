import Vue from 'vue';
import Router from 'vue-router';
import store from './store';

const StoreLogin = () => import(/* webpackChunkName: "StoreLogin" */"./views/StoreLogin.vue");
const ItemList = () => import(/* webpackChunkName: "ItemList" */"./views/ItemList.vue");
const StoreRegister = () => import(/* webpackChunkName: "StoreRegister" */"./views/StoreRegister.vue");
const DashBoard = () => import(/* webpackChunkName: "DashBoard" */"./views/DashBoard.vue");
const ItemRegister = () => import(/* webpackChunkName: "ItemRegister" */"./views/ItemRegister.vue");
const StoreItemList = () => import(/* webpackChunkName: "StoreItemList" */"./views/StoreItemList.vue");
const StoreItemDetail = () => import(/* webpackChunkName: "StoreItemDetail" */"./views/StoreItemDetail.vue");
const ItemDetail = () => import(/* webpackChunkName: "ItemDetail" */"./views/ItemDetail.vue");
const ItemCart = () => import(/* webpackChunkName: "ItemCart" */"./views/ItemCart.vue");
const ItemCartOrder = () => import(/* webpackChunkName: "ItemCartOrder" */"./views/ItemCartOrder.vue");
const PaymentConfirmed = () => import(/* webpackChunkName: "PaymentConfirmed" */"./views/PaymentConfirmed.vue");
const StoreHomePage = () => import(/* webpackChunkName: "StoreHomePage" */"./views/StoreHomePage.vue");
const OrderHistory = () => import(/* webpackChunkName: "OrderHistory" */"./views/OrderHistory.vue");

const UserRegister = () => import(/* webpackChunkName: "UserRegister" */"./views/User/UserRegister.vue");
const UserLogin = () => import(/* webpackChunkName: "UserLogin" */"./views/User/UserLogin.vue");
const UserHomePage = () => import(/* webpackChunkName: "UserHomePage" */"./views/User/UserHomePage.vue");


Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      component: DashBoard,
    },
    {
      path: '/store_register',
      component: StoreRegister,
      // beforeEnter(to, from, next) {
      //   if (store.getters.access_token) {//access_tokenがある場合は登録せず、ダッシュボード画面へ
      //     next('/');
      //   } else {
      //     next();
      //   }
      // }
    },
    {
      path: '/store_login',
      component: StoreLogin,
      // beforeEnter(to, from, next) {
      //   if (store.getters.access_token) {//access_tokenがある場合はログインぜず、ダッシュボード画面へ
      //     next('/');
      //   } else {
      //     next();
      //   }
      // }
    },
    {
      path: '/store_home',
      component: StoreHomePage,
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
          next('/item_detail');
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
    {
      path: '/user_home',
      component: UserHomePage,
      beforeEnter(to, from, next) {
        if (store.getters.user_access_token) { // ユーザートークンがない場合は、ダッシュボードへ
          next();
        } else {
          next('/');
        }
      }
    },
    {
      path: '/items/:id',
      component: ItemDetail,
    },
    {
      path: '/order/cart/furisode',
      component: ItemCart,
    },
    {
      path: '/order/cart/furisode/:id',
      component: ItemCartOrder,
      beforeEnter(to, from, next) {
        if (store.getters.user_access_token) { // ユーザートークンがない場合は、ダッシュボードへ
          next();
        } else {
          next('/');
        }
      }
    },
    {
      path: '/payment',
      component: PaymentConfirmed,
      beforeEnter(to, from, next) {
        if (store.getters.user_access_token) { // ユーザートークンがない場合は、ダッシュボードへ
          next();
        } else {
          next('/');
        }
      }
    },
    {
      path: '/member/order/history',
      component: OrderHistory,
      beforeEnter(to, from, next) {
        if (store.getters.user_access_token) { // ユーザートークンがない場合は、ダッシュボードへ
          next();
        } else {
          next('/');
        }
      }
    },
    {
      // 定義されていないパスへの対応
      path: '*',
      beforeEnter(to, from, next) {
        if (store.getters.access_token) { // ストアのトークンがある場合は、ストアホームへ
          next('/store_home');
        } else if (store.getters.user_access_token) { // ユーザーのトークンがある場合は、ユーザーホームへ
          next('/user_home');
        } else { // それ以外はダッシュボード画面へ
          next('/');
        }
      }
    }
  ],
  scrollBehavior (to, from, savedPosition) {
    // スクロール位置を記憶している場合はその位置を返す
    if (savedPosition) {
      return new Promise((resolve) => {
        // トランジションあり
        this.app.$root.$once('triggerScroll', () => {
          resolve(savedPosition);
        });
      });
    } else {
      // それ以外は、先頭の位置を返す
      return { x: 0, y: 0 };
    }
  }
});