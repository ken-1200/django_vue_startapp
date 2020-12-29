export default class ScrollObserver {
  constructor(els, cb, options) {
    // 要素を取得する
    this.els = document.querySelectorAll(els);
    const defaultOptions = {
      root: null,
      rootMargin: "0px",
      threshold: 0,
      once: true
    };
    this.cb = cb;
    // optionsをマージする
    this.options = Object.assign(defaultOptions, options);
    this.once = this.options.once;
    this._init();
  }

  // メソッド
  _init() {
    const callback = ((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          // 登録した要素が画面に入った場合
          this.cb(entry.target, true);

          if (this.once) {
            // 画面内の状態で監視を停止
            observer.unobserve(entry.target);
          }
        } else {
          // 要素が画面から出た場合
          this.cb(entry.target, false);
        }
      });
    })

    // 登録した要素が交差するタイミングでコールバック関数が呼ばれる
    this.io = new IntersectionObserver(callback.bind(this), this.options);
    this.els.forEach(el => {
      // 検知したい要素を登録して監視する
      this.io.observe(el);
    });
  }

  // ユーザが必要なくなったときに、それを解放してあげる役割がある。
  destory() {
    this.io.disconnect();
  }
}