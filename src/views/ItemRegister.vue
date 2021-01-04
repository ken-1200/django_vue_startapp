<template>
  <div id="app">
    <!-- 商品投稿 -->
    <v-card-title>商品を登録する</v-card-title>
    <v-card-subtitle>あなただけの商品を登録しましょう</v-card-subtitle>

    <!-- フォーム -->
    <v-form
      ref="form"
      v-model="valid"
      lazy-validation
    >
      <v-text-field
        v-model="name"
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
        v-model="detail"
        :rules="detailRules"
        :placeholder="detailPlaceholder"
        hint="詳細は500文字以下である必要があります。"
        counter
        label="詳細"
        prepend-icon="mdi-form-textarea"
      ></v-textarea>

      <v-text-field
        v-model.number="price"
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
        v-model.number="total"
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
        登録ボタン
      </v-btn>

      <v-btn
        color="error"
        class="mr-4"
        @click="reset"
      >
        編集ボタン
      </v-btn>
    </v-form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      name: "",
      detail: "",
      detailPlaceholder: "ちょうど良いウエイトの裏起毛生地、クラシックシルエットのフーディに、都会的なグラフィックがシルクスクリーンで施されたアイテム。厳選された生地色とプリントカラーはデザイン性に優れ、一年を通し、トレーニングウェアから、街着まで、様々なシーンで重宝する。",
      price: null,
      total: null,
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
    }
  },
  methods: {
    createdItems() {
      axios.post('/item_list/', {
        item_name: this.name,
        item_detail: this.detail,
        item_price: this.price,
        item_total: this.total,
      }, {
        headers: {
          Authorization: `Bearer ${this.accessToken}`
        }
      })
      .then(response => {
        console.log(response);
      })
      .catch(error => {
        console.log(error);
      })
      this.$router.push('/');
    },
    // ボタン
    validate() {
      // 空文字の場合
      if (this.name == "" || this.name == undefined) return;

      // 入力値の検証と商品の登録
      this.$refs.form.validate();
      this.createdItems();
    },
    reset() {
      // リセット、エラー文字を削除
      this.$refs.form.reset();
    },
  },
}
</script>