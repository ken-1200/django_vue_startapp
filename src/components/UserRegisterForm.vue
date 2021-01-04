<template>
  <div id="app">
    <v-form
      ref="form"
      v-model="valid"
      lazy-validation
    >
      <v-text-field
        v-model="name"
        :counter="30"
        :rules="nameRules"
        :error-messages="errorName"
        label="Name"
        prepend-icon="mdi-account"
        required
      ></v-text-field>
  
      <v-text-field
        v-model="email"
        :rules="emailRules"
        :error-messages="errorEmail"
        label="E-mail"
        prepend-icon="mdi-email"
        required
      ></v-text-field>

      <v-text-field
        v-model="password"
        :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
        :rules="passRules"
        :type="show ? 'text' : 'password'"
        name="input-10-1"
        label="Password"
        hint="８文字以上必要です。"
        counter
        prepend-icon="mdi-lock"
        @click:append="show = !show"
        required
      ></v-text-field>

      <v-btn
        :disabled="!valid"
        :loading="loading"
        color="success"
        class="mr-4"
        @click="validate"
      >
        登録する
      </v-btn>

      <v-btn
        color="error"
        class="mr-4"
        @click="reset"
      >
        修正する
      </v-btn>

      <v-btn
        :loading="loading"
        color="primary"
        class="mr-4"
        @click="loginButton"
      >
        登録済みの方はこちらから
      </v-btn>
    </v-form>
  </div>
</template>

<script>
import axios from 'axios';
import { formMixins } from '@/formMixins';

export default {
  mixins: [ formMixins ],
  name: 'UserRegisterForm',
  methods: {
    // 登録
    async register(){
      this.sending = true;
      await axios.post('/users/create_user/', {
        // オブジェクトを送る
        user_name: this.name,
        user_email: this.email,
        password: this.password,
      })
      .then(response => {
        this.$router.push('/user_login');
        console.log(response.data);
      })
      .catch(error => {
        this.onError(error);
      });
      // ローディング、テキスト解除
      this.loading = false;
      this.name = "";
      this.email = "";
      this.password = "";
    },
    onError(error) {
      // エラー内容を変数に格納
      const name = error.response.data.user_name;
      const email = error.response.data.user_email;

      // ステータス400以外返却時
      if (!(error.response.status == 400)) {
        window.alert(error.message);
      }

      // ステータス400返却時
      else if (Boolean(name) && Boolean(email)) {
        // 両方エラーの場合
        this.errorName = "この名前は既に存在します。";
        this.errorEmail = "このメールアドレスは既に存在します。";
      } else {
        // 片方がエラーの場合
        !name ? this.errorEmail = "このメールアドレスは既に存在します。" : this.errorName = "この名前は既に存在します。";
      }

      // 3.6s後にリセット
      setTimeout(() => {
        this.reset();
      }, 3600);
    },
    loginButton() {
      // login画面に遷移
      this.$router.push('/user_login');
    },
  }
};
</script>