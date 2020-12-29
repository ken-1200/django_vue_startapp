export const formMixins = {
  data() {
    return {
      name: "",
      email: "",
      password: "",
      valid: true,
      show: false,
      loading: false,
      errorName: "",
      errorEmail: "",
      nameRules: [
        v => Boolean(v) || '名前は必須です。',
        v => (v && v.length <= 30) || '名前は30文字以下である必要があります。',
      ],
      emailRules: [
        v => Boolean(v) || 'E-mailは必須です。',
        v => /.+@.+\..+/.test(v) || '電子メールは有効である必要があります。',
      ],
      passRules: [
        v => Boolean(v) || 'パスワードは必須です。',
        v => (v && v.length >= 8) || '最低８文字必要です。',
      ]
    }
  },
  methods: {
    // ボタン
    validate() {
      // 空文字の場合
      if (this.name == "" || this.name == undefined) return;

      // 入力値の検証と登録
      this.$refs.form.validate();
      this.register();
    },
    reset() {
      // リセット、エラー文字を削除
      this.$refs.form.reset();
      this.errorName = "";
      this.errorEmail = "";
    },
  },
}