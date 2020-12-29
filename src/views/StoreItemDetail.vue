<template>
  <div id="app">
    <!-- 商品詳細 -->
    <p v-if="isErrored">{{ error }}</p>
    <v-form
      ref="form"
      v-model="valid"
      lazy-validation
    >
      <v-text-field
        v-model.trim="items.item_name"
        v-bind="items"
        :counter="30"
        :rules="nameRules"
        label="商品名"
        prepend-icon="mdi-shopping"
        required
      ></v-text-field>

      <v-file-input
        label="写真"
        filled
        placeholder="クリックしてください。"
        prepend-icon="mdi-camera"
        background-color="#fbfbfb"
      ></v-file-input>

      <v-textarea
        v-model.trim="items.item_detail"
        v-bind="items"
        :rules="detailRules"
        hint="詳細は500文字以下である必要があります。"
        counter
        label="詳細"
        prepend-icon="mdi-form-textarea"
      ></v-textarea>

      <v-text-field
        v-model.number="items.item_price"
        v-bind="items"
        :rules="priceRules"
        name="input-10-1"
        label="値段"
        type="number"
        max="10000000"
        min="100"
        prepend-icon="mdi-currency-jpy"
        counter
        required
      ></v-text-field>

      <v-text-field
        v-model.number="items.item_total"
        v-bind="items"
        :rules="totalRules"
        name="input-10-1"
        label="品数"
        type="number"
        prepend-icon="mdi-paper-cut-vertical"
        max="100"
        min="1"
        counter
        required
      ></v-text-field>

      <v-btn
        :disabled="!valid"
        :loading="loading"
        color="success"
        class="mr-4"
        @click="validate"
      >
        編集ボタン
      </v-btn>

      <v-btn
        color="error"
        class="mr-4"
        @click="reset"
      >
        リセットボタン
      </v-btn>
    </v-form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      items: {
        item_id: this.$route.params.id,
        item_name: '',
        item_detail: '',
        item_price: null,
        item_total: null,
        item_img: '',
      },
      error: null,
      valid: true,
      loading: false,
      nameRules: [
        v => Boolean(v) || '商品名は必須です。',
        v => (v && v.length <= 30) || '商品名は30文字以下である必要があります。',
      ],
      detailRules: [
        v => Boolean(v) || '詳細は必須です。',
        v => (v && v.length <= 500) || '詳細は500文字以下である必要があります。'
      ],
      priceRules: [
        v => Boolean(v) || '値段は必須です。',
        v => v >= 100 || '100円から登録可能です',
        v => v <= 10000000 || '1000万円まで登録可能です',
      ],
      totalRules: [
        v => Boolean(v) || '品数は必須です。',
        v => v != 0 || '1個から登録可能です',
        v => v <= 100 || '100個まで登録可能です',
      ],
    }
  },
  computed: {
    accessToken() {
      return this.$store.getters.access_token;
    },
    isErrored() {
      return this.error != null;
    },
  },
  methods: {
    // Promissが帰ってくるまで、商品一覧に遷移しない処理
    async updateItem() {
      await axios.patch(`/items/${this.$route.params.id}/update_item/`, {
        // オブジェクトを送る
        item_id: this.items.item_id,
        item_name: this.items.item_name,
        item_detail: this.items.item_detail,
        item_price: this.items.item_price,
        item_total: this.items.item_total,
        item_img: this.items.item_img,
      }, {
        headers: {
          Authorization: `Bearer ${this.accessToken}`
        }
      })
      .then(response => {
        console.log(response.data);
        // 商品一覧（オーナーのみ）に遷移する
        this.$router.push('/item_detail/')
      })
      .catch(error => {
        console.log(error);
        this.error = error;
      });
    },
    // ボタン
    validate() {
      // 空文字の場合
      if (this.items.item_name == "" || this.items.item_name == undefined) return;

      // 入力値の検証と商品の編集
      this.$refs.form.validate();
      this.updateItem();
    },
    reset() {
      // リセット、エラー文字を削除
      this.$refs.form.reset();
    },
  },
  async created() {
    // 商品取得
    await this.$store.dispatch('getItem');
    // Vuex gettersからオーナーの商品リストを取得する
    const allItemData = this.$store.getters.item_data;
    // 該当アイテムを取得
    const getApplicableItem = allItemData.filter(element => element.pk == this.$route.params.id);

    // itemsに該当アイテム情報を格納
    getApplicableItem.forEach(el => {
      this.items = {
        item_id: this.$route.params.id,
        item_name: el.fields.item_name,
        item_detail: el.fields.item_detail,
        item_price: el.fields.item_price,
        item_total: el.fields.item_total,
        item_img: el.fields.item_img,
      }
      console.log(this.items);
    });
  },
}
</script>