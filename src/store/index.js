import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios'
import router from '../router';

Vue.use(Vuex);

export default new Vuex.Store({
  state: { //初期値
    access_token: null,
    user_access_token: null,
    store_id: null,
    user_id: null,
    userInfo: [],
    storeItemData: [],
    allItemListData: [],
    addToCart: [],
    itemInfo: [],
    paymentInfo: [],
    error: null,
  },
  getters: {
    access_token: state => state.access_token,
    user_access_token: state => state.user_access_token,
    store_id: state => state.store_id,
    user_id: state => state.user_id,
    userInfo: state => state.userInfo,
    storeItemData: state => state.storeItemData,
    allItemListData: state => state.allItemListData,
    selectItems: state => id => {
      return state.allItemListData.filter(el => el.pk === id);
    },
    addToCart: state => state.addToCart,
    itemInfo: state => state.itemInfo,
    paymentInfo: state => state.paymentInfo,
    error: state => state.error,
  },
  mutations: {
    // トークン
    updateAccessToken(state, token) {
      state.access_token = token;
    },
    // ユーザーのトークン
    updateUserAccessToken(state, token) {
      state.user_access_token = token;
    },
    // ストアID
    updateStoreId(state, store_id) {
      state.store_id = store_id;
    },
    // ユーザーID
    updateUserId(state, user_id) {
      state.user_id = user_id;
    },
    // ストア側商品データ
    getItemDetail(state, storeItemData) {
      state.storeItemData = storeItemData;
    },
    // 商品リスト
    getAllItemListData(state, allItemListData) {
      state.allItemListData = allItemListData;
    },
    // カートの中身
    addToCart(state, addToCart) {
      state.addToCart.push(addToCart);
    },
    // 商品情報
    getItemInfo(state, itemInfo) {
      state.itemInfo.push(itemInfo);
    },
    // カート内削除
    deleteCart(state, id) {
      const index = state.addToCart.findIndex(el => el.pk == id);
      if (index >= 0) {
        state.addToCart.splice(index, 1);
      }
    },
    // カート内の情報削除
    deleteCartInfo(state, id) {
      const index = state.itemInfo.findIndex(el => el.item_id == id);
      if (index >= 0) {
        state.itemInfo.splice(index, 1);
      }
    },
    // ユーザー情報を格納
    getUserInfo(state, userInfo) {
      state.userInfo = userInfo;
    },
    // 支払い情報取得
    getPaymentInfo(state, paymentInfo) {
      state.paymentInfo = paymentInfo;
    }
  },
  actions: {
    // オートログイン
    async userAutoLogin({ commit, dispatch }) {
      // ローカルストレージからユーザー情報を取得する
      const userName = localStorage.getItem('userName');
      const userEmail = localStorage.getItem('userEmail');

      // ローカルストレージからユーザーidを取得する
      const userId = localStorage.getItem('userId');

      // ローカルストレージからアクセストークンを取得する
      const accessToken = localStorage.getItem('userRefreshAccessToken');

      // アクセストークンが無い場合
      if (!accessToken) return;

      // 有効期限が切れているか判別
      const now = new Date();

      // 有効期限取得(未来)
      const userExpiryTimeMs = localStorage.getItem('userExpiryTimeMs');

      // 有効期限切れ取得 true/false
      const isExpired = now.getTime() >= userExpiryTimeMs;

      // リフレッシュトークン取得
      const refreshToken = localStorage.getItem('userRefreshToken');

      if (isExpired) {
        // １時間有効期限切れの場合
        await dispatch('userRefreshAccessToken', refreshToken);
        console.log('トークンを更新しました。');
      } else {
        // 有効期限内の場合、残り時間を取得する
        const expiresInMs = userExpiryTimeMs - now.getTime();

        // 残り時間後にトークンをリフレッシュする処理
        setTimeout(() => {
          dispatch('userRefreshAccessToken', refreshToken);
        }, expiresInMs);

        // リフレッシュしたアクセストークンをステートに保存する
        commit('updateUserAccessToken', accessToken);

        // ユーザーidをステートに保存する
        commit('updateUserId', userId);

        // ユーザー情報をステートに保存する
        const userInfo = {
          user_name: userName,
          user_email: userEmail,
        }
        commit('getUserInfo', userInfo);
      }
    },
    // ユーザーログイン
    async userLogin({ dispatch }, loginData) {
      await axios.post('/user_login/', {
        user_email: loginData.user_email,
        password: loginData.password,
      })
      .then(response => {
        console.log(response.data.data);

        // user_id
        const id = response.data.data.user_id;

        dispatch('setUserAuthData', {
          // オブジェクトでユーザー名、メールアドレス、id, 有効期限、アクセス、リフレッシュトークンを渡す
          user_name: response.data.data.user_name,
          user_email: response.data.data.user_email,
          user_id: response.data.data.user_id,
          access_token: response.data.data.access_token,
          refresh_token: response.data.data.refresh_token,
          expires_in: response.data.data.expires_in,
        });

        if (this.getters.addToCart.length != 0) {
          // カートに商品が入っている場合は支払い確認画面
          router.push(`/order/cart/kinomo/${id}`);
        } else {
          // 商品一覧画面
          router.push('/user_home');
        }
      })
      .catch(error => {
        console.log(error);
      });
    },
    // トークンをリフレッシュする為の関数
    async userRefreshAccessToken({ dispatch }, refreshToken) {
      await axios.post('/user_refresh_token/', {
        // リフレッシュトークンを送り、アクセストークンの更新を促す
        'key': refreshToken,
      })
      .then(response => {
        // 更新されたaccess_tokenが帰ってくる
        dispatch('setUserAuthData', {
          // オブジェクトでユーザー名、メールアドレス、id, 有効期限、アクセス、リフレッシュトークンを渡す
          user_name: response.data.data.user_name,
          user_email: response.data.data.user_email,
          user_id: response.data.data.user_id,
          access_token: response.data.data.access_token,
          refresh_token: response.data.data.refresh_token,
          expires_in: response.data.data.expires_in,
        });
      });
    },
    // ローカルストレージにアクセストークンと有効期限時間とリフレッシュトークンを保存し、１時間おきにトークンを更新する
    setUserAuthData({ commit, dispatch }, authData) {
      // 有効期限を決める
      const now = new Date();
      // 1hに設定
      const userExpiryTimeMs = now.getTime() + authData.expires_in * 1000;

      // mutationsを実行し、ステートのアクセストークンに保存する
      commit('updateUserAccessToken', authData.access_token);

      // mutationsを実行し、ステートのユーザーidに保存する
      commit('updateUserId', authData.user_id);

      // ユーザー情報を格納
      const userInfo = {
        user_name: authData.user_name,
        user_email: authData.user_email,
      }
      commit('getUserInfo', userInfo);

      // ローカルストレージにユーザー名、メールさドレス、id、アクセストークンと有効期限時間とリフレッシュトークンを保存する(有効期限(12H)も保存)
      localStorage.setItem('userName', authData.user_name);
      localStorage.setItem('userEmail', authData.user_email);
      localStorage.setItem('userId', authData.user_id);
      localStorage.setItem('userRefreshAccessToken', authData.access_token);
      localStorage.setItem('userRefreshToken', authData.refresh_token);
      localStorage.setItem('userExpiryTimeMs', userExpiryTimeMs);

      // リフレッシュトークンを使って、1時間置きにトークンを更新する
      setTimeout(() => {
        dispatch('userRefreshAccessToken', authData.refresh_token);
        console.log('1時間おきに更新しました。');
      }, authData.expires_in * 1000);
    },
    // ログアウト
    user_logout({ commit }) {
      // AccessTokenを削除
      commit('updateUserAccessToken', null);

      // userIdを削除
      commit('updateUserId', null);

      // ユーザー情報を削除
      commit('getUserInfo', null);

      // ローカルストレージから各アイテムを削除
      localStorage.removeItem('userName');
      localStorage.removeItem('userEmail');
      localStorage.removeItem('userId');
      localStorage.removeItem('userRefreshAccessToken');
      localStorage.removeItem('userRefreshToken');
      localStorage.removeItem('userExpiryTimeMs');

      // DashBoardに遷移する
      router.push('/');
    },
    // 商品リスト取得
    async getItemList({ commit }) {
      await axios.get('/all/items_list/')
      .then(response => {
        console.log(response);
        // コミット実行で商品リストを格納
        commit('getAllItemListData', response.data);
      })
      .catch(error => {
        // エラー処理
        this.getters.error = `商品が見つかりませんでした。${error}`;
        console.log(error);
      })
    },
    // カートの処理/制御
    addToCart({ state, commit }, itemData) {
      // idに紐づく商品情報を取得する
      const data = state.allItemListData.filter(el => el.pk == itemData.item_id);

      // 同じ商品をカートに入れた時は既に入っているという旨の警告を出す
      const sameItem = state.addToCart.find(el => el.pk == itemData.item_id);

      if (!sameItem) {
        // カートに格納
        commit('addToCart', data[0]);

        // 数量を格納
        commit('getItemInfo', itemData);

        // ページ遷移
        router.push('/order/cart/kinomo');
      } else {
        // アラートを表示
        itemData.alert = true;

        // 1分後解除
        if (itemData.alert) {
          setTimeout(() => {
            itemData.alert = false;
          }, 60000);
        }
      }

      // カートに入れた後の商品一覧の在庫数を減らす
      const quantity = state.allItemListData.find(el => el.pk == itemData.item_id);

      // 商品一覧の在庫数からカート内の商品数を引く
      quantity.fields.item_total -= itemData.item_total;
    },
    // カート内削除
    deleteCart({ commit }, id) {
      commit('deleteCart', id);
    },
    // カート内の情報削除
    deleteCartInfo({ commit }, id) {
      commit('deleteCartInfo', id);
    },
    // 購入する
    // payment() {
      
    // }

/* ストア側の処理
  - 商品取得
  - オートログイン
  - ログイン
  - ログアウト
  - リフレッシュトークン
  - ローカルストレージにアクセストークンと有効期限時間とリフレッシュトークンを保存し、１時間おきにトークンを更新する
*/

    // 商品取得
    async getItem({ commit }) {
      await axios.get(`/items/get_item_detail/?page=${this.getters.store_id}`, {
        // 第二引数にヘッダー //ユーザー側の認証もしくは、認証しない状態でのアクセス可能なエンドポイントに変更 
        headers: {
          Authorization: `Bearer ${this.getters.access_token}`
        }
      })
      .then(response => {
        console.log(response.data);
        // コミット実行で、商品データを格納
        commit('getItemDetail', response.data);
      })
      .catch(error => {
        // エラー処理
        this.getters.error = `商品が見つかりませんでした。${error}`;
        console.log(error);
      });
    },
    // オートログイン
    async autoLogin({ commit, dispatch }) {
      // ローカルストレージからストアidを取得する
      const StoreId = localStorage.getItem('StoreId');

      // ローカルストレージからアクセストークンを取得する
      const accessToken = localStorage.getItem('refreshAccessToken');

      // アクセストークンが無い場合
      if (!accessToken) return;

      // 有効期限が切れているか判別
      const now = new Date();

      // 有効期限取得(未来)
      const expiryTimeMs = localStorage.getItem('expiryTimeMs');

      // 有効期限切れ取得 true/false
      const isExpired = now.getTime() >= expiryTimeMs;

      // リフレッシュトークン取得
      const refreshToken = localStorage.getItem('refreshToken');

      if (isExpired) {
        // １時間有効期限切れの場合
        await dispatch('refreshAccessToken', refreshToken);
        console.log('トークンを更新しました。');
      } else {
        // 有効期限内の場合、残り時間を取得する
        const expiresInMs = expiryTimeMs - now.getTime();

        // 残り時間後にトークンをリフレッシュする処理
        setTimeout(() => {
          dispatch('refreshAccessToken', refreshToken);
        }, expiresInMs);

        // リフレッシュしたアクセストークンをステートに保存する
        commit('updateAccessToken', accessToken);

        // ストアidをステートに保存する
        commit('updateStoreId', StoreId);
      }
    },
    // ログイン
    async login({ dispatch }, loginData) {
      await axios.post('store_login/', {
        store_email: loginData.store_email,
        store_password: loginData.store_password
      })
      .then(response => {
        console.log(response.data.data);
        dispatch('setAuthData', {
          // オブジェクトでid, 有効期限、アクセス、リフレッシュトークンを渡す
          store_id: response.data.data.store_id,
          access_token: response.data.data.access_token,
          refresh_token: response.data.data.refresh_token,
          expires_in: response.data.data.expires_in,
        });
        // ストアホーム画面に遷移
        router.push('/store_home');
      })
      .catch(error => {
        // ここもう少し改善余地あり1/3
        console.log(error);
        router.push('/store_register');
      });
    },
    // ログアウト
    logout({ commit }) {
      // AccessTokenを削除
      commit('updateAccessToken', null);

      // StoreIdを削除
      commit('updateStoreId', null);

      // ItemDataを削除
      commit('getItemDetail', []);

      // ローカルストレージから各アイテムを削除
      localStorage.removeItem('StoreId');
      localStorage.removeItem('refreshAccessToken');
      localStorage.removeItem('expiryTimeMs');
      localStorage.removeItem('refreshToken');

      // DashBoardに遷移する
      router.push('/');
    },
    // トークンをリフレッシュする為の関数
    async refreshAccessToken({ dispatch }, refreshToken) {
      await axios.post('/refresh_token/', {
        // リフレッシュトークンを送り、アクセストークンの更新を促す
        'refresh_key': refreshToken,
      })
      .then(response => {
        // 更新されたaccess_tokenが帰ってくる
        dispatch('setAuthData', {
          // オブジェクトで有効期限、アクセス、リフレッシュトークンを渡す
          store_id: response.data.data.store_user_id,
          access_token: response.data.data.access_token,
          refresh_token: response.data.data.refresh_token,
          expires_in: response.data.data.expires_in,
        });
      });
    },
    // ローカルストレージにアクセストークンと有効期限時間とリフレッシュトークンを保存し、１時間おきにトークンを更新する
    setAuthData({ commit, dispatch }, authData) {
      // 有効期限を決める
      const now = new Date();
      // 1hに設定
      const expiryTimeMs = now.getTime() + authData.expires_in * 1000;

      // mutationsを実行し、ステートのアクセストークンに保存する
      commit('updateAccessToken', authData.access_token);

      // mutationsを実行し、ステートのストアidに保存する
      commit('updateStoreId', authData.store_id);

      // ローカルストレージにアクセストークンと有効期限時間とリフレッシュトークンを保存する(有効期限(12H)も保存)
      localStorage.setItem('StoreId', authData.store_id);
      localStorage.setItem('refreshAccessToken', authData.access_token);
      localStorage.setItem('refreshToken', authData.refresh_token);
      localStorage.setItem('expiryTimeMs', expiryTimeMs);

      // リフレッシュトークンを使って、1時間置きにトークンを更新する
      setTimeout(() => {
        dispatch('refreshAccessToken', authData.refresh_token);
        console.log('1時間おきに更新しました。')
      }, authData.expires_in * 1000);
    }
  }
})