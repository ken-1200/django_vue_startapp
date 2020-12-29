export const loginMixins = {
  data() {
    return {
      email: "",
      password: "",
      valid: true,
      show: false,
      loading: false,
      emailRules: [
        v => Boolean(v) || 'E-mailは必須です。',
        v => /.+@.+\..+/.test(v) || '',
      ],
      passRules: [
        v => Boolean(v) || 'パスワードは必須です。',
      ]
    }
  },
  methods: {
    // ボタン
    validate() {
      // 空文字の場合
      if (this.email == "" || this.email == undefined) return;

      // 入力値の検証とログイン
      this.$refs.form.validate();
      this.login();
    },
    reset() {
      // リセット、エラー文字を削除
      this.$refs.form.reset();
    },
  },
}