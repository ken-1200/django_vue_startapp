export const loginMixins = {
  data() {
    return {
      error: "",
      alert: false,
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
    onError() {
      // エラー内容を変数に格納
      this.error = this.$store.getters.errorInfo;

      // アラート判定
      if (this.error) {
        this.alert = true;

        // 5s後にリセット
        setTimeout(() => {
          this.reset();
        }, 3600);
      } else {
        this.alert = false;
      }

      // エラー内容リセット
      this.$store.dispatch('setError', null);
    },
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

      // アラートリセット
      this.alert = false;
      this.error = "";
    },
  },
  computed: {
    errorInfo() {
      return this.error;
    },
  },
}