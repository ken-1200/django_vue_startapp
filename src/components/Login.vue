<template>
  <div id="app">
    <v-form
      ref="form"
      v-model="valid"
      lazy-validation
    >

      <v-text-field
        v-model="email"
        :rules="emailRules"
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
        ログインボタン
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
import { loginMixins } from '@/loginMixins';

export default {
  mixins: [ loginMixins ],
  name: 'Login',
  methods: {
    login(){
      this.$store.dispatch('login', {
        store_email: this.email,
        store_password: this.password,
      });
      this.email = "";
      this.password = "";
    },
  }
}
</script>